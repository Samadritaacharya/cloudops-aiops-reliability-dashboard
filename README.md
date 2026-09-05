# CloudOps / AIOps Reliability Dashboard

[![Python CI](https://github.com/Samadritaacharya/cloudops-aiops-reliability-dashboard/actions/workflows/ci.yml/badge.svg)](https://github.com/Samadritaacharya/cloudops-aiops-reliability-dashboard/actions/workflows/ci.yml)

**A cloud-operations reliability application for service-health scoring, anomaly detection, deployment-impact analysis, incident prioritization, runbook recommendations, and executive RAG reporting.**

[**Open live app →**](https://cloudops-aiops-reliability-dashboard.streamlit.app/) · [Validation evidence](VALIDATION_REPORT.md) · [Source](https://github.com/Samadritaacharya/cloudops-aiops-reliability-dashboard)

> All telemetry, incidents, alerts, and deployments are synthetic. No confidential employer, customer, or client information is used.

## What it does

The application turns noisy operational signals into decision-ready reliability views:

- Red/Amber/Green service-health scoring
- latency, error-rate, CPU, memory, traffic, and uptime analysis
- severity-coded incident timelines and ownership
- rolling z-score and Isolation Forest anomaly detection
- prioritized alert queues
- deployment and change-impact analysis
- signal-to-runbook recommendations
- downloadable executive status reports

## Dashboard pages

| # | Page | Decision supported |
|---|---|---|
| 1 | Reliability Overview | Which services need attention? |
| 2 | Service Metrics | Which technical signals explain degraded health? |
| 3 | Incident Timeline | What happened, with what severity, and who owns it? |
| 4 | Anomaly Detection | Which unusual signals deserve priority? |
| 5 | Deployment & Change Impact | Did a recent deployment increase risk? |
| 6 | Runbook Recommendations | What operational response should happen next? |
| 7 | Executive Status Report | What should leadership understand and decide? |

## Verification snapshot

The recorded validation includes:

- `11/11` pytest tests passed
- `7/7` Streamlit pages rendered with Streamlit AppTest
- Streamlit health endpoint returned `200 ok`
- telemetry generation, anomaly detection, service-health scoring, deployment impact, and runbook recommendations verified

GitHub Actions reruns the automated checks on future changes. See [VALIDATION_REPORT.md](VALIDATION_REPORT.md) for scope and limitations.

## Technology

`Python` · `Streamlit` · `Pandas` · `NumPy` · `Plotly` · `scikit-learn` · `pytest` · `GitHub Actions` · `Docker`

## Run locally

```bash
git clone https://github.com/Samadritaacharya/cloudops-aiops-reliability-dashboard.git
cd cloudops-aiops-reliability-dashboard
python -m venv .venv
```

```bash
# Windows PowerShell
.\.venv\Scripts\Activate.ps1

# macOS/Linux
source .venv/bin/activate
```

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pytest -q
python -m streamlit run app.py
```

## Design principle

Reliability tooling is most useful when it helps teams decide **what needs attention, why it changed, who owns the next action, and what evidence supports that decision**.
