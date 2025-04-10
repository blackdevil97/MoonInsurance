if ! pgrep -f "minikube tunnel" > /dev/null; then
  echo "🚀 Starting Minikube tunnel..."
  nohup minikube tunnel > /dev/null 2>&1 &
  echo "✅ Minikube tunnel started in background!"
else
  echo "✅ Minikube tunnel is already running."
fi
