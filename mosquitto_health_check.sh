#!/bin/bash

check_mosquitto_container() {
    echo "🔍 Checking Mosquitto Container..."
    
    if ! podman ps --format "{{.Names}}" | grep -q "mosquitto-broker"; then
        echo "❌ Mosquitto container is not running"
        return 1
    fi
    
    echo "✅ Mosquitto container is running"
    
    if nc -z localhost 1883 2>/dev/null; then
        echo "✅ Mosquitto is listening on port 1883"
    else
        echo "❌ Mosquitto is not listening on port 1883"
        return 1
    fi
    
    echo "📋 Checking container logs..."
    podman logs --tail 10 mosquitto-broker 2>&1 | grep -i error
    if [ $? -eq 0 ]; then
        echo "⚠️  Found errors in container logs"
        return 1
    else
        echo "✅ No errors in recent container logs"
    fi
    
    return 0
}

check_mosquitto_container