#!/bin/bash

echo "🚀 Starting MoonInsurance full local automation!"

# Step 1: Check and update /etc/hosts
echo "🔍 Checking /etc/hosts for mooninsurance.local..."
MINIKUBE_IP=$(minikube ip || echo "192.168.49.2")

if grep -q "mooninsurance.local" /etc/hosts; then
  echo "✅ /etc/hosts is already configured."
else
  echo "⚠️ /etc/hosts entry missing. Adding it now (requires sudo)..."
  echo "$MINIKUBE_IP mooninsurance.local" | sudo tee -a /etc/hosts > /dev/null
  echo "✅ /etc/hosts updated!"
fi

# Step 2: Clean up environment
echo "🧹 Cleaning up local environment..."
./local-cleanup.sh || echo "⚠️ local-cleanup.sh encountered an issue but continuing..."

# Step 3: Run setup
echo "🚀 Starting full setup..."
./local-setup.sh || { echo "❌ Setup failed. Exiting."; exit 1; }

# Step 4: Run tests automatically
echo "🧪 Running automated tests..."
if [ -f "venv/bin/activate" ]; then
  source venv/bin/activate
  python test.py || echo "⚠️ Tests failed, check output above."
  deactivate
else
  echo "⚠️ Virtual environment not found. Skipping tests."
fi

# Step 5: Launch Minikube dashboard
echo "🖥️ Launching Minikube dashboard..."
minikube addons enable metrics-server
minikube dashboard &>/dev/null &

# Step 6: Open mooninsurance.local in browser
echo "🌐 Opening mooninsurance.local in browser..."
sleep 3
open "http://mooninsurance.local" || xdg-open "http://mooninsurance.local" || echo "⚠️ Could not open browser automatically."

# Step 7: Auto-detect MongoDB pod and connect
echo "🍃 Checking for MongoDB pod..."
MONGO_POD=$(kubectl get pods --all-namespaces -l app=mongodb -o jsonpath="{.items[0].metadata.name}" 2>/dev/null)

if [ -n "$MONGO_POD" ]; then
  echo "✅ MongoDB pod detected: $MONGO_POD"
  echo "🔌 Connecting to MongoDB shell..."
  kubectl exec -it "$MONGO_POD" -- mongo || echo "⚠️ MongoDB shell failed to connect."
else
  echo "⚠️ MongoDB pod not found. Skipping MongoDB access."
fi

echo "🎉 All done! MoonInsurance local environment is ready 🚀"
