#!/bin/bash

echo "🔍 Auto-detecting MongoDB Pod..."

# Get MongoDB pod name dynamically
MONGO_POD=$(kubectl get pods --all-namespaces -o jsonpath="{range .items[?(@.metadata.labels.app=='mongo')]}{.metadata.name}{'\n'}{end}")

if [ -z "$MONGO_POD" ]; then
    echo "❌ MongoDB Pod not found. Please ensure MongoDB is deployed."
    exit 1
fi

# Get namespace of MongoDB pod
MONGO_NAMESPACE=$(kubectl get pods --all-namespaces -o jsonpath="{range .items[?(@.metadata.labels.app=='mongo')]}{.metadata.namespace}{'\n'}{end}")

echo "✅ MongoDB Pod: $MONGO_POD"
echo "✅ Namespace: $MONGO_NAMESPACE"

echo "📡 Connecting to MongoDB..."
kubectl exec -it -n "$MONGO_NAMESPACE" "$MONGO_POD" -- mongosh
