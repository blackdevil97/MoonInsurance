
# 🚀 Deployment Runbook - Moon Insurance Project

This runbook guides you through the deployment process for the Moon Insurance Cloud Microservices project.

---

## ✅ Prerequisites

- AWS Account (ECR + DynamoDB setup)
- AWS CLI configured locally
- Docker installed
- Kubernetes cluster running
- kubectl configured for your cluster
- GitHub repository configured with Secrets for CI/CD
- Python virtual environment (optional)

---

## 🌟 Step 1: Build Docker Images Locally (Optional for testing)

> Optional: If using GitHub Actions CI/CD, this is automated.

```bash
docker build -t agent-service ./agent-service
docker build -t integration-service ./integration-service
docker build -t notification-service ./notification-service
docker build -t aggregator-service ./aggregator-service
```

---

## 🌟 Step 2: Push Images to AWS ECR

1. **Login to ECR:**

```bash
aws ecr get-login-password --region ap-southeast-1 | docker login --username AWS --password-stdin <your_aws_account_id>.dkr.ecr.ap-southeast-1.amazonaws.com
```

2. **Tag and push each service image:**

```bash
docker tag agent-service:latest <your_aws_account_id>.dkr.ecr.ap-southeast-1.amazonaws.com/agent-service:latest
docker push <your_aws_account_id>.dkr.ecr.ap-southeast-1.amazonaws.com/agent-service:latest

docker tag integration-service:latest <your_aws_account_id>.dkr.ecr.ap-southeast-1.amazonaws.com/integration-service:latest
docker push <your_aws_account_id>.dkr.ecr.ap-southeast-1.amazonaws.com/integration-service:latest

docker tag notification-service:latest <your_aws_account_id>.dkr.ecr.ap-southeast-1.amazonaws.com/notification-service:latest
docker push <your_aws_account_id>.dkr.ecr.ap-southeast-1.amazonaws.com/notification-service:latest

docker tag aggregator-service:latest <your_aws_account_id>.dkr.ecr.ap-southeast-1.amazonaws.com/aggregator-service:latest
docker push <your_aws_account_id>.dkr.ecr.ap-southeast-1.amazonaws.com/aggregator-service:latest
```

> ✅ **Note:** Your CI/CD pipeline will also handle this automatically!

---

## 🌟 Step 3: Create DynamoDB Tables

Before running the services, create the required DynamoDB tables:

```bash
python scripts/create_dynamodb_tables.py
```

Optional: Insert sample data

```bash
python scripts/generate_bulk_data.py
python scripts/insert_data.py
python scripts/verify_dynamodb_data.py
```

---

## 🌟 Step 4: Deploy to Kubernetes Cluster

Either use **GitHub Actions CI/CD** (recommended) or apply manifests manually:

```bash
kubectl apply -f k8s/
```

> ✅ Tip: Use the optional `deploy.sh` script for quick deployment!

---

## 🌟 Step 5: Verify Deployment

Check pods and services:

```bash
kubectl get pods
kubectl get services
```

---

## 🌟 Step 6: Test Microservices

Forward ports for local testing:

```bash
kubectl port-forward service/agent-service 5001:5001
kubectl port-forward service/integration-service 5002:5002
kubectl port-forward service/notification-service 5003:5003
kubectl port-forward service/aggregator-service 5004:5004
```

Test endpoints:

| Service | Endpoint |
|---------|-----------|
| Agent Service | http://localhost:5001/agent |
| Integration Service | http://localhost:5002/sales |
| Notification Service | http://localhost:5003/notify |
| Aggregator Service | http://localhost:5004/aggregate |

---

## 🌟 Step 7: CI/CD Pipeline (Blue-Green Deployment)

Your GitHub Actions pipeline:
- Builds Docker images
- Pushes to AWS ECR
- Deploys Blue-Green to Kubernetes
- Performs automated health checks
- Switches traffic to Green if healthy

> ✅ Push changes to `main` branch to trigger CI/CD!

---

## 🎉 Congratulations!

Your project is successfully deployed and running on Kubernetes! 🚀

---
