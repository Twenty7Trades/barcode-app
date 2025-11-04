#!/usr/bin/env python3
"""
WSGI entry point for the barcode generator application.
This file is used by Gunicorn to serve the Flask application.
"""

import os
from app import app

if __name__ == "__main__":
    # Set production environment variables
    os.environ.setdefault('FLASK_SECRET_KEY', 'your-production-secret-key-change-this')
    os.environ.setdefault('OUTPUT_DIR', '/var/www/barcode-app/output')
    # Use persistent directory for saved labels (not /tmp which gets cleared on reboot)
    os.environ.setdefault('SAVED_LABELS_DIR', '/home/ec2-user/barcode-app/saved_labels')
    
    app.run()
