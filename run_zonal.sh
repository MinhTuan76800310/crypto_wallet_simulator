#!/bin/bash

DEVICE_ID="04d8:0053"

DEVICE_INFO=$(lsusb | grep "$DEVICE_ID")

if [ -z "$DEVICE_INFO" ]; then
    echo "Not found device: $DEVICE_ID"
    exit 1
fi

BUS=$(echo "$DEVICE_INFO" | awk '{print $2}')
DEVICE_NUM=$(echo "$DEVICE_INFO" | awk '{print $4}' | sed 's/://')

DEVICE_PATH="/dev/bus/usb/$BUS/$DEVICE_NUM"

if [ ! -e "$DEVICE_PATH" ]; then
    echo "Error: Device path not found $DEVICE_PATH"
    exit 1
fi

echo "Grantting permissions 777 for device: $DEVICE_PATH"
sudo chmod 777 "$DEVICE_PATH"

if [ $? -eq 0 ]; then
    echo "✅ Successfully granted permissions for $DEVICE_PATH"
else
    echo "❌ Error granting permissions"
    exit 1
fi

# Run container
echo "🚀 Starting container..."

podman run -it --rm \
    --network=host  \
    --device="$DEVICE_PATH" \
    -e LOG_LEVEL=DEBUG   \
    -v "$(pwd)/net_conf.ini:/dist/config/dbc_feeder.ini:Z"   \
    -v "$(pwd)/vss_dbc.json:/config/vss_dbc.json:Z" \
    -v "$(pwd)/vss_dbc.json:/dist/vss_dbc.json:Z" \
    -v "$(pwd)/dbc_default_values.json:/dist/dbc_default_values.json:Z" \
    -v "$(pwd)/HnR.dbc:/dist/HnR.dbc:Z"  ghcr.io/pmt563/hr_zonal/hr-zonal:latest \
    --no-val2dbc

if [ $? -eq 0 ]; then
    echo "✅ Successfully started container Podman"
else
    echo "❌ Error starting container Podman"
    exit 1
fi