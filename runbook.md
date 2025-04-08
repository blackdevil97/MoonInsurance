
# MoonInsurance Project - Runbook 📖

## Overview

MoonInsurance is a microservices project simulating an insurance sales platform with agent management, sales data integration, notifications, and analytics reporting using AWS Redshift.

## Services Overview

- **AgentService**: CRUD operations for insurance agents.
- **IntegrationService**: Receives and records sales transactions.
- **NotificationService**: Alerts when sales targets are met.
- **AggregatorService**: Provides analytics on sales data.
- **RedshiftAnalyticsService**: Exports analytics data to AWS Redshift.

## Pre-requisites

- AWS Account
- MongoDB Atlas Cluster
- GitHub repository with Secrets configured
- Terraform for Redshift provisioning

## Deployment Steps

1. **Terraform Setup**
   - Navigate to `terraform/` directory.
   - Run:
     ```
     terraform init
     terraform apply
     ```

2. **Add GitHub Secrets**
   - MONGO_URI
   - REDSHIFT_HOST
   - REDSHIFT_PORT
   - REDSHIFT_USER
   - REDSHIFT_PASSWORD
   - REDSHIFT_DBNAME

3. **Push to Repository**
   - GitHub Actions will auto-deploy services to Minikube.

4. **Validate Services**
   - Access services via Ingress: `mooninsurance.local`
   - Run integration tests:
     ```
     python test.py
     ```

## CI/CD Pipeline Details

- **Trigger**: Push to `main` branch.
- **Steps**:
  - Install dependencies
  - Start Minikube
  - Build Docker images
  - Deploy to Kubernetes
  - Run tests

## Ingress Configuration

Services exposed via `mooninsurance.local` domain for testing.

## Secrets Management

All sensitive data is injected via GitHub Actions Vault.

## Support

For any issues, contact:
Rajitha Wijesinghe