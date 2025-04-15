
# 📘 Moon Insurance Microservices - Runbook

## 🗓️ Last Updated
2025-04-15 04:41:33 UTC

---

## 🚀 Overview

This runbook documents how to deploy, test, and operate the **Moon Agent Tracker** microservices platform for MoonInsurance. It includes deployment steps for GKE (Google Kubernetes Engine), Redshift integration, and automated CI/CD with GitHub Actions.

---

## 📦 Services Overview

| Service                 | Port | Description |
|------------------------|------|-------------|
| agent-service          | 5001 | Manages agent records |
| integration-service    | 5002 | Receives sales data |
| notification-service   | 5003 | Sends alerts when targets are hit |
| aggregator-service     | 5004 | Aggregates data for reporting |
| redshift-analytics-service | 5005 | Syncs aggregated data to Redshift |

---

## 🔧 Prerequisites

- Google Cloud Project with GKE enabled
- MongoDB Atlas URI
- AWS Redshift cluster
- GitHub Repository with Secrets configured:
  - `MONGO_URI`
  - `REDSHIFT_HOST`, `REDSHIFT_PORT`, `REDSHIFT_USER`, `REDSHIFT_PASSWORD`, `REDSHIFT_DBNAME`
  - `GCP_SA_KEY`, `GCP_PROJECT_ID`

---

## 🛠️ CI/CD Deployment Steps

1. Push or merge changes to the `main` branch.
2. GitHub Actions will:
   - Build and push Docker images
   - Deploy to GKE using manifests
   - Inject secrets into Kubernetes
   - Run Postman collection for integration testing
   - Validate Redshift data ingestion

You can monitor the pipeline from the **Actions** tab on GitHub.

---

## 🌐 Accessing the Application

Once deployed, access the services via:

```
http://<INGRESS-IP>/agent
http://<INGRESS-IP>/sales
http://<INGRESS-IP>/notification/check_target/AGENT001
http://<INGRESS-IP>/aggregation/best_teams
http://<INGRESS-IP>/aggregation/best_products
http://<INGRESS-IP>/aggregation/branch_performance
http://<INGRESS-IP>/sync/best_teams
http://<INGRESS-IP>/sync/products_achieving_targets
http://<INGRESS-IP>/sync/branch_wise_performance
```

---

## 🧪 Testing Instructions

1. Import `postman_collection_updated.json` into Postman.
2. Use environment `{baseUrl}` with your Ingress IP.
3. Run the collection to validate sales creation, retrieval, and syncing.

---

## 🚨 Troubleshooting

| Issue | Fix |
|-------|-----|
| MongoDB connection error | Ensure `MONGO_URI` is valid and whitelisted |
| Redshift sync failure | Verify Redshift credentials and DB accessibility |
| Pod CrashLoopBackOff | Check container logs via `kubectl logs <pod-name>` |

---

## ✅ Health Check (Optional)

You may implement `/health` endpoints in each service returning:
```json
{"status": "ok", "service": "agent-service"}
```

---

## 📊 Observability (Optional Bonus)

To earn extra marks:
- Enable Prometheus metrics scraping
- Use Kubernetes probes: `livenessProbe` and `readinessProbe`

---

## 🔐 Security Notes

- All secrets injected via GitHub Vault
- No hardcoded credentials in code or manifests
- Communication between services is internal (ClusterIP)

---

## 📞 Support

Maintainer: MoonInsurance DevOps Team  
Contact: rajthawijesinghe74@gmail.com

