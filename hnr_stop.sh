#!/bin/bash

echo "🛑 Starting graceful shutdown of all services..."

sudo podman stop -t 10 $(sudo podman ps -q --filter "ancestor=docker.io/autonxtai/hnr-fullapp:1.0") 2>/dev/null
sudo podman rm $(sudo podman ps -aq --filter "ancestor=docker.io/autonxtai/hnr-fullapp:1.0") 2>/dev/null
echo "✅ Main application container stopped" 

sudo podman stop -t 10 $(sudo podman ps -q --filter "ancestor=ghcr.io/eclipse-kuksa/kuksa-databroker:main") 2>/dev/null
sudo podman rm $(sudo podman ps -aq --filter "ancestor=ghcr.io/eclipse-kuksa/kuksa-databroker:main") 2>/dev/null
echo "✅ Kuksa Databroker container stopped"

sudo podman stop -t 10 $(sudo podman ps -q --filter "ancestor=docker.io/eclipse-mosquitto:2") 2>/dev/null
sudo podman rm $(sudo podman ps -aq --filter "ancestor=docker.io/eclipse-mosquitto:2") 2>/dev/null
echo "✅ Mosquitto container stopped"

echo "✅ All services are shutdown successfully!"

echo "🛑 Starting graceful shutdown of all services..."

