#!/bin/bash

podman stop $(podman ps --filter "ancestor=hr_zonal:latest" --format "{{.ID}}") 2>/dev/null \
&& echo "✅ Container stopped" \
|| echo "❌ No container found or error stopping"