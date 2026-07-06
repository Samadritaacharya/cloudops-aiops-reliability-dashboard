"""Tests for telemetry generation, anomaly detection, health scoring and runbooks."""
import pandas as pd
import pytest
from src.data_generator import generate_metrics, SERVICES, REGIONS
from src.anomaly import detect_anomalies, service_health, uptime, prioritize_alerts, deployment_impact, rag
from src.runbooks import recommend_runbooks, export_status_report

@pytest.fixture(scope="module")
def df():
    return generate_metrics(days=14, seed=7)

@pytest.fixture(scope="module")
def anomalies(df):
    return detect_anomalies(df)

def test_generator_columns_and_ranges(df):
    expected = {"timestamp", "service_name", "region", "latency_ms", "error_rate", "cpu_usage", "memory_usage", "request_count", "deployment_id", "incident_flag", "severity", "customer_impact", "alert_count", "owner_team"}
    assert expected.issubset(df.columns)
    assert set(df["service_name"].unique()) == set(SERVICES)
    assert set(df["region"].unique()) == set(REGIONS)
    assert (df["latency_ms"] > 0).all()
    assert df["error_rate"].between(0, 1).all()
    assert df["cpu_usage"].between(0, 100).all()

def test_generator_reproducible():
    pd.testing.assert_frame_equal(generate_metrics(days=5, seed=11), generate_metrics(days=5, seed=11))

def test_generator_has_deployments_and_incidents(df):
    assert (df["deployment_id"] != "").sum() > 0
    assert df["incident_flag"].sum() > 0

def test_anomaly_detection_flags_something(df, anomalies):
    assert "is_anomaly" in anomalies.columns
    rate = anomalies["is_anomaly"].mean()
    assert 0 < rate < 0.30
    assert anomalies[anomalies["incident_flag"]]["is_anomaly"].mean() >= anomalies[~anomalies["incident_flag"]]["is_anomaly"].mean()

def test_uptime_bounds(df):
    assert uptime(df).between(0, 1).all()

def test_service_health(anomalies):
    h = service_health(anomalies)
    assert h["health_score"].between(0, 100).all()
    assert set(h["rag_status"]).issubset({"Green", "Amber", "Red"})
    assert len(h) == len(SERVICES)

def test_rag():
    assert rag(90) == "Green"
    assert rag(70) == "Amber"
    assert rag(50) == "Red"

def test_prioritize_alerts(df):
    alerts = prioritize_alerts(df)
    assert not alerts.empty
    assert alerts["priority_score"].is_monotonic_decreasing
    assert "recommended_action" in alerts.columns

def test_deployment_impact(df):
    impact = deployment_impact(df)
    assert not impact.empty
    assert {"deployment_id", "latency_delta_ms", "error_delta", "suspected_bad"}.issubset(impact.columns)

def test_runbooks(df):
    recs = recommend_runbooks(df)
    assert not recs.empty
    assert {"signal", "runbook", "action", "owner", "priority"}.issubset(recs.columns)

def test_status_report(df):
    report = export_status_report(df, recommend_runbooks(df))
    assert report.startswith("# CloudOps / AIOps Executive Status Report")
    assert "Recommended actions" in report
