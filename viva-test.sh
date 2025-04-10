



cd agent-service
eval $(minikube docker-env)
docker build -t agent-service:latest -f docker/Dockerfile .
kubectl apply -f manifests/deployment.yaml
kubectl apply -f manifests/service.yaml
cd ..
cd aggregator-service
eval $(minikube docker-env)
docker build -t aggregator-service:latest -f docker/Dockerfile .
kubectl apply -f manifests/deployment.yaml
kubectl apply -f manifests/service.yaml
cd ..
cd integration-service
eval $(minikube docker-env)
docker build -t integration-service:latest -f docker/Dockerfile .
kubectl apply -f manifests/deployment.yaml
kubectl apply -f manifests/service.yaml
cd ..
cd notification-service
eval $(minikube docker-env)
docker build -t notification-service:latest -f docker/Dockerfile .
kubectl apply -f manifests/deployment.yaml
kubectl apply -f manifests/service.yaml
cd ..
cd redshift-analytics-service
eval $(minikube docker-env)
docker build -t redshift-analytics-service:latest -f docker/Dockerfile .
kubectl apply -f manifests/deployment.yaml
kubectl apply -f manifests/service.yaml
cd ..

# Troubleshooting Steps

sudo lsof -ti :5001 | xargs kill -9
sudo lsof -ti :5002 | xargs kill -9
sudo lsof -ti :5003 | xargs kill -9
sudo lsof -ti :5004 | xargs kill -9
sudo lsof -ti :5005 | xargs kill -9

kubectl apply -f agent-service/manifests/deployment.yaml
kubectl apply -f integration-service/manifests/deployment.yaml
kubectl apply -f notification-service/manifests/deployment.yaml
kubectl apply -f aggregator-service/manifests/deployment.yaml
kubectl apply -f redshift-analytics-service/manifests/deployment.yaml

kubectl apply -f agent-service/manifests/service.yaml
kubectl apply -f integration-service/manifests/service.yaml
kubectl apply -f notification-service/manifests/service.yaml
kubectl apply -f aggregator-service/manifests/service.yaml
kubectl apply -f redshift-analytics-service/manifests/service.yaml

kubectl port-forward svc/agent-service 5001:5001
kubectl port-forward svc/integration-service 5002:5002
kubectl port-forward svc/notification-service 5003:5003
kubectl port-forward svc/aggregator-service 5004:5004
kubectl port-forward svc/redshift-analytics-service 5005:5005
