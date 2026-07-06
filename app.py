"""CloudOps / AIOps Reliability Dashboard."""
from __future__ import annotations
import plotly.express as px
import streamlit as st
from src.data_generator import generate_metrics
from src.anomaly import detect_anomalies, service_health, prioritize_alerts, deployment_impact
from src.runbooks import recommend_runbooks, export_status_report

st.set_page_config(page_title="CloudOps / AIOps Reliability", page_icon="🛰️", layout="wide")
st.title("CloudOps / AIOps Reliability Dashboard")
st.caption("Synthetic cloud telemetry for reliability monitoring, anomaly detection, deployment impact and executive reporting.")

@st.cache_data
def load_data(days: int, seed: int):
    return generate_metrics(days=days, seed=seed)

@st.cache_data
def load_anomalies(days: int, seed: int):
    return detect_anomalies(load_data(days, seed))

def show(fig):
    st.plotly_chart(fig, width="stretch")

pages = ["1 Reliability Overview", "2 Service Metrics", "3 Incident Timeline", "4 Anomaly Detection", "5 Deployment and Change Impact", "6 Runbook Recommendations", "7 Executive Status Report"]
with st.sidebar:
    page = st.radio("Navigation", pages)
    days = st.slider("History days", 7, 60, 21, step=7)
    seed = int(st.number_input("Random seed", value=42, step=1))
    st.caption("All telemetry is synthetic.")

df = load_data(days, seed)
anoms = load_anomalies(days, seed)
health = service_health(anoms)

if page.startswith("1"):
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Services", df["service_name"].nunique())
    c2.metric("Regions", df["region"].nunique())
    c3.metric("Avg health", f"{health['health_score'].mean():.1f}/100")
    c4.metric("Incident hours", int(df["incident_flag"].sum()))
    show(px.bar(health.sort_values("health_score"), x="health_score", y="service_name", color="rag_status", orientation="h", title="Service health scores"))
    show(px.line(df.groupby("timestamp")["alert_count"].sum().reset_index(), x="timestamp", y="alert_count", title="Alert volume over time"))

elif page.startswith("2"):
    service = st.selectbox("Service", sorted(df["service_name"].unique()))
    view = df[df["service_name"] == service]
    c1, c2, c3 = st.columns(3)
    c1.metric("P95 latency", f"{view['latency_ms'].quantile(.95):.0f} ms")
    c2.metric("Avg error rate", f"{view['error_rate'].mean():.2%}")
    c3.metric("Total requests", f"{view['request_count'].sum():,}")
    show(px.line(view, x="timestamp", y="latency_ms", color="region", title=f"{service} latency"))
    show(px.line(view, x="timestamp", y="error_rate", color="region", title=f"{service} error rate"))

elif page.startswith("3"):
    incidents = df[df["incident_flag"]]
    st.metric("Incident hours", len(incidents))
    show(px.scatter(incidents, x="timestamp", y="service_name", color="severity", size="alert_count", hover_data=["region", "owner_team"], title="Incident timeline"))
    show(px.bar(incidents.groupby(["owner_team", "severity"])["timestamp"].count().reset_index(name="hours"), x="owner_team", y="hours", color="severity", title="Incident hours by owner"))

elif page.startswith("4"):
    alerts = prioritize_alerts(df)
    st.metric("Anomalies", int(anoms["is_anomaly"].sum()))
    service = st.selectbox("Service for anomaly view", sorted(df["service_name"].unique()))
    show(px.scatter(anoms[anoms["service_name"] == service], x="timestamp", y="latency_ms", color="is_anomaly", title=f"{service} anomaly overlay"))
    st.subheader("Prioritized alert queue")
    st.dataframe(alerts[["timestamp", "service_name", "region", "severity", "priority_score", "recommended_action", "owner_team"]].head(30), width="stretch", hide_index=True)

elif page.startswith("5"):
    impact = deployment_impact(df)
    if impact.empty:
        st.info("No deployments detected.")
    else:
        st.metric("Change failure rate", f"{impact['suspected_bad'].mean():.1%}")
        show(px.bar(impact, x="deployment_id", y="latency_delta_ms", color="suspected_bad", title="Deployment latency impact"))
        st.dataframe(impact.sort_values("latency_delta_ms", ascending=False).head(30), width="stretch", hide_index=True)

elif page.startswith("6"):
    recs = recommend_runbooks(df)
    st.dataframe(recs, width="stretch", hide_index=True)
    show(px.histogram(recs, x="priority", title="Runbook recommendations by priority"))

else:
    recs = recommend_runbooks(df)
    report = export_status_report(df, recs)
    st.subheader("Executive RAG status")
    st.dataframe(health, width="stretch", hide_index=True)
    st.download_button("Download executive status report", report, file_name="cloudops_aiops_status_report.md", mime="text/markdown")
    with st.expander("Preview report"):
        st.markdown(report)
