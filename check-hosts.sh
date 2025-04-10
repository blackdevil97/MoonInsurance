#!/bin/bash

HOST_ENTRY="192.168.49.2 mooninsurance.local"

if grep -q "$HOST_ENTRY" /etc/hosts; then
  echo "✅ /etc/hosts is already configured for mooninsurance.local"
else
  echo "⚠️  /etc/hosts is missing entry for mooninsurance.local!"
  echo "💡 Please run: sudo nano /etc/hosts"
  echo "$HOST_ENTRY"
  exit 1
fi
