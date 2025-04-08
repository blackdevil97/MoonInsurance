
# MoonInsurance Project 🚀

MoonInsurance is a microservices-based insurance sales data platform designed for efficient data management, notification, and analytics reporting. This project mirrors professional cloud-native architectures and integrates services like MongoDB Atlas, AWS Redshift, and Kubernetes, with CI/CD pipelines on GitHub Actions.

## Project Architecture

- **AgentService**: Manages insurance agent profiles.
- **IntegrationService**: Collects sales data from core systems.
- **NotificationService**: Sends notifications based on sales achievements.
- **AggregatorService**: Aggregates sales data for analysis.
- **RedshiftAnalyticsService**: Syncs data to AWS Redshift for advanced analytics and dashboards.

## Technologies Used

- Python Flask Microservices
- MongoDB Atlas
- AWS Redshift
- Docker
- Kubernetes (Minikube)
- GitHub Actions CI/CD
- GitHub Vault for secrets management

## Project Structure

```
MoonInsurance
├── AgentService
├── IntegrationService
├── NotificationService
├── AggregatorService
├── RedshiftAnalyticsService
├── .github/workflows/ci-cd.yaml
├── ingress.yaml
├── README.md
├── runbook.md
└── Test.py
```

## Setup Instructions

1. Clone this repository.
2. Add secrets to GitHub Vault:
   - MONGO_URI
   - REDSHIFT_HOST
   - REDSHIFT_PORT
   - REDSHIFT_USER
   - REDSHIFT_PASSWORD
   - REDSHIFT_DBNAME
3. Push to main branch to trigger CI/CD.
4. Services deployed on Minikube, validated via Test.py.

## Testing

```bash
python Test.py
```

## CI/CD Pipeline

- Automated build and deploy with GitHub Actions.
- Secrets injected securely from GitHub Vault.
- Minikube used for Kubernetes environment.

## Future Improvements

- Implement automated scaling.
- Enhance monitoring and logging.
- Add security hardening for production use.

## Maintained by
Rajitha Wijesinghe