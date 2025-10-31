#!/bin/bash

check_kuksa_broker() {
    echo "🔍 Checking Kuksa Databroker..."
    if nc -z localhost 55555 2>/dev/null; then
        echo "✅ Kuksa Databroker is running on port 55555"
        return 0
    else
        echo "❌ Kuksa Databroker is not responding on port 55555"
        if podman ps --format "{{.Names}}" | grep -q "kuksa-broker"; then
            echo "📋 Checking Kuksa container logs..."
            podman logs --tail 10 kuksa-broker 2>&1 | grep -i error
            if [ $? -eq 0 ]; then
                echo "⚠️  Found errors in Kuksa container logs"
            else
                echo "✅ No errors in recent Kuksa container logs"
            fi
        fi
        return 1
    fi
}

check_mosquitto() {
    echo "🔍 Checking Mosquitto..."
    if nc -z localhost 1883 2>/dev/null; then
        echo "✅ Mosquitto is running on port 1883"
        return 0
    else
        echo "❌ Mosquitto is not responding on port 1883"
        if podman ps --format "{{.Names}}" | grep -q "mosquitto-broker"; then
            echo "📋 Checking Mosquitto container logs..."
            podman logs --tail 10 mosquitto-broker 2>&1 | grep -i error
            if [ $? -eq 0 ]; then
                echo "⚠️  Found errors in Mosquitto container logs"
            else
                echo "✅ No errors in recent Mosquitto container logs"
            fi
        fi
        return 1
    fi
}

check_services() {
    echo "🏥 Running comprehensive health check..."
    check_kuksa_broker
    local kuksa_status=$?
    
    check_mosquitto
    local mosquitto_status=$?
    
    if [ $kuksa_status -eq 0 ] && [ $mosquitto_status -eq 0 ]; then
        echo "✅ All services are running properly"
        return 0
    else
        echo "❌ Some services are not running properly"
        return 1
    fi
}

case "${1:-}" in
    "kuksa")
        check_kuksa_broker
        ;;
    "mosquitto")
        check_mosquitto
        ;;
    *)
        check_services
        ;;
esac