# 🚀 AWS EC2 Deployment Guide

## Prerequisites
- AWS EC2 instance running Ubuntu 20.04+ or Amazon Linux 2
- SSH access to your EC2 instance
- Domain name (optional, can use EC2 public IP)

## Quick Deployment Steps

### 1. Upload Files to EC2
```bash
# From your local machine, upload all files to EC2
scp -r /Applications/barcode-app/* ubuntu@your-ec2-ip:/home/ubuntu/barcode-app/
```

### 2. SSH into EC2 Instance
```bash
ssh ubuntu@your-ec2-ip
```

### 3. Run Deployment Script
```bash
cd /home/ubuntu/barcode-app
chmod +x deploy.sh
./deploy.sh
```

### 4. Configure Domain (Optional)
```bash
# Edit Nginx configuration
sudo nano /etc/nginx/sites-available/barcode-app

# Replace 'your-domain.com' with your actual domain
# Save and restart Nginx
sudo systemctl restart nginx
```

### 5. Set Up SSL (Optional but Recommended)
```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Get SSL certificate
sudo certbot --nginx -d your-domain.com -d www.your-domain.com
```

## Manual Deployment (Alternative)

If the script doesn't work, follow these manual steps:

### 1. Update System
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-pip python3-venv nginx
```

### 2. Set Up Application
```bash
sudo mkdir -p /var/www/barcode-app
sudo chown -R $USER:$USER /var/www/barcode-app
cp -r /home/ubuntu/barcode-app/* /var/www/barcode-app/
cd /var/www/barcode-app
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Configure Nginx
```bash
sudo cp nginx.conf /etc/nginx/sites-available/barcode-app
sudo ln -sf /etc/nginx/sites-available/barcode-app /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl restart nginx
```

### 4. Set Up Gunicorn Service
```bash
# Copy the systemd service files from deploy.sh
sudo systemctl daemon-reload
sudo systemctl enable barcode-app.socket
sudo systemctl start barcode-app.socket
sudo systemctl enable barcode-app.service
sudo systemctl start barcode-app.service
```

## Troubleshooting

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

### Common Issues

1. **Permission Errors**
   ```bash
   sudo chown -R www-data:www-data /var/www/barcode-app
   sudo chmod -R 755 /var/www/barcode-app
   ```

2. **Port Already in Use**
   ```bash
   sudo lsof -i :8000
   sudo pkill -f gunicorn
   sudo systemctl restart barcode-app.service
   ```

3. **Nginx Configuration Error**
   ```bash
   sudo nginx -t
   sudo systemctl restart nginx
   ```

## Security Groups Configuration

Make sure your EC2 security group allows:
- **SSH (22)**: From your IP
- **HTTP (80)**: From anywhere (0.0.0.0/0)
- **HTTPS (443)**: From anywhere (0.0.0.0/0) - if using SSL

## Testing Your Deployment

1. **Check if services are running:**
   ```bash
   curl http://localhost:8000
   curl http://your-ec2-ip
   ```

2. **Test the application:**
   - Visit `http://your-ec2-ip` in your browser
   - Test both Round21 and Hunter Harms formats
   - Upload sample files to verify functionality

## File Structure After Deployment

```
/var/www/barcode-app/
├── app.py
├── barcode_gen.py
├── wsgi.py
├── gunicorn.conf.py
├── requirements.txt
├── templates/
│   ├── index.html
│   ├── round21.html
│   ├── hunter_harms.html
│   └── result.html
├── static/
│   └── style.css
├── venv/
└── output/
```

## Environment Variables

The application uses these environment variables:
- `FLASK_SECRET_KEY`: Set in wsgi.py (change for production!)
- `OUTPUT_DIR`: Set to `/var/www/barcode-app/output`

## Maintenance

### Update Application
```bash
cd /var/www/barcode-app
git pull  # if using git
# or upload new files
sudo systemctl restart barcode-app.service
```

### Backup
```bash
# Backup application files
tar -czf barcode-app-backup-$(date +%Y%m%d).tar.gz /var/www/barcode-app
```

## Support

If you encounter issues:
1. Check the logs first
2. Verify all services are running
3. Check security group settings
4. Ensure file permissions are correct
