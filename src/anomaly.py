"""AIOps anomaly, health, alert and deployment scoring utilities."""
from __future__ import annotations
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest


def uptime(df: pd.DataFrame) -> pd.Series:
    return 1 - df.groupby("service_name")["incident_flag"].mean()


def detect_anomalies(df: pd.DataFrame) -> pd.DataFrame:
    out = df.sort_values(["service_name", "region", "timestamp"]).copy()
    out["latency_mean_24h"] = out.groupby(["service_name", "region"])["latency_ms"].transform(lambda s: s.rolling(24, min_periods=6).mean())
    out["latency_std_24h"] = out.groupby(["service_name", "region"])["latency_ms"].transform(lambda s: s.rolling(24, min_periods=6).std()).fillna(1)
    out["z_score"] = ((out["latency_ms"] - out["latency_mean_24h"]) / out["latency_std_24h"]).fillna(0)
    features = out[["latency_ms", "error_rate", "cpu_usage", "memory_usage", "alert_count"]]
    model = IsolationForest(contamination=0.035, random_state=42)
    out["iforest_anomaly"] = model.fit_predict(features) == -1
    out["z_anomaly"] = out["z_score"].abs() > 3
    out["is_anomaly"] = out["iforest_anomaly"] | out["z_anomaly"] | out["incident_flag"]
    return out


def rag(score: float) -> str:
    if score >= 80:
        return "Green"
    if score >= 60:
        return "Amber"
    return "Red"


def service_health(df: pd.DataFrame) -> pd.DataFrame:
    if "is_anomaly" not in df.columns:
        df = detect_anomalies(df)
    rows = []
    for svc, g in df.groupby("service_name"):
        up = 1 - g["incident_flag"].mean()
        anomaly = g["is_anomaly"].mean()
        sev1 = (g["severity"] == "SEV1").mean()
        alerts = min(g["alert_count"].mean() / 10, 1)
        burn = min(g["error_rate"].mean() / 0.03, 1)
        score = max(0, 100 - anomaly * 30 - sev1 * 35 - alerts * 15 - burn * 20)
        rows.append({"service_name": svc, "owner_team": g["owner_team"].iloc[0], "uptime": round(float(up), 4), "anomaly_rate": round(float(anomaly), 4), "sev1_hours": int((g["severity"] == "SEV1").sum()), "avg_alerts": round(float(g["alert_count"].mean()), 2), "health_score": round(float(score), 1), "rag_status": rag(score)})
    return pd.DataFrame(rows).sort_values("health_score")


def prioritize_alerts(df: pd.DataFrame) -> pd.DataFrame:
    data = detect_anomalies(df)
    alerts = data[data["is_anomaly"]].copy()
    if alerts.empty:
        return alerts
    alerts["priority_score"] = alerts["error_rate"] * 1000 + alerts["latency_ms"] / 10 + alerts["alert_count"] * 2 + alerts["customer_impact"].astype(int) * 20
    alerts["recommended_action"] = np.where(alerts["deployment_id"] != "", "Review or rollback recent deployment", np.where(alerts["cpu_usage"] > 80, "Scale out service capacity", "Investigate anomaly and tune alert"))
    return alerts.sort_values("priority_score", ascending=False)


def deployment_impact(df: pd.DataFrame) -> pd.DataFrame:
    deployments = df[df["deployment_id"] != ""]
    rows = []
    for _, d in deployments.iterrows():
        svc, reg, ts = d["service_name"], d["region"], d["timestamp"]
        window = df[(df["service_name"] == svc) & (df["region"] == reg)]
        before = window[(window["timestamp"] >= ts - pd.Timedelta(hours=6)) & (window["timestamp"] < ts)]
        after = window[(window["timestamp"] > ts) & (window["timestamp"] <= ts + pd.Timedelta(hours=6))]
        if len(before) and len(after):
            latency_delta = after["latency_ms"].mean() - before["latency_ms"].mean()
            error_delta = after["error_rate"].mean() - before["error_rate"].mean()
            rows.append({"deployment_id": d["deployment_id"], "timestamp": ts, "service_name": svc, "region": reg, "latency_delta_ms": round(float(latency_delta), 2), "error_delta": round(float(error_delta), 4), "suspected_bad": bool(latency_delta > before["latency_ms"].mean() * 0.25 or error_delta > 0.02), "owner_team": d["owner_team"]})
    return pd.DataFrame(rows)
