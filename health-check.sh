#!/bin/bash

echo "🔍 Checking Kubernetes pod health status..."

kubectl get pods -A

echo ""
echo "💡 Tip: All pods should be in 'Running' state."
