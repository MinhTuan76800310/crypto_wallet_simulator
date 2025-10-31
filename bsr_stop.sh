#!/bin/bash

echo "🛑 Safely shutting down Baby Safety Reminder App..."

podman stop baby_safety_reminder 2>/dev/null
podman rm baby_safety_reminder 2>/dev/null

sudo podman stop $(sudo podman ps --filter "ancestor=docker.io/emtekthien/deskapp:ver8" --format "{{.ID}}") 2>/dev/null

pkill -f "python3 desk_app.py" 2>/dev/null
pkill -f "python.*main.py" 2>/dev/null

pkill -f "launch_vehicle_app.sh" 2>/dev/null
pkill -f "launch_podman_OCS_app.sh" 2>/dev/null

sleep 2

pkill -f "gnome-terminal.*Vehicle App" 2>/dev/null
pkill -f "gnome-terminal.*Podman OCS App" 2>/dev/null

export DISPLAY=:0

echo "✅ Application safely shut down"
