#!/bin/bash

cd /home/jetson/Projects/project_babysafetyreminder || exit 1

# ascii art character get at:
# https://patorjk.com/software/taag/#p=display&f=RubiFont&t=Type%20Something

cat <<'EOF'

 ▗▄▄▖▗▄▄▄▖▗▖  ▗▖▗▄▄▄▖▗▄▄▖  ▗▄▖ ▗▖       ▗▖  ▗▖▗▄▄▄▖▗▖ ▗▖▗▄▄▄▖ ▗▄▄▖▗▖   ▗▄▄▄▖     ▗▄▄▖ ▗▄▖ ▗▖  ▗▖▗▄▄▖ ▗▖ ▗▖▗▄▄▄▖▗▄▄▄▖▗▄▄▖ 
▐▌   ▐▌   ▐▛▚▖▐▌  █  ▐▌ ▐▌▐▌ ▐▌▐▌       ▐▌  ▐▌▐▌   ▐▌ ▐▌  █  ▐▌   ▐▌   ▐▌       ▐▌   ▐▌ ▐▌▐▛▚▞▜▌▐▌ ▐▌▐▌ ▐▌  █  ▐▌   ▐▌ ▐▌
▐▌   ▐▛▀▀▘▐▌ ▝▜▌  █  ▐▛▀▚▖▐▛▀▜▌▐▌       ▐▌  ▐▌▐▛▀▀▘▐▛▀▜▌  █  ▐▌   ▐▌   ▐▛▀▀▘    ▐▌   ▐▌ ▐▌▐▌  ▐▌▐▛▀▘ ▐▌ ▐▌  █  ▐▛▀▀▘▐▛▀▚▖
▝▚▄▄▖▐▙▄▄▖▐▌  ▐▌  █  ▐▌ ▐▌▐▌ ▐▌▐▙▄▄▖     ▝▚▞▘ ▐▙▄▄▖▐▌ ▐▌▗▄█▄▖▝▚▄▄▖▐▙▄▄▖▐▙▄▄▖    ▝▚▄▄▖▝▚▄▞▘▐▌  ▐▌▐▌   ▝▚▄▞▘  █  ▐▙▄▄▖▐▌ ▐▌
                                                                                                                                                                                                                                                                                                                                                                      
EOF

application_name="Baby Safety Reminder App"

echo "$application_name will start in 10 seconds..."
echo "Press any key **two times** to cancel the $application_name starting."

cancel_count=0

# Start 10-second countdown
for i in {10..1}; do
    echo -n "$i... "
    
    # Check for keypress (non-blocking, 1 second timeout)
    if read -t 1 -n 1 key; then
        ((cancel_count++))
        if [[ $cancel_count -eq 1 ]]; then
            echo -e "\nPress any key again to stop"
        elif [[ $cancel_count -eq 2 ]]; then
            echo -e "\nStarting cancelled."
            exit 0
        fi
    fi
done

echo -e "\nStarting $application_name..."

gnome-terminal --title="Vehicle App" -- bash -c "./shell_script/launch_vehicle_app.sh baby_safety_reminder; exec bash" &

sleep 10
# Launch KUKSA Client
# gnome-terminal --title="KUKSA Client" -- bash -c "./shell_script/launch_kuksa_client_cli.sh; exec bash" &

# Launch Podman OCS App
gnome-terminal --title="Podman OCS App" -- bash -c "./shell_script/launch_podman_OCS_app.sh; exec bash" &
