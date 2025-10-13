#!/bin/bash

# Script to help transfer files to your other machine
# Run this script and follow the instructions

echo "🚀 Barcode App Transfer Instructions"
echo "======================================"
echo ""
echo "1. Copy the following file to your other machine:"
echo "   📁 /Applications/barcode-app/barcode-app.zip"
echo ""
echo "2. On your other machine, run these commands:"
echo ""
echo "   # Upload to EC2"
echo "   scp barcode-app.zip ubuntu@18.220.30.5:/home/ubuntu/"
echo ""
echo "   # SSH into EC2"
echo "   ssh ubuntu@18.220.30.5"
echo ""
echo "   # Extract and deploy"
echo "   cd /home/ubuntu"
echo "   unzip barcode-app.zip -d barcode-app"
echo "   cd barcode-app"
echo "   chmod +x deploy.sh"
echo "   ./deploy.sh"
echo ""
echo "3. After deployment, your app will be live at:"
echo "   🌐 http://18.220.30.5"
echo ""
echo "📋 Files ready for transfer:"
ls -la barcode-app.zip
echo ""
echo "✅ Ready to transfer!"


