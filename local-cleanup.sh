#!/bin/bash

echo "🧹 Cleaning up local environment..."

# Stop Minikube if running
if minikube status | grep -q "Running"; then
    echo "⏳ Stopping Minikube cluster..."
    minikube stop
    echo "✅ Minikube stopped."
else
    echo "✅ Minikube is already stopped."
fi

# Optional: Clean up Docker system
echo "🐳 Cleaning up Docker system (optional)..."
docker system prune -af --volumes

echo "🎉 Local environment is clean."
