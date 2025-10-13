# Upload Instructions for EC2 Server (18.220.30.5)

## Step 1: Copy Files to Your Other Machine
Copy the `barcode-app.zip` file from this machine to your other machine (the one that can SSH to 18.220.30.5).

## Step 2: Upload to EC2
On your other machine, run these commands:

```bash
# Upload the zip file
scp barcode-app.zip ubuntu@18.220.30.5:/home/ubuntu/

# SSH into the server
ssh ubuntu@18.220.30.5

# Extract the files
cd /home/ubuntu
unzip barcode-app.zip -d barcode-app
cd barcode-app

# Make deployment script executable
chmod +x deploy.sh

# Run the deployment
./deploy.sh
```

## Step 3: Test Your Application
After deployment completes, your app will be available at:
- **Main page**: http://18.220.30.5
- **Round21**: http://18.220.30.5/round21  
- **Hunter Harms**: http://18.220.30.5/hunter-harms

## What the Deployment Script Does:
1. Installs Python, Nginx, and other dependencies
2. Sets up the application in `/home/ubuntu/barcode-app`
3. Configures Nginx as a reverse proxy
4. Sets up Gunicorn as a systemd service
5. Starts all services automatically

## Troubleshooting:
- Check Gunicorn status: `sudo systemctl status gunicorn.service`
- Check Nginx status: `sudo systemctl status nginx`
- View logs: `tail -f /var/log/barcode-app/gunicorn.log`


