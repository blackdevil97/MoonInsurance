#!/bin/bash

set -e  # 🚨 Important: Stop script if any command fails

echo "🚀 Starting MoonInsurance full deployment..."

# Step 1: Apply Namespace
echo "📦 Creating namespace..."
kubectl apply -f namespace.yaml

# Step 2: Apply Kubernetes manifests for all services
echo "📦 Applying Kubernetes manifests..."

kubectl apply -f agent-service/manifests/deployment.yaml
kubectl apply -f integration-service/manifests/deployment.yaml
kubectl apply -f notification-service/manifests/deployment.yaml
kubectl apply -f aggregator-service/manifests/deployment.yaml
kubectl apply -f redshift-analytics-service/manifests/deployment.yaml
kubectl apply -f ingress.yaml

# Step 3: Wait for pods to be ready
echo "⏳ Waiting for all pods to be ready..."
kubectl wait --for=condition=available --timeout=300s deployment --all -n mooninsurance

# Step 4: Print pods status
echo "✅ Current Pods Status:"
kubectl get pods -n mooninsurance

# Step 5: Get Minikube IP
MINIKUBE_IP=$(minikube ip)
echo "🌐 Minikube IP: $MINIKUBE_IP"

# Step 6: Show useful endpoints
echo "🔗 Useful Endpoints:"
echo "Agent Service:          http://$MINIKUBE_IP/agent-service/health"
echo "Integration Service:    http://$MINIKUBE_IP/integration-service/health"
echo "Notification Service:   http://$MINIKUBE_IP/notification-service/health"
echo "Aggregator Service:     http://$MINIKUBE_IP/aggregator-service/health"
echo "Redshift Analytics:     http://$MINIKUBE_IP/redshift-analytics-service/health"

echo ""
echo "🧩 Quick test commands:"
echo "curl http://$MINIKUBE_IP/agent-service/health"
echo "curl http://$MINIKUBE_IP/integration-service/health"
echo "curl http://$MINIKUBE_IP/notification-service/health"
echo "curl http://$MINIKUBE_IP/aggregator-service/health"
echo "curl http://$MINIKUBE_IP/redshift-analytics-service/health"

echo ""
echo "✅ Deployment completed successfully!"
