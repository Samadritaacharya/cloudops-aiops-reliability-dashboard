"""CloudOps / AIOps Reliability Dashboard."""
from __future__ import annotations

import plotly.express as px
import streamlit as st

from src.data_generator import generate_metrics
from src.anomaly import detect_anomalies, service_health, prioritize_alerts, deployment_impact
from src.runbooks import recommend_runbooks, export_status_report

st.set_page_config(page_title="CloudOps / AIOps Reliability", page_icon="🛰️", layout="wide")

st.markdown(
    """
    <style>
    .hero {
        background: linear-gradient(135deg, #08111f 0%, #123456 50%, #2563eb 100%);
        padding: 2rem 2.2rem;
        border-radius: 22px;
        color: white;
        margin-bottom: 1.4rem;
        box-shadow: 0 18px 55px rgba(8, 17, 31, 0.25);
    }
    .hero h1 {font-size: 2.35rem; margin: 0 0 .55rem 0; letter-spacing: -.04em;}
    .hero p {font-size: 1.02rem; max-width: 980px; color: #dbeafe; margin: 0;}
    .demo-card {
        border: 1px solid #d8e5f2;
        border-left: 5px solid #2563eb;
        border-radius: 14px;
        padding: 1rem 1.1rem;
        background: #f8fbff;
        margin-bottom: 1rem;
    }
    div[data-testid="stMetric"] {
        background: #f8fbff;
        border-left: 4px solid #2563eb;
        padding: 12px 16px;
        border-radius: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
      <h1>🛰️ CloudOps / AIOps Reliability Dashboard</h1>
      <p>Interactive cloud telemetry simulation for service health, anomaly detection, deployment impact and executive runbook decisions. Choose a scenario, click <b>Run AIOps simulation</b>, then explain how operational signals become PMO-ready actions.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

@st.cache_data
def load_data(days: int, seed: int):
    return generate_metrics(days=days, seed=seed)

@st.cache_data
def load_anomalies(days: int, seed: int):
    return detect_anomalies(load_data(days, seed))

def show(fig):
    st.plotly_chart(fig, width="stretch")

pages = [
    "1 Reliability Overview",
    "2 Service Metrics",
    "3 Incident Timeline",
    "4 Anomaly Detection",
    "5 Deployment and Change Impact",
    "6 Runbook Recommendations",
    "7 Executive Status Report",
]

if "cloudops_run" not in st.session_state:
    st.session_state.cloudops_run = 0

with st.sidebar:
    st.header("🎛️ Live demo inputs")
    page = st.radio("Navigation", pages)
    scenario = st.selectbox(
        "Scenario preset",
        ["Balanced cloud operations", "Deployment risk week", "Alert storm", "Regional latency spike"],
    )
    preset = {
        "Balanced cloud operations": (21, 42),
        "Deployment risk week": (21, 101),
        "Alert storm": (28, 155),
        "Regional latency spike": (35, 208),
    }[scenario]
    days = st.slider("Telemetry history in days", 7, 60, preset[0], step=7)
    seed = int(st.number_input("Simulation seed", value=preset[1], step=1))
    if st.button("🚀 Run AIOps simulation", width="stretch", type="primary"):
        st.session_state.cloudops_run += 1
    st.caption("Use this input panel to demonstrate: telemetry → anomaly detection → incident/runbook action → executive RAG report.")

st.markdown(
    f"""
    <div class="demo-card">
      <b>Current live input:</b> {scenario} · {days} days of hourly synthetic telemetry · run #{st.session_state.cloudops_run + 1}<br>
      <span style="color:#405264;">Best demo flow: Overview → Anomaly Detection → Deployment Impact → Runbook Recommendations → Executive Report.</span>
    </div>
    """,
    unsafe_allow_html=True,
)

effective_seed = seed + st.session_state.cloudops_run * 19
df = load_data(days, effective_seed)
anoms = load_anomalies(days, effective_seed)

with st.expander("🔎 Optional filters for live explanation", expanded=False):
    f1, f2 = st.columns(2)
    services = f1.multiselect("Filter service", sorted(df["service_name"].unique()))
    regions = f2.multiselect("Filter region", sorted(df["region"].unique()))
    if services:
        df = df[df["service_name"].isin(services)]
        anoms = anoms[anoms["service_name"].isin(services)]
    if regions:
        df = df[df["region"].isin(regions)]
        anoms = anoms[anoms["region"].isin(regions)]

health = service_health(anoms)

if page.startswith("1"):
    st.subheader("Reliability Overview")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Services", df["service_name"].nunique())
    c2.metric("Regions", df["region"].nunique())
    c3.metric("Avg health", f"{health['health_score'].mean():.1f}/100")
    c4.metric("Incident hours", int(df["incident_flag"].sum()))
    show(px.bar(health.sort_values("health_score"), x="health_score", y="service_name", color="rag_status", orientation="h", title="Service health scores"))
    show(px.line(df.groupby("timestamp")["alert_count"].sum().reset_index(), x="timestamp", y="alert_count", title="Alert volume over time"))

elif page.startswith("2"):
    st.subheader("Service Metrics")
    service = st.selectbox("Service", sorted(df["service_name"].unique()))
    view = df[df["service_name"] == service]
    c1, c2, c3 = st.columns(3)
    c1.metric("P95 latency", f"{view['latency_ms'].quantile(.95):.0f} ms")
    c2.metric("Avg error rate", f"{view['error_rate'].mean():.2%}")
    c3.metric("Total requests", f"{view['request_count'].sum():,}")
    show(px.line(view, x="timestamp", y="latency_ms", color="region", title=f"{service} latency"))
    show(px.line(view, x="timestamp", y="error_rate", color="region", title=f"{service} error rate"))

elif page.startswith("3"):
    st.subheader("Incident Timeline")
    incidents = df[df["incident_flag"]]
    st.metric("Incident hours", len(incidents))
    show(px.scatter(incidents, x="timestamp", y="service_name", color="severity", size="alert_count", hover_data=["region", "owner_team"], title="Incident timeline"))
    show(px.bar(incidents.groupby(["owner_team", "severity"])["timestamp"].count().reset_index(name="hours"), x="owner_team", y="hours", color="severity", title="Incident hours by owner"))

elif page.startswith("4"):
    st.subheader("Anomaly Detection")
    alerts = prioritize_alerts(df)
    st.metric("Anomalies", int(anoms["is_anomaly"].sum()))
    service = st.selectbox("Service for anomaly view", sorted(df["service_name"].unique()))
    show(px.scatter(anoms[anoms["service_name"] == service], x="timestamp", y="latency_ms", color="is_anomaly", title=f"{service} anomaly overlay"))
    st.subheader("Prioritized alert queue")
    st.dataframe(alerts[["timestamp", "service_name", "region", "severity", "priority_score", "recommended_action", "owner_team"]].head(30), width="stretch", hide_index=True)

elif page.startswith("5"):
    st.subheader("Deployment and Change Impact")
    impact = deployment_impact(df)
    if impact.empty:
        st.info("No deployments detected for the selected filters.")
    else:
        st.metric("Change failure rate", f"{impact['suspected_bad'].mean():.1%}")
        show(px.bar(impact, x="deployment_id", y="latency_delta_ms", color="suspected_bad", title="Deployment latency impact"))
        st.dataframe(impact.sort_values("latency_delta_ms", ascending=False).head(30), width="stretch", hide_index=True)

elif page.startswith("6"):
    st.subheader("Runbook Recommendations")
    recs = recommend_runbooks(df)
    st.dataframe(recs, width="stretch", hide_index=True)
    show(px.histogram(recs, x="priority", title="Runbook recommendations by priority"))

else:
    st.subheader("Executive Status Report")
    recs = recommend_runbooks(df)
    report = export_status_report(df, recs)
    st.dataframe(health, width="stretch", hide_index=True)
    st.download_button("Download executive status report", report, file_name="cloudops_aiops_status_report.md", mime="text/markdown", width="stretch")
    with st.expander("Preview report"):
        st.markdown(report)
