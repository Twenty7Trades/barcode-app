#!/bin/bash

# Script to upload barcode app files to AWS EC2
# Usage: ./upload_to_aws.sh your-ec2-ip

if [ $# -eq 0 ]; then
    echo "Usage: $0 <ec2-ip-address>"
    echo "Example: $0 54.123.45.67"
    exit 1
fi

EC2_IP=$1
echo "🚀 Uploading barcode app to EC2 instance: $EC2_IP"

# Create directory on EC2
echo "📁 Creating directory on EC2..."
ssh ubuntu@$EC2_IP "mkdir -p /home/ubuntu/barcode-app"

# Upload all files
echo "📤 Uploading files..."
scp -r app.py barcode_gen.py wsgi.py gunicorn.conf.py nginx.conf requirements.txt deploy.sh ubuntu@$EC2_IP:/home/ubuntu/barcode-app/
scp -r templates/ ubuntu@$EC2_IP:/home/ubuntu/barcode-app/
scp -r static/ ubuntu@$EC2_IP:/home/ubuntu/barcode-app/

echo "✅ Upload complete!"
echo "📋 Next steps:"
echo "1. SSH into your EC2 instance: ssh ubuntu@$EC2_IP"
echo "2. Run the deployment script: cd /home/ubuntu/barcode-app && ./deploy.sh"
echo "3. Test your application at: http://$EC2_IP"


