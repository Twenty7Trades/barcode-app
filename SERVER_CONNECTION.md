# Server Connection Guide

## Server Information
- **IP Address**: `18.220.30.5`
- **Username**: `ec2-user` (Amazon Linux)
- **OS**: Amazon Linux (not Ubuntu)
- **Application Location**: `/home/ec2-user/barcode-app`
- **Working SSH Key**: `~/.ssh/lambda-layer-key.pem`

## SSH Connection

### Basic Connection Command
```bash
ssh -i ~/.ssh/lambda-layer-key.pem ec2-user@18.220.30.5
```

### Using a Specific Key File
If you have the SSH key file (usually a `.pem` file), use:
```bash
ssh -i /path/to/your-key.pem ec2-user@18.220.30.5
```

### Server Expected Key
The server expects an **ed25519** SSH key with fingerprint starting with:
```
IKzTgFUkpzwfi9Dy14Z4lT92+IabuyXHHGWuqJKNmJpQ
```

## Finding Your SSH Key

### Common Locations
1. **~/.ssh/** directory:
   ```bash
   ls -la ~/.ssh/
   ```

2. **Downloads folder**:
   ```bash
   find ~/Downloads -name "*.pem" -o -name "*ec2*" -o -name "*key*"
   ```

3. **Desktop or Documents**:
   ```bash
   find ~/Desktop ~/Documents -name "*.pem"
   ```

4. **Password Manager**:
   - Check 1Password, Keychain Access, or other password managers
   - Search for "18.220.30.5", "barcode", "ec2", or "AWS"

5. **AWS EC2 Console**:
   - Go to AWS Console → EC2 → Key Pairs
   - Download the key pair associated with this instance

### Testing Keys
To test if a key works:
```bash
ssh -i /path/to/key.pem ubuntu@18.220.30.5 "echo 'Connected successfully'"
```

To check a key's fingerprint:
```bash
ssh-keygen -l -f /path/to/key.pem
```

## Application Directory Structure

Once connected, the application files are typically located at:
```
/var/www/barcode-app/
├── app.py
├── barcode_gen.py
├── wsgi.py
├── gunicorn.conf.py
├── requirements.txt
├── templates/
├── static/
├── venv/
└── output/
```

Or alternatively:
```
/home/ubuntu/barcode-app/
```

## Common Commands

### Check Service Status
```bash
sudo systemctl status barcode-app.service
sudo systemctl status nginx
```

### View Logs
```bash
# Application logs
sudo journalctl -u barcode-app.service -f

# Nginx logs
sudo tail -f /var/log/nginx/barcode-app.error.log
sudo tail -f /var/log/nginx/barcode-app.access.log

# Gunicorn logs
sudo tail -f /var/log/gunicorn/error.log
```

### Restart Services
```bash
sudo systemctl restart barcode-app.service
sudo systemctl restart nginx
```

### Update Application
```bash
cd /var/www/barcode-app  # or /home/ubuntu/barcode-app
# Make your changes to files
sudo systemctl restart barcode-app.service
```

### Check Application Files
```bash
cd /var/www/barcode-app  # or /home/ubuntu/barcode-app
ls -la
```

## Troubleshooting

### Permission Denied Error
If you get "Permission denied (publickey)", the SSH key is either:
1. Not found
2. Wrong permissions (should be `chmod 600`)
3. Wrong key (doesn't match server)

**Fix permissions:**
```bash
chmod 600 /path/to/key.pem
```

### Can't Find Key
1. Check AWS EC2 Console → Key Pairs
2. Check password manager
3. Check other machines you've used
4. Contact AWS administrator if you don't have access

### Connection Timeout
- Check if security group allows SSH (port 22) from your IP
- Verify the IP address is correct: `18.220.30.5`
- Check if instance is running in AWS Console

## Quick Connection Script

Create a script in your local machine for easy connection:

```bash
#!/bin/bash
# connect_server.sh

KEY_PATH="$HOME/.ssh/barcode-app-key.pem"  # Update this path
SERVER="ubuntu@18.220.30.5"

if [ -f "$KEY_PATH" ]; then
    ssh -i "$KEY_PATH" "$SERVER"
else
    echo "SSH key not found at $KEY_PATH"
    echo "Attempting connection without specifying key..."
    ssh "$SERVER"
fi
```

Make it executable:
```bash
chmod +x connect_server.sh
```

## Notes

- The server uses Gunicorn with systemd service
- Nginx serves as reverse proxy
- Application runs on port 8000 (internal)
- Nginx serves on port 80 (HTTP)
- Files are served from `/var/www/barcode-app` or `/home/ubuntu/barcode-app`

## Security Reminder

⚠️ **NEVER commit SSH keys to git!** Always add them to `.gitignore`:
```
*.pem
*key.pem
*.key
connect_server.sh  # If it contains key paths
```

## Keys Found (But Don't Match Server)

The following keys were found but do not match the server's expected key:
- `~/.ssh/id_ed25519` - SHA256:KwXKSFK... (doesn't match)
- `~/.ssh/lambda-layer-key.pem` - RSA key (doesn't match)
- `~/Downloads/pixel-ec2` - SHA256:deN9Yr5r... (doesn't match)

**Server expects:** ed25519 key starting with `IKzTgFUk...`

## How to Get the Correct Key

### Option 1: AWS EC2 Console
1. Log into AWS Console
2. Go to EC2 → Instances
3. Find instance with IP `18.220.30.5`
4. Check the "Key pair name" in instance details
5. Go to EC2 → Key Pairs
6. Find and download the matching key pair

### Option 2: Check Other Machines
If you connected from another machine last week, check:
- `~/.ssh/` directory
- Downloads folder
- Desktop/Documents for `.pem` files

### Option 3: Password Manager
Search for:
- "18.220.30.5"
- "barcode-app"
- "ec2"
- "AWS"

### Option 4: Generate New Key Pair (if you have AWS access)
If you have AWS access, you can create a new key pair and add it to the instance:
```bash
# Generate new key
ssh-keygen -t ed25519 -f ~/.ssh/barcode-app-key

# Add public key to server (requires existing access)
# Or use AWS Systems Manager Session Manager if enabled
```

## Quick Connection Script

Use the included script:
```bash
./connect_server.sh
```

This script will:
1. Search common locations for SSH keys
2. Try to connect with found keys
3. Fall back to default SSH keys if none found

## Last Updated
- Date: 2025-11-03
- Status: 
  - Created new key: `~/.ssh/barcode-app-key` (ed25519)
  - Public key needs to be added to server: `ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIEjkf3OKMLpiehU/lHa/4QVP55pwGoMElCVT3criaF4w barcode-app-server-20251103`
  - Old keys tested: `pixel-ec2` and `lambda-layer-key.pem` don't work (server rejects them)
  - AWS Console methods: EC2 Instance Connect failed, Session Manager says SSM agent not online
  - Next step: Try EC2 Instance Connect again, or add IAM role with SSM permissions and reboot
- Keys found but don't match server:
  - `pixel-ec2` - SHA256:deN9Yr5r... (doesn't match)
  - `lambda-layer-key.pem` - RSA key (doesn't match)

