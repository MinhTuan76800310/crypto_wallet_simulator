#!/bin/bash

WORKSPACE_DIR=$(pwd)
MAX_WAIT_TIME=60
CHECK_INTERVAL=3

check_success() {
    if [ $? -eq 0 ]; then
        echo "✅ $1"
    else
        echo "❌ Failed: $1"
        exit 1
    fi
}

is_port_available() {
    local port=$1
    if nc -z localhost "$port" 2>/dev/null; then
        return 0  
    else
        return 1  
    fi
}

wait_for_service() {
    local service_name="$1"
    local port="$2"
    local counter=0
    
    echo "⏳ Waiting for $service_name on port $port..."
    
    while [ $counter -lt $MAX_WAIT_TIME ]; do
        if nc -z localhost "$port" 2>/dev/null; then
            echo "✅ $service_name is ready!"
            return 0
        fi
        sleep $CHECK_INTERVAL
        counter=$((counter + CHECK_INTERVAL))
        echo "   Still waiting for $service_name... ($counter/$MAX_WAIT_TIME seconds)"
    done
    
    echo "❌ Timeout waiting for $service_name after $MAX_WAIT_TIME seconds"
    return 1
}

check_kuksa_broker() {
    echo "🔍 Checking Kuksa Databroker..."
    if nc -z localhost 55555 2>/dev/null; then
        echo "✅ Kuksa Databroker is running on port 55555"
        return 0
    else
        echo "❌ Kuksa Databroker is not responding on port 55555"
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
        return 1
    fi
}

main() {
    echo "--------------- Starting ------------------------"
    
    if is_port_available 55555; then
        echo "⚠️  Port 55555 is already in use, skipping Kuksa Databroker startup"
    else
        echo "🔧 Starting Kuksa Databroker..."
        cd dependency/kuksa_databroker
        ./linux_run.sh &
        check_success "Kuksa Databroker process started"
    fi

    if is_port_available 1883; then
        echo "⚠️  Port 1883 is already in use, skipping Mosquitto startup"
    else
        echo "🔧 Starting Mosquitto..."
        cd "$WORKSPACE_DIR/dependency/mosquitto"
        ./linux_run.sh &
        check_success "Mosquitto process started"
    fi

    cd "$WORKSPACE_DIR"
    
    echo "⏳ Waiting for services to be ready..."
    
    if ! wait_for_service "Mosquitto" 1883; then
        echo "❌ Mosquitto failed to start properly or is not accessible"
        check_mosquitto
        exit 1
    fi
    
    if ! wait_for_service "Kuksa Databroker" 55555; then
        echo "❌ Kuksa Databroker failed to start properly or is not accessible"
        check_kuksa_broker
        exit 1
    fi
    
    echo "Extra time to fully initialize..."
    sleep 8
    
    echo "Running final health check..."
    check_mosquitto
    check_kuksa_broker
    
    echo "All dependencies are ready! Starting main application..."
    
    sudo podman run -it --rm --network=host \
        --device /dev/ttyACM0 \
        --device=/dev/video4:/dev/video0 \
        -v "$PWD/filter_noise_tracker.cfg:/app/filter_noise_tracker.cfg:ro" \
        --mount type=bind,source=$PWD/camera_app/config,target=/app/config,ro=true \
        docker.io/autonxtai/hnr-fullapp:1.0
    
    check_success "Main application container execution completed"
    echo "✅ All services started and executed successfully!"
}

main