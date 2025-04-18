
# 🌙 Moon Insurance - Cloud Microservices Project

This project implements the **Moon Insurance - Moon Agent Tracker** system using modern cloud-native architecture and microservices deployed on Kubernetes.

## 🚀 Project Purpose

> To build an enterprise-grade cloud-native microservices solution for Moon Insurance, allowing them to:
> - Track agent performances.
> - Ingest and aggregate sales data.
> - Generate real-time insights.
> - Deploy with zero downtime using Blue-Green deployment strategy.

---

## 🧩 Microservices Overview

| Service               | Description |
|----------------------|-------------|
| **Agent Service**     | Manages agent profiles and product allocations. |
| **Integration Service** | Ingests and stores real-time sales data from agents. |
| **Notification Service** | Simulated notifications when sales targets are reached. |
| **Aggregator Service** | Aggregates sales data for branch, product, and team performance insights. |

---

## 🛠️ Technologies Used

- **Python Flask** — Lightweight microservices framework
- **AWS DynamoDB** — NoSQL database for agents and sales data
- **AWS ECR** — Docker image repository
- **AWS IAM** — Secure access controls
- **Kubernetes (K8s)** — Container orchestration platform
- **GitHub Actions** — CI/CD pipeline with Blue-Green deployment
- **Docker** — Containerization for microservices
- **Boto3** — AWS SDK for Python

---

## ⚙️ Project Features

- ✅ Microservices communication inside Kubernetes
- ✅ Full CI/CD pipeline with zero-downtime Blue-Green deployment
- ✅ Automated health checks and rollback in CI/CD
- ✅ Bulk data generation and insertion to DynamoDB
- ✅ Environment variable configuration for AWS credentials and table names
- ✅ Professional folder structure and clear separation of concerns
- ✅ GitHub Secrets for secure key management

---

## 🚀 Deployment Guide

> ✅ Refer to the included [runbook.md](runbook.md) for step-by-step deployment instructions.

### Quick Start (after setup):
\`\`\`bash
# 1. Create AWS resources (DynamoDB tables)
python scripts/create_dynamodb_tables.py

# 2. Generate bulk demo data
python scripts/generate_bulk_data.py

# 3. Insert data into DynamoDB
python scripts/insert_data.py

# 4. Verify inserted data
python scripts/verify_dynamodb_data.py

# 5. Deploy Kubernetes services
bash deploy.sh

# 6. Trigger CI/CD pipeline via GitHub Actions (push to main branch)
\`\`\`

---

## 🧩 Architecture Diagram

> (Include your architecture PNG or draw.io file reference here)

---

## 📂 Project Structure

\`\`\`
.github/workflows/          # CI/CD pipeline
agent-service/              # Agent microservice
integration-service/        # Integration microservice
notification-service/       # Notification microservice
aggregator-service/         # Aggregator microservice
k8s/                        # Kubernetes YAMLs
scripts/                    # Setup & data scripts
tests/                      # Health check script
\`\`\`

---

## 👨‍💻 Author

- **Rajitha Wijesinghe**

---

## ✅ Notes

- ✅ AWS credentials and sensitive data are managed via **GitHub Secrets** and **environment variables**.
- ✅ Blue-Green deployments ensure zero downtime.
- ✅ Health checks automatically verify deployment success.

---
