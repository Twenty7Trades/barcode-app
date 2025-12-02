#!/bin/bash

# AWS EC2 Deployment Script for Barcode Generator
# Run this script on your EC2 instance

set -e  # Exit on any error

echo "🚀 Starting Barcode Generator Deployment..."

# Update system
echo "📦 Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install Python 3 and pip
echo "🐍 Installing Python 3 and pip..."
sudo apt install -y python3 python3-pip python3-venv

# Install Nginx
echo "🌐 Installing Nginx..."
sudo apt install -y nginx

# Create application directory
echo "📁 Creating application directory..."
sudo mkdir -p /var/www/barcode-app
sudo chown -R $USER:$USER /var/www/barcode-app

# Create output directory
sudo mkdir -p /var/www/barcode-app/output
sudo chown -R $USER:$USER /var/www/barcode-app/output

# Create log directories
sudo mkdir -p /var/log/gunicorn
sudo mkdir -p /var/run/gunicorn
sudo chown -R $USER:$USER /var/log/gunicorn
sudo chown -R $USER:$USER /var/run/gunicorn

# Create virtual environment
echo "🔧 Setting up Python virtual environment..."
cd /var/www/barcode-app
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
echo "📚 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Set up Nginx configuration
echo "⚙️ Configuring Nginx..."
sudo cp nginx.conf /etc/nginx/sites-available/barcode-app
sudo ln -sf /etc/nginx/sites-available/barcode-app /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Test Nginx configuration
sudo nginx -t

# Create systemd service for Gunicorn
echo "🔧 Creating systemd service..."
sudo tee /etc/systemd/system/barcode-app.service > /dev/null <<EOF
[Unit]
Description=Barcode Generator Gunicorn daemon
Requires=barcode-app.socket
After=network.target

[Service]
Type=notify
User=www-data
Group=www-data
RuntimeDirectory=gunicorn
WorkingDirectory=/var/www/barcode-app
ExecStart=/var/www/barcode-app/venv/bin/gunicorn --config gunicorn.conf.py wsgi:app
ExecReload=/bin/kill -s HUP \$MAINPID
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

# Create socket file for Gunicorn
sudo tee /etc/systemd/system/barcode-app.socket > /dev/null <<EOF
[Unit]
Description=Barcode Generator socket

[Socket]
ListenStream=/var/run/gunicorn/barcode-app.sock
SocketUser=www-data
SocketMode=600

[Install]
WantedBy=sockets.target
EOF

# Set proper permissions
echo "🔐 Setting permissions..."
sudo chown -R www-data:www-data /var/www/barcode-app
sudo chmod -R 755 /var/www/barcode-app

# Enable and start services
echo "🚀 Starting services..."
sudo systemctl daemon-reload
sudo systemctl enable barcode-app.socket
sudo systemctl start barcode-app.socket
sudo systemctl enable barcode-app.service
sudo systemctl start barcode-app.service
sudo systemctl enable nginx
sudo systemctl restart nginx

# Check service status
echo "✅ Checking service status..."
sudo systemctl status barcode-app.service --no-pager
sudo systemctl status nginx --no-pager

echo "🎉 Deployment complete!"
echo "📋 Next steps:"
echo "1. Update your domain name in /etc/nginx/sites-available/barcode-app"
echo "2. Set up SSL certificate with Let's Encrypt (optional)"
echo "3. Configure your security groups to allow HTTP (port 80) and HTTPS (port 443)"
echo "4. Test your application at http://your-ec2-public-ip"
