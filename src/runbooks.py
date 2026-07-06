"""Runbook recommendation and executive report utilities."""
from __future__ import annotations
import pandas as pd
from .anomaly import service_health, prioritize_alerts, deployment_impact


def recommend_runbooks(df: pd.DataFrame) -> pd.DataFrame:
    health = service_health(df)
    alerts = prioritize_alerts(df).head(20)
    deps = deployment_impact(df)
    rows = []
    for _, row in health.head(5).iterrows():
        if row["rag_status"] != "Green":
            rows.append({"signal": f"{row['service_name']} health is {row['rag_status']}", "runbook": "Reliability review", "action": "Open problem record and review SLO/error budget", "owner": row["owner_team"], "priority": "High" if row["rag_status"] == "Red" else "Medium"})
    for _, alert in alerts.head(5).iterrows():
        rows.append({"signal": f"Anomaly on {alert['service_name']} in {alert['region']}", "runbook": "Anomaly triage", "action": alert["recommended_action"], "owner": alert["owner_team"], "priority": "High" if alert["customer_impact"] else "Medium"})
    bad_deps = deps[deps["suspected_bad"]] if not deps.empty else deps
    for _, dep in bad_deps.head(5).iterrows():
        rows.append({"signal": f"Deployment impact: {dep['deployment_id']}", "runbook": "Change failure review", "action": "Review release notes, compare metrics and decide rollback", "owner": dep["owner_team"], "priority": "High"})
    if not rows:
        rows.append({"signal": "No critical signals", "runbook": "Normal operations", "action": "Continue monitoring", "owner": "SRE Team", "priority": "Low"})
    return pd.DataFrame(rows).drop_duplicates().reset_index(drop=True)


def export_status_report(df: pd.DataFrame, recommendations: pd.DataFrame) -> str:
    health = service_health(df)
    red = health[health["rag_status"] == "Red"]["service_name"].tolist()
    amber = health[health["rag_status"] == "Amber"]["service_name"].tolist()
    lines = ["# CloudOps / AIOps Executive Status Report", "", "## RAG summary", f"- Red services: {', '.join(red) if red else 'none'}", f"- Amber services: {', '.join(amber) if amber else 'none'}", f"- Average service health: {health['health_score'].mean():.1f}/100", "", "## Recommended actions"]
    for _, r in recommendations.iterrows():
        lines.append(f"- **[{r['priority']}] {r['signal']}** — {r['action']} (owner: {r['owner']}, runbook: {r['runbook']})")
    lines.append("\n_Generated from synthetic telemetry. Portfolio project by Samadrita Acharya._")
    return "\n".join(lines)
