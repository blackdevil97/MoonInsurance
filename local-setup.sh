#!/bin/bash

echo "🚀 Starting full local MoonInsurance setup..."

# Check Minikube status
echo "📦 Checking Minikube status..."
if minikube status | grep -q "Running"; then
  echo "✅ Minikube already running."
else
  echo "⏳ Starting Minikube with Docker driver and ingress..."
  minikube start --driver=docker --addons=ingress,ingress-dns --memory=4096 --cpus=2
fi

# Get Minikube IP
MINIKUBE_IP=$(minikube ip)
echo "🌐 Minikube IP: $MINIKUBE_IP"
echo "💡 Ensure this is in your /etc/hosts file:"
echo "$MINIKUBE_IP mooninsurance.local"

# Build Docker images inside Minikube
echo "🐳 Building Docker images inside Minikube..."
eval $(minikube docker-env)

services=(
  agent-service
  integration-service
  notification-service
  aggregator-service
  redshift-analytics-service
)

for service in "${services[@]}"; do
  echo "➡️ Building $service..."
  docker build -t "$service:latest" -f "$service/docker/Dockerfile" "$service"
done

echo "✅ Docker images built."

# Apply Kubernetes manifests
echo "📦 Applying Kubernetes manifests..."
for service in "${services[@]}"; do
  echo "➡️ Deploying $service..."
  kubectl apply -f "$service/manifests/"
done

# Apply ingress
echo "🌐 Applying Ingress..."
kubectl apply -f ingress.yaml

echo "🎉 Setup complete! Access your services via:"
echo "🌐 Agent Service:               http://mooninsurance.local/agent"
echo "🌐 Integration Service:         http://mooninsurance.local/sales"
echo "🌐 Notification Service:        http://mooninsurance.local/notification/check_target?target=1"
echo "🌐 Aggregator Service:          http://mooninsurance.local/aggregation/best_teams"
echo "🌐 Redshift Analytics Service:  http://mooninsurance.local/sync/appointments_per_doctor"

echo ""
echo "💡 Ensure /etc/hosts has:"
echo "$MINIKUBE_IP mooninsurance.local"
echo ""
echo "🧪 Optionally, run your test script manually: source venv/bin/activate && python test.py"
