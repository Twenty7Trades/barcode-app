#!/bin/bash
set -e

APP_DIR="/home/ec2-user/barcode-app"
VENV_DIR="$APP_DIR/.venv"
LOG_DIR="/var/log/barcode-app"
GUNICORN_SERVICE_FILE="/etc/systemd/system/barcode-app.service"
NGINX_CONF_FILE="/etc/nginx/conf.d/barcode-app.conf"

echo "🚀 Starting Barcode Generator Deployment on Amazon Linux..."

# 1. Update and install system dependencies
echo "📦 Updating system and installing dependencies..."
sudo dnf update -y
sudo dnf install -y python3 python3-pip nginx curl zip unzip

# 2. Create application directory and virtual environment
echo "📁 Setting up application directory and virtual environment..."
cd $APP_DIR

# Create virtual environment if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    python3 -m venv $VENV_DIR
fi

source $VENV_DIR/bin/activate

# 3. Install Python dependencies
echo "🐍 Installing Python dependencies..."
pip install -r requirements.txt

# 4. Configure Gunicorn systemd service
echo "⚙️ Configuring Gunicorn service..."
sudo bash -c "cat > $GUNICORN_SERVICE_FILE" <<EOF
[Unit]
Description=Gunicorn instance to serve barcode-app
After=network.target

[Service]
User=ec2-user
Group=ec2-user
WorkingDirectory=$APP_DIR
Environment="PATH=$VENV_DIR/bin"
Environment="FLASK_SECRET_KEY=your_super_secret_key_here"
ExecStart=$VENV_DIR/bin/gunicorn --config gunicorn.conf.py wsgi:app
Restart=always
RestartSec=3
StandardOutput=append:$LOG_DIR/gunicorn.log
StandardError=append:$LOG_DIR/gunicorn.log

[Install]
WantedBy=multi-user.target
EOF

# Create log directory and set permissions
sudo mkdir -p $LOG_DIR
sudo chown ec2-user:ec2-user $LOG_DIR
sudo chmod 775 $LOG_DIR

# 5. Configure Nginx
echo "🌐 Configuring Nginx..."
sudo bash -c "cat > $NGINX_CONF_FILE" <<EOF
server {
    listen 80;
    server_name 18.220.30.5;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN";
    add_header X-XSS-Protection "1; mode=block";
    add_header X-Content-Type-Options "nosniff";
    add_header Referrer-Policy "no-referrer-when-downgrade";
    add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self';";

    client_max_body_size 50M;

    location /static {
        alias $APP_DIR/static;
        expires 30d;
        add_header Cache-Control "public, no-transform";
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_redirect off;
    }

    error_page 500 502 503 504 /500.html;
    location = /500.html {
        root /usr/share/nginx/html;
    }
}
EOF

# 6. Start and enable services
echo "🚀 Starting and enabling services..."
sudo systemctl daemon-reload
sudo systemctl restart gunicorn.service
sudo systemctl enable gunicorn.service
sudo systemctl restart nginx
sudo systemctl enable nginx

echo "✅ Deployment complete! Your application should be live at http://18.220.30.5"
echo "You can check Gunicorn status with: sudo systemctl status gunicorn.service"
echo "You can check Nginx status with: sudo systemctl status nginx"
echo "Gunicorn logs: tail -f $LOG_DIR/gunicorn.log"


