# Python 3.9 Upgrade Plan

## Current Status
- **Current Python Version**: ✅ **3.11.6** (UPGRADED)
- **Previous Version**: 3.9.20 (sunset by AWS)
- **AWS Sunset**: Python 3.9 support ending soon
- **Node.js**: Not installed (not an issue)
- **Upgrade Date**: 2025-11-10

## Recommended Upgrade Path

### Option 1: Upgrade to Python 3.11 or 3.12 (Recommended)
Python 3.11+ is the current stable version with long-term support.

### Option 2: Upgrade to Python 3.13 (Latest)
If available, Python 3.13 is the newest version.

## Upgrade Steps

### 1. Check Available Python Versions
```bash
dnf list available python3*
```

### 2. Install New Python Version
```bash
# For Python 3.11
sudo dnf install -y python3.11 python3.11-pip

# Or for Python 3.12
sudo dnf install -y python3.12 python3.12-pip
```

### 3. Create New Virtual Environment
```bash
cd /home/ec2-user/barcode-app
python3.11 -m venv .venv_new  # or python3.12
source .venv_new/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Test Application
```bash
# Test imports
python -c "import app; import barcode_gen; print('OK')"

# Test with gunicorn
gunicorn --config gunicorn_amazon_linux.conf.py wsgi:app
```

### 5. Switch to New Environment
```bash
# Backup old venv
mv .venv .venv_python39_backup

# Use new venv
mv .venv_new .venv

# Restart service
sudo systemctl restart barcode-app.service
```

### 6. Verify
```bash
# Check Python version
python --version

# Check service status
sudo systemctl status barcode-app.service

# Test application
curl http://localhost:8000
```

## Compatibility Check

Before upgrading, verify:
- ✅ Flask 3.0.0+ (supports Python 3.11+)
- ✅ pandas 2.0.0+ (supports Python 3.11+)
- ✅ Pillow 10.0.0+ (supports Python 3.11+)
- ✅ All dependencies in requirements.txt are compatible

## Rollback Plan

If issues occur:
```bash
# Restore old virtual environment
mv .venv .venv_python311
mv .venv_python39_backup .venv

# Restart service
sudo systemctl restart barcode-app.service
```

## Timeline

- **Previous**: Python 3.9.20 (sunset by AWS)
- **Current**: ✅ Python 3.11.6 (UPGRADED)
- **Upgrade Date**: 2025-11-10
- **Status**: ✅ Complete and running

## Upgrade Completed

The upgrade to Python 3.11.6 has been completed successfully:
- ✅ Python 3.11.6 installed
- ✅ New virtual environment created
- ✅ All dependencies installed
- ✅ Application tested and working
- ✅ Service running with Python 3.11.6
- ✅ Old Python 3.9 venv backed up as `.venv_python39_backup`

