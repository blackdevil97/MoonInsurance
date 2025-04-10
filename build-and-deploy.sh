services=("agent-service" "aggregator-service" "integration-service" "notification-service" "redshift-analytics-service")

for service in "${services[@]}"
do
  echo "🚀 Processing $service"
  cd $service
  eval $(minikube docker-env)
  docker build -t $service:latest -f docker/Dockerfile .
  kubectl apply -f manifests/deployment.yaml
  kubectl apply -f manifests/service.yaml
  cd ..
done

