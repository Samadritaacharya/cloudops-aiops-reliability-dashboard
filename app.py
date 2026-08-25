"""CloudOps / AIOps Reliability Dashboard."""
from __future__ import annotations

import plotly.express as px
import streamlit as st

from src.data_generator import generate_metrics
from src.anomaly import detect_anomalies, service_health, prioritize_alerts, deployment_impact
from src.runbooks import recommend_runbooks, export_status_report

st.set_page_config(
    page_title="CloudOps / AIOps Reliability",
    page_icon="◌",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get help": "https://github.com/Samadritaacharya/cloudops-aiops-reliability-dashboard",
        "Report a bug": "https://github.com/Samadritaacharya/cloudops-aiops-reliability-dashboard/issues",
        "About": "Independent CloudOps/AIOps portfolio project using synthetic telemetry.",
    },
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    html, body, [class*="css"] {font-family: Inter, system-ui, sans-serif;}
    .stApp {
      background:
        radial-gradient(circle at 12% -5%, rgba(37,99,235,.20), transparent 31rem),
        radial-gradient(circle at 88% 4%, rgba(6,182,212,.14), transparent 34rem),
        #07111f;
      color:#e7eef8;
    }
    .block-container {max-width:1500px;padding-top:1.15rem;padding-bottom:4rem;}
    h1,h2,h3,p,label {color:#eaf2ff;}
    .cloud-hero {
      position:relative;overflow:hidden;
      background:linear-gradient(120deg,rgba(11,25,45,.96),rgba(12,45,78,.94) 55%,rgba(13,78,111,.94));
      border:1px solid rgba(125,211,252,.16);
      border-radius:28px;padding:2.55rem 2.7rem;margin-bottom:1.1rem;
      box-shadow:0 32px 100px rgba(0,0,0,.35);
    }
    .cloud-hero:before {content:'';position:absolute;inset:0;background:linear-gradient(90deg,transparent 0 49.5%,rgba(255,255,255,.025) 50% 50.5%,transparent 51%);background-size:38px 100%;opacity:.45;pointer-events:none;}
    .cloud-hero:after {content:'';position:absolute;width:430px;height:430px;border-radius:999px;right:-130px;top:-200px;background:rgba(56,189,248,.16);filter:blur(8px);}
    .eyebrow {position:relative;z-index:1;color:#67e8f9;font-size:.75rem;letter-spacing:.14em;text-transform:uppercase;font-weight:800;margin-bottom:.72rem;}
    .cloud-hero h1 {position:relative;z-index:1;font-size:clamp(2.25rem,4.8vw,4.05rem);line-height:1;margin:0 0 .85rem;color:#fff;letter-spacing:-.055em;}
    .cloud-hero p {position:relative;z-index:1;max-width:1000px;color:#c8d9ef;font-size:1.04rem;line-height:1.72;margin:0;}
    .status-row {display:flex;flex-wrap:wrap;gap:.48rem;margin-top:1.2rem;position:relative;z-index:1;}
    .status-chip {display:inline-flex;align-items:center;gap:.42rem;padding:.36rem .7rem;border-radius:999px;background:rgba(255,255,255,.065);border:1px solid rgba(148,163,184,.16);color:#dbeafe;font-size:.78rem;font-weight:650;backdrop-filter:blur(12px);}
    .pulse {width:.48rem;height:.48rem;border-radius:99px;background:#22d3ee;box-shadow:0 0 0 5px rgba(34,211,238,.10);animation:pulse 2.4s infinite;}
    @keyframes pulse {0%,100%{box-shadow:0 0 0 5px rgba(34,211,238,.10)}50%{box-shadow:0 0 0 9px rgba(34,211,238,.02)}}
    .signal-flow {display:grid;grid-template-columns:repeat(5,1fr);gap:.58rem;margin:.8rem 0 1.05rem;}
    .signal-step {background:rgba(13,27,45,.88);border:1px solid rgba(125,211,252,.12);border-radius:15px;padding:.82rem .9rem;box-shadow:0 12px 32px rgba(0,0,0,.16);}
    .signal-step strong {display:block;color:#dff6ff;font-size:.82rem;margin-bottom:.2rem;}
    .signal-step span {color:#849bb5;font-size:.74rem;}
    .signal-step b {color:#22d3ee;font-size:.69rem;margin-right:.25rem;}
    .context-card {background:rgba(10,23,40,.88);border:1px solid rgba(125,211,252,.13);border-radius:17px;padding:1rem 1.1rem;margin-bottom:1rem;color:#b8cbe0;box-shadow:0 14px 38px rgba(0,0,0,.18);}
    .context-card strong {color:#67e8f9;}
    .context-card .muted {font-size:.86rem;color:#7f96ae;margin-top:.3rem;}
    .section-kicker {font-size:.74rem;letter-spacing:.12em;text-transform:uppercase;color:#22d3ee;font-weight:800;margin-top:1.1rem;}
    div[data-testid="stMetric"] {background:linear-gradient(180deg,rgba(15,31,52,.96),rgba(9,23,39,.96));border:1px solid rgba(125,211,252,.13);border-top:3px solid #2563eb;padding:14px 16px;border-radius:16px;box-shadow:0 14px 38px rgba(0,0,0,.18);}
    div[data-testid="stMetricLabel"] {color:#91a8c0;}
    div[data-testid="stMetricValue"] {color:#f4f8ff;letter-spacing:-.035em;}
    [data-testid="stSidebar"] {background:linear-gradient(180deg,#030b14 0%,#071725 100%);border-right:1px solid rgba(125,211,252,.11);}
    [data-testid="stSidebar"] * {color:#dce9f7;}
    [data-testid="stSidebar"] [data-baseweb="select"] > div,
    [data-testid="stSidebar"] input {background:rgba(255,255,255,.055)!important;border-color:rgba(125,211,252,.13)!important;color:#fff!important;}
    .stButton>button,.stDownloadButton>button {border-radius:12px!important;font-weight:750!important;min-height:2.65rem;border-color:rgba(125,211,252,.15)!important;transition:transform .18s ease,box-shadow .18s ease!important;}
    .stButton>button:hover,.stDownloadButton>button:hover {transform:translateY(-1px);box-shadow:0 10px 28px rgba(37,99,235,.24)!important;}
    div[data-testid="stExpander"] {background:rgba(10,23,40,.82);border:1px solid rgba(125,211,252,.12);border-radius:14px;}
    div[data-testid="stDataFrame"] {border:1px solid rgba(125,211,252,.12);border-radius:14px;overflow:hidden;}
    [data-testid="stAlert"] {border-radius:14px;}
    @media(max-width:950px){.signal-flow{grid-template-columns:1fr 1fr}.cloud-hero{padding:2rem 1.45rem}}
    @media(max-width:560px){.signal-flow{grid-template-columns:1fr}}
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="cloud-hero">
      <div class="eyebrow">Observability · Reliability · AIOps Decision Cockpit</div>
      <h1>CloudOps / AIOps Reliability</h1>
      <p>Simulate a multi-service cloud estate, detect unusual telemetry, connect incidents to deployments, prioritize alerts and translate technical signals into runbook actions and an executive reliability report.</p>
      <div class="status-row">
        <span class="status-chip"><span class="pulse"></span> Live synthetic telemetry</span>
        <span class="status-chip">Anomaly detection</span><span class="status-chip">Change impact</span><span class="status-chip">Runbook routing</span><span class="status-chip">Executive RAG</span>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="signal-flow">
      <div class="signal-step"><strong><b>01</b> Telemetry</strong><span>Latency, error, volume, alerts</span></div>
      <div class="signal-step"><strong><b>02</b> Detect</strong><span>Surface anomalous service behaviour</span></div>
      <div class="signal-step"><strong><b>03</b> Correlate</strong><span>Connect incidents and deployments</span></div>
      <div class="signal-step"><strong><b>04</b> Respond</strong><span>Prioritize owner + runbook action</span></div>
      <div class="signal-step"><strong><b>05</b> Report</strong><span>Summarize reliability for leadership</span></div>
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
    fig.update_layout(
        margin=dict(l=18, r=18, t=58, b=18),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, system-ui, sans-serif", color="#9db2c8"),
        title_font=dict(size=17, color="#eaf2ff"),
        legend_title_text="",
        hoverlabel=dict(font_size=13),
    )
    fig.update_xaxes(gridcolor="rgba(148,163,184,.10)", zerolinecolor="rgba(148,163,184,.10)")
    fig.update_yaxes(gridcolor="rgba(148,163,184,.10)", zerolinecolor="rgba(148,163,184,.10)")
    st.plotly_chart(fig, width="stretch", config={"displaylogo": False})


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
    st.markdown("### ◌ Reliability Console")
    st.caption("Navigate from telemetry to an accountable reliability decision.")
    page = st.radio("Workspace", pages)
    st.divider()
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
    days = st.slider("Telemetry history", 7, 60, preset[0], step=7, format="%d days")
    seed = int(st.number_input("Simulation seed", value=preset[1], step=1))
    if st.button("Run AIOps simulation →", width="stretch", type="primary"):
        st.session_state.cloudops_run += 1
    st.divider()
    st.caption("Synthetic telemetry only. No employer, customer, production or personal data.")

effective_seed = seed + st.session_state.cloudops_run * 19
df = load_data(days, effective_seed)
anoms = load_anomalies(days, effective_seed)

with st.expander("Filters · isolate services and regions", expanded=False):
    f1, f2 = st.columns(2)
    services = f1.multiselect("Service", sorted(df["service_name"].unique()))
    regions = f2.multiselect("Region", sorted(df["region"].unique()))
    if services:
        df = df[df["service_name"].isin(services)]
        anoms = anoms[anoms["service_name"].isin(services)]
    if regions:
        df = df[df["region"].isin(regions)]
        anoms = anoms[anoms["region"].isin(regions)]

health = service_health(anoms)
avg_health = health["health_score"].mean()
ops_signal = "Healthy" if avg_health >= 85 else "Watch" if avg_health >= 70 else "Degraded"

st.markdown(
    f"""
    <div class="context-card"><strong>{scenario}</strong> · {days} days of hourly telemetry · simulation {st.session_state.cloudops_run + 1} · fleet signal: <strong>{ops_signal}</strong>
      <div class="muted">Recommended demo path: Overview → Anomaly Detection → Deployment Impact → Runbooks → Executive Report.</div>
    </div>
    """,
    unsafe_allow_html=True,
)

if page.startswith("1"):
    st.markdown('<div class="section-kicker">Command view</div>', unsafe_allow_html=True)
    st.subheader("Reliability Overview")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Services", df["service_name"].nunique())
    c2.metric("Regions", df["region"].nunique())
    c3.metric("Avg health", f"{avg_health:.1f}/100")
    c4.metric("Incident hours", int(df["incident_flag"].sum()))
    col1, col2 = st.columns([1.15, 1])
    with col1:
        show(px.bar(health.sort_values("health_score"), x="health_score", y="service_name", color="rag_status", orientation="h", title="Service health ranking"))
    with col2:
        show(px.line(df.groupby("timestamp")["alert_count"].sum().reset_index(), x="timestamp", y="alert_count", title="Alert volume over time"))
    st.info(f"Current fleet readout: **{ops_signal}** at **{avg_health:.1f}/100** average health. Use anomaly and deployment views to separate persistent service weakness from change-driven risk.")

elif page.startswith("2"):
    st.markdown('<div class="section-kicker">Service drill-down</div>', unsafe_allow_html=True)
    st.subheader("Service Metrics")
    service = st.selectbox("Service", sorted(df["service_name"].unique()))
    view = df[df["service_name"] == service]
    c1, c2, c3 = st.columns(3)
    c1.metric("P95 latency", f"{view['latency_ms'].quantile(.95):.0f} ms")
    c2.metric("Avg error rate", f"{view['error_rate'].mean():.2%}")
    c3.metric("Total requests", f"{view['request_count'].sum():,}")
    show(px.line(view, x="timestamp", y="latency_ms", color="region", title=f"{service} · latency"))
    show(px.line(view, x="timestamp", y="error_rate", color="region", title=f"{service} · error rate"))

elif page.startswith("3"):
    st.markdown('<div class="section-kicker">Incident intelligence</div>', unsafe_allow_html=True)
    st.subheader("Incident Timeline")
    incidents = df[df["incident_flag"]]
    st.metric("Incident hours", len(incidents))
    show(px.scatter(incidents, x="timestamp", y="service_name", color="severity", size="alert_count", hover_data=["region", "owner_team"], title="Incident timeline"))
    show(px.bar(incidents.groupby(["owner_team", "severity"])["timestamp"].count().reset_index(name="hours"), x="owner_team", y="hours", color="severity", title="Incident hours by owner"))

elif page.startswith("4"):
    st.markdown('<div class="section-kicker">Signal detection</div>', unsafe_allow_html=True)
    st.subheader("Anomaly Detection")
    alerts = prioritize_alerts(df)
    st.metric("Anomalies detected", int(anoms["is_anomaly"].sum()))
    service = st.selectbox("Service for anomaly view", sorted(df["service_name"].unique()))
    show(px.scatter(anoms[anoms["service_name"] == service], x="timestamp", y="latency_ms", color="is_anomaly", title=f"{service} · anomaly overlay"))
    st.subheader("Prioritized response queue")
    st.dataframe(alerts[["timestamp", "service_name", "region", "severity", "priority_score", "recommended_action", "owner_team"]].head(30), width="stretch", hide_index=True)

elif page.startswith("5"):
    st.markdown('<div class="section-kicker">Release risk</div>', unsafe_allow_html=True)
    st.subheader("Deployment & Change Impact")
    impact = deployment_impact(df)
    if impact.empty:
        st.info("No deployments detected for the selected filters.")
    else:
        st.metric("Change failure rate", f"{impact['suspected_bad'].mean():.1%}")
        show(px.bar(impact, x="deployment_id", y="latency_delta_ms", color="suspected_bad", title="Deployment latency impact"))
        st.dataframe(impact.sort_values("latency_delta_ms", ascending=False).head(30), width="stretch", hide_index=True)

elif page.startswith("6"):
    st.markdown('<div class="section-kicker">Response orchestration</div>', unsafe_allow_html=True)
    st.subheader("Runbook Recommendations")
    recs = recommend_runbooks(df)
    c1, c2 = st.columns([1.4, 1])
    with c1:
        st.dataframe(recs, width="stretch", hide_index=True)
    with c2:
        show(px.histogram(recs, x="priority", title="Runbooks by priority"))

else:
    st.markdown('<div class="section-kicker">Leadership communication</div>', unsafe_allow_html=True)
    st.subheader("Executive Status Report")
    recs = recommend_runbooks(df)
    report = export_status_report(df, recs)
    st.dataframe(health, width="stretch", hide_index=True)
    st.download_button("Download executive reliability report", report, file_name="cloudops_aiops_status_report.md", mime="text/markdown", width="stretch")
    with st.expander("Preview report"):
        st.markdown(report)
