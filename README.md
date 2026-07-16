# CloudOps / AIOps Reliability Dashboard

A cloud-operations reliability application for service-health scoring, latency and error monitoring, incident timelines, anomaly detection, deployment-impact analysis, runbook recommendations, and executive RAG reporting.

[![Python CI](https://github.com/Samadritaacharya/cloudops-aiops-reliability-dashboard/actions/workflows/ci.yml/badge.svg)](https://github.com/Samadritaacharya/cloudops-aiops-reliability-dashboard/actions/workflows/ci.yml)

**Live application:** [cloudops-aiops-reliability-dashboard.streamlit.app](https://cloudops-aiops-reliability-dashboard.streamlit.app/)  
**Validation evidence:** [VALIDATION_REPORT.md](VALIDATION_REPORT.md)  
**Portfolio owner:** [Samadrita Acharya](https://www.linkedin.com/in/samadrita-acharya-a07266184/)

## Recruiter quick view

| Area | Evidence in this project |
|---|---|
| Business problem | Cloud teams need to turn noisy telemetry, incidents, alerts, and deployment signals into clear operational priorities. |
| Product solution | A seven-page Streamlit reliability dashboard using synthetic cloud telemetry and incident data. |
| AIOps analytics | Rolling z-score and Isolation Forest anomaly detection, alert prioritization, and service-health scoring. |
| Change reliability | Before/after deployment analysis and change-failure indicators. |
| Operational action | Runbook recommendations with owners and priorities plus an executive Markdown status report. |
| Engineering | Modular Python, automated tests, GitHub Actions, Docker support, and documented validation. |
| Data/privacy | All telemetry, incidents, and deployments are synthetic. |

## Business problem

Cloud teams work across high-volume telemetry, frequent deployments, alert noise, and distributed service ownership. The key challenge is not displaying more charts; it is deciding which services require attention, which changes increased risk, and what action should happen next.

## Solution

The application simulates a cloud operations environment and provides:

- Red/Amber/Green service-health scoring
- latency, error-rate, CPU, memory, traffic, and uptime views
- severity-coded incident timelines and team ownership
- rolling z-score and Isolation Forest anomaly detection
- prioritized alert queues
- deployment and change-impact analysis
- signal-to-runbook recommendations
- downloadable executive status reports

## Two-minute recruiter demo

1. Open the [live app](https://cloudops-aiops-reliability-dashboard.streamlit.app/).
2. Select **Deployment risk week**, **Alert storm**, or **Regional latency spike**.
3. Click **Run AIOps simulation**.
4. Review service health and telemetry signals.
5. Explain the anomaly and deployment-impact findings.
6. Finish with the recommended runbooks and executive RAG report.

## Dashboard pages

| # | Page | Decision supported |
|---|---|---|
| 1 | Reliability Overview | Which services currently need attention? |
| 2 | Service Metrics | Which technical signals explain degraded health? |
| 3 | Incident Timeline | What happened, with what severity, and who owns it? |
| 4 | Anomaly Detection | Which unusual signals should be prioritized? |
| 5 | Deployment & Change Impact | Did a recent deployment increase operational risk? |
| 6 | Runbook Recommendations | What operational response should happen next? |
| 7 | Executive Status Report | What should leadership understand and decide? |

## Validation status

The repository includes a documented pre-publication validation report:

- `11/11` pytest tests passed
- `7/7` Streamlit pages rendered with Streamlit AppTest
- Streamlit server started successfully
- health endpoint returned `200 ok`
- telemetry generation, anomaly detection, service-health scoring, deployment impact, and runbook recommendations were verified

See [VALIDATION_REPORT.md](VALIDATION_REPORT.md) for the recorded validation scope. GitHub Actions now reruns the test suite for future changes.

## Technology stack

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

## Skills demonstrated

Cloud operations · AIOps · observability · anomaly detection · incident management · deployment/change analysis · service reliability · RAG reporting · operational runbooks · PMO coordination · Python engineering · executive communication

## Why this project is relevant to my profile

This project connects directly to my SAP Cloud Delivery Architecture / AIOps and Sovereign Cloud PMO experience. It demonstrates how technical telemetry can be translated into service-health decisions, incident priorities, runbook ownership, and leadership-ready status reporting.

## CV / LinkedIn project description

> Built a tested CloudOps/AIOps Reliability Dashboard using Python, Streamlit, Pandas, Plotly, and scikit-learn to simulate cloud-service monitoring, detect anomalies, analyze deployment impact, prioritize incidents and alerts, recommend runbooks, and generate executive RAG reports.

## Responsible portfolio use

All telemetry, incidents, alerts, and deployments are synthetic. The project is independent and contains no confidential SAP, AWS, IBM, Kyndryl, employer, customer, or client data.
