"""Synthetic CloudOps telemetry generator."""
from __future__ import annotations
import numpy as np
import pandas as pd

SERVICES = ["checkout", "payments", "identity", "catalog", "search", "orders", "reco", "monitoring"]
REGIONS = ["eu-central", "eu-west", "us-east"]


def generate_metrics(days: int = 14, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    stamps = pd.date_range(end=pd.Timestamp.today().floor("h"), periods=days * 24, freq="h")
    rows = []
    for svc_i, svc in enumerate(SERVICES):
        for reg_i, reg in enumerate(REGIONS):
            base = 90 + svc_i * 10 + reg_i * 5
            for i, ts in enumerate(stamps):
                release = f"REL{svc_i}{reg_i}{i:04d}" if i > 0 and i % 72 == 0 else ""
                stress = (i % 72) in range(1, 8) and i > 20
                load = 1 + 0.25 * np.sin(ts.hour / 24 * 2 * np.pi)
                latency = base * load + rng.normal(0, 8) + (120 if stress else 0)
                err = max(0.001, 0.006 + rng.normal(0, 0.002) + (0.055 if stress else 0))
                cpu = min(95, 45 + rng.normal(0, 8) + (25 if stress else 0))
                mem = min(95, 55 + rng.normal(0, 7) + (15 if stress else 0))
                inc = bool(stress or err > 0.06)
                sev = "SEV1" if inc and err > 0.07 else ("SEV2" if inc else "None")
                rows.append({
                    "timestamp": ts,
                    "service_name": svc,
                    "region": reg,
                    "latency_ms": round(float(latency), 2),
                    "error_rate": round(float(err), 5),
                    "cpu_usage": round(float(cpu), 2),
                    "memory_usage": round(float(mem), 2),
                    "request_count": int(1000 * load + rng.normal(0, 80)),
                    "deployment_id": release,
                    "incident_flag": inc,
                    "severity": sev,
                    "customer_impact": bool(inc and rng.random() < 0.7),
                    "alert_count": int(max(0, rng.poisson(2 + (8 if inc else 0)))),
                    "owner_team": f"{svc.title()} Team",
                })
    return pd.DataFrame(rows)
