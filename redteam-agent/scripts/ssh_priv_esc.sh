#!/bin/bash

# Variables
HOST="localhost"
PORT="32772"
USERNAME="esmythe"
PASSWORD="WP5=JoZeev"

# Use sshpass to pass the password non-interactively to the SSH client
sshpass -p "$PASSWORD" ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -p "$PORT" "$USERNAME@$HOST" << EOF
# Commands to execute on the remote host
sudo apt-get update
sudo apt-get install -y some-package
# Add more commands as needed
EOF
