#!/bin/bash
# Quick connection script for barcode-app server
# Usage: ./connect_server.sh [command]

SERVER="ec2-user@18.220.30.5"
SERVER_IP="18.220.30.5"

# Try to find the SSH key in common locations
KEY_PATHS=(
    "$HOME/.ssh/lambda-layer-key.pem"
    "$HOME/.ssh/barcode-app-key.pem"
    "$HOME/.ssh/ec2-key.pem"
    "$HOME/.ssh/aws-key.pem"
    "$HOME/Downloads/*ec2*.pem"
    "$HOME/Downloads/pixel-ec2"
    "$HOME/.ssh/id_ed25519"
)

KEY=""
for path in "${KEY_PATHS[@]}"; do
    # Expand glob patterns
    for expanded in $path; do
        if [ -f "$expanded" ] && [ -r "$expanded" ]; then
            # Test if it's a valid SSH key
            if ssh-keygen -l -f "$expanded" >/dev/null 2>&1; then
                KEY="$expanded"
                echo "✅ Found SSH key: $KEY"
                break 2
            fi
        fi
    done
done

# If no key found, try connecting without specifying key (uses default)
if [ -z "$KEY" ]; then
    echo "⚠️  No SSH key found in common locations"
    echo "Attempting connection with default SSH keys..."
    echo ""
    if [ -z "$1" ]; then
        ssh "$SERVER"
    else
        ssh "$SERVER" "$@"
    fi
else
    # Set proper permissions
    chmod 600 "$KEY" 2>/dev/null
    
    echo "Connecting to $SERVER..."
    echo ""
    if [ -z "$1" ]; then
        ssh -i "$KEY" "$SERVER"
    else
        ssh -i "$KEY" "$SERVER" "$@"
    fi
fi

