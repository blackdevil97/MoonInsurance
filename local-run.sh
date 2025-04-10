#!/bin/bash

echo "🚀 Starting local development environment for MoonInsurance"

# Step 0: Check if Minikube is running
if minikube status | grep -q "Running"; then
    echo "✅ Minikube is already running."
else
    echo "⏳ Minikube is not running. Starting Minikube..."
    minikube start --driver=docker
    minikube addons enable ingress
    echo "✅ Minikube started."
fi

# Step 1: Build Docker images inside Minikube
echo "🔨 Building Docker images..."
eval $(minikube docker-env)

services=("AgentService" "IntegrationService" "NotificationService" "AggregatorService" "RedshiftAnalyticsService")

for service in "${services[@]}"
do
  echo "➡️ Building $service..."
  lowercase_service=$(echo "$service" | tr '[:upper:]' '[:lower:]')
  docker build -t "${lowercase_service}:latest" -f "${service}/docker/Dockerfile" "${service}"
done
echo "✅ Docker images built successfully."

# Step 2: Apply Kubernetes manifests
echo "📦 Applying Kubernetes manifests..."
for service in "${services[@]}"
do
  echo "➡️ Deploying $service..."
  kubectl apply -f "${service}/manifests/"
done

kubectl apply -f ingress.yaml
echo "✅ Kubernetes manifests applied."

# Step 3: Port forwarding
echo "🌐 Setting up port forwarding for services..."

kubectl port-forward svc/agent-service 8080:5001 &
AGENT_PID=$!

kubectl port-forward svc/integration-service 8081:5002 &
INTEGRATION_PID=$!

kubectl port-forward svc/notification-service 8082:5003 &
NOTIFICATION_PID=$!

kubectl port-forward svc/aggregator-service 8083:5004 &
AGGREGATOR_PID=$!

kubectl port-forward svc/redshift-analytics-service 8084:5005 &
REDSHIFT_PID=$!

sleep 5 # Wait for port-forwarding to stabilize

echo "✅ Port forwarding established."
echo "🔗 Access your services:"
echo "Agent Service:               http://localhost:8080/agent"
echo "Integration Service:         http://localhost:8081/sales"
echo "Notification Service:        http://localhost:8082/notification/check_target?target=1"
echo "Aggregator Service:          http://localhost:8083/aggregation/best_teams"
echo "Redshift Analytics Service:  http://localhost:8084/sync/appointments_per_doctor"

# Step 4: Run tests automatically
echo ""
echo "🧪 Running test.py to validate services..."
if python3 test.py; then
    echo "🎉✅ All tests passed successfully!"
else
    echo "❌ Some tests failed. Check the output above ☝️"
fi

# Step 5: Auto-kill port-forwards
echo ""
echo "🧹 Cleaning up port-forwards..."
kill $AGENT_PID $INTEGRATION_PID $NOTIFICATION_PID $AGGREGATOR_PID $REDSHIFT_PID

echo "✅ Port-forwards terminated."
echo "🎉 Local environment run completed."
