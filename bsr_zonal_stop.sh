#!/bin/bash


IMAGE_NAME="${1:-zonal_app}"

echo "Stopping zonal application: $IMAGE_NAME"

sudo podman stop $(sudo podman ps --filter "ancestor=$IMAGE_NAME" --format "{{.ID}}") 2>/dev/null

sudo podman rm $(sudo podman ps -a --filter "ancestor=$IMAGE_NAME" --filter "status=exited" --format "{{.ID}}") 2>/dev/null

echo "Zonal application stopped"