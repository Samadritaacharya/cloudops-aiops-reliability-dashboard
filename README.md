# CloudOps / AIOps Reliability Dashboard

**A cloud operations reliability dashboard** for service health scoring, latency/error monitoring, incident timelines, anomaly detection, deployment impact analysis, runbook recommendations and an executive RAG status report.

> 🔗 **Live demo:** _add your Streamlit Cloud link here after deployment_

---

## Business problem

Cloud teams often work with noisy telemetry, frequent deployments and many alerts. Leadership needs a clear view of which services are healthy, which deployments caused risk, which anomalies matter and what action should be taken next.

## Solution

This project simulates a cloud operations environment with synthetic telemetry and turns it into a practical AIOps-style reliability dashboard:

- service health scoring with Red/Amber/Green status
- service metrics for latency, error rate, CPU, memory and traffic
- incident timeline by severity and owning team
- anomaly detection using rolling z-scores and Isolation Forest
- deployment/change impact analysis
- prioritized alert queue
- runbook recommendations with owners and priorities
- downloadable executive status report

## Dashboard pages

| # | Page | What it shows |
|---|------|---------------|
| 1 | Reliability Overview | Service health, uptime and alert summary |
| 2 | Service Metrics | Latency, error rate, CPU, memory and traffic |
| 3 | Incident Timeline | Severity-coded incidents and ownership |
| 4 | Anomaly Detection | Anomalies and prioritized alert queue |
| 5 | Deployment & Change Impact | Before/after deployment impact and change failure indicators |
| 6 | Runbook Recommendations | Signal-to-action recommendations |
| 7 | Executive Status Report | RAG status and downloadable Markdown report |

## Tech stack

`Python` · `Streamlit` · `Pandas` · `NumPy` · `Plotly` · `scikit-learn` · `pytest` · `Docker`

## Validation status

Tested before publication:

- `11/11` pytest tests passed
- `7/7` Streamlit pages rendered successfully
- Streamlit app booted successfully
- Health endpoint returned `200 ok`

## How to run locally

```bash
git clone https://github.com/Samadritaacharya/cloudops-aiops-reliability-dashboard.git
cd cloudops-aiops-reliability-dashboard
pip install -r requirements.txt
streamlit run app.py
```

Run tests:

```bash
pytest -v
```

## Deploy to Streamlit Cloud

Use:

```text
Repository: Samadritaacharya/cloudops-aiops-reliability-dashboard
Branch: main
Main file path: app.py
```

## Why this project is relevant to my target roles

This project connects directly to my SAP Cloud Delivery Architecture / AIOps PMO experience. It demonstrates practical thinking for cloud operations, AIOps, incident management, reliability reporting, runbook ownership and technical project coordination.

Relevant target roles:

- Cloud Operations Analyst
- AIOps / Observability Associate
- Technical Project Coordinator
- PMO Analyst
- Digital Transformation Associate
- Site Reliability / Operations-adjacent junior roles

## CV bullet

> Built a CloudOps/AIOps Reliability Dashboard using Python, Streamlit, Pandas, Plotly and scikit-learn to simulate cloud service-health monitoring, anomaly detection, deployment-impact analysis, incident timelines and executive RAG reporting.

## Disclaimer

All telemetry, deployments and incidents are synthetic. No confidential SAP, AWS, IBM, Kyndryl, employer or client data is used.

---

**Samadrita Acharya** · [LinkedIn](https://www.linkedin.com/in/samadrita-acharya-a07266184/) · [GitHub](https://github.com/Samadritaacharya)
