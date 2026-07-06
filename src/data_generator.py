import pandas as pd

def generate_metrics(days=14, seed=42):
    return pd.DataFrame({"timestamp":[pd.Timestamp("2026-01-01")],"service_name":["checkout"],"region":["eu"],"latency_ms":[100.0],"error_rate":[0.01],"cpu_usage":[40.0],"memory_usage":[50.0],"request_count":[1000],"deployment_id":["REL0001"],"incident_flag":[False],"severity":["None"],"customer_impact":[False],"alert_count":[1],"owner_team":["Cloud Team"]})

SERVICES=["checkout"]
REGIONS=["eu"]
