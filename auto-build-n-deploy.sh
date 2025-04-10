eval $(minikube docker-env)

for SERVICE in agent-service aggregator-service integration-service notification-service redshift-analytics-service
do
  echo "🚀 Building and deploying $SERVICE ..."
  cd $SERVICE

  # Correct docker build command
  docker build -t $SERVICE:latest -f docker/Dockerfile .

  # Apply deployment and service
  kubectl apply -f manifests/deployment.yaml
  kubectl apply -f manifests/service.yaml

  cd ..
done

echo "✅ Build and deploy completed. Cleaning up old pods..."

# Clean up old pods to refresh deployments
kubectl delete pods --all -n default

echo "⏳ Waiting for pods to start..."
sleep 10

# Show pod status
kubectl get pods -n default

echo "✅ All services deployed! Test with:"
echo "curl -H \"Host: mooninsurance.local\" http://mooninsurance.local/agent"
