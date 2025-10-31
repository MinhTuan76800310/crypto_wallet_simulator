#!/bin/bash

# Usage: sudo ./run.sh <image-name> [brokerip:port]
# Example: sudo ./run.sh zonal_app 192.168.0.3:55556

VID="04d8"
PID="0053"

while true; do
    read -p "Enter loopback value (0 or 1): " loopback_value
    if [[ "$loopback_value" == "0" || "$loopback_value" == "1" ]]; then
        break
    else
        echo "Invalid input. Please enter 0 or 1."
    fi
done

# Find the line in lsusb that matches the device
line=$(lsusb | grep "${VID}:${PID}")

if [ -n "$line" ]; then
    BUS=$(echo "$line" | awk '{print $2}')
    DEV=$(echo "$line" | awk '{print $4}' | sed 's/://')

    # Format the full path
    USB_DEV="/dev/bus/usb/${BUS}/${DEV}"

    echo "Found USB device at $USB_DEV"
else
    echo "USB device ${VID}:${PID} not found."
    exit 1
fi

if [ $# -lt 1 ] || [ $# -gt 2 ]; then
  echo "Usage: sudo $0 <image-name> [brokerip:port]"
  exit 1
fi

IMAGE_NAME=$1
BROKER_ARG=${2:-192.168.1.1:55555}

podman run --rm -it --device=$USB_DEV "$IMAGE_NAME"  -loopback="$loopback_value" "$BROKER_ARG"