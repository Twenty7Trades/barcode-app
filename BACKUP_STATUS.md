# Complete Backup Status

## ✅ What is Backed Up

### 1. Saved Labels
- **What**: User-saved label sets (PNGs, PDFs, metadata)
- **Location**: `/home/ec2-user/barcode-app/saved_labels/`
- **Backup File**: `saved_labels_YYYYMMDD.tar.gz`
- **Size**: ~3.9M (varies by number of saved labels)

### 2. Application Codebase
- **What**: All application code, templates, static files, configs
- **Location**: `/home/ec2-user/barcode-app/`
- **Backup File**: `codebase_YYYYMMDD.tar.gz`
- **Size**: ~8.3M
- **Includes**:
  - All Python files (`*.py`)
  - Templates (`templates/`)
  - Static files (`static/`)
  - Configuration files (`*.conf`, `*.sh`, `requirements.txt`)
  - Documentation (`*.md`)
  - Backup scripts
- **Excludes**:
  - Virtual environment (`.venv/`, `venv/`)
  - Python cache (`__pycache__/`, `*.pyc`)
  - Output directory (temporary files)
  - Saved labels (backed up separately)
  - Log files

## 📍 Backup Locations

### Server Backups
- **Directory**: `/home/ec2-user/backups/`
- **Schedule**: Daily at 2:00 AM
- **Retention**: 7 days (automatically deletes older backups)
- **Script**: `/home/ec2-user/barcode-app/backup_full_app.sh`

### Backup Files
```
/home/ec2-user/backups/
├── saved_labels_20251104.tar.gz    (3.9M) - Saved labels
├── codebase_20251104.tar.gz         (8.3M) - Application code
├── saved_labels_20251105.tar.gz    (future backups)
├── codebase_20251105.tar.gz        (future backups)
└── backup.log                      (backup activity log)
```

## 🔄 Backup Process

### Automatic Daily Backup
- **Time**: 2:00 AM UTC daily
- **Cron Job**: `0 2 * * * /home/ec2-user/barcode-app/backup_full_app.sh`
- **Logs**: `/home/ec2-user/backups/backup.log`

### Manual Backup
To create a backup manually:
```bash
/home/ec2-user/barcode-app/backup_full_app.sh
```

## 📦 What's NOT Backed Up

These are excluded for good reasons:
- **Virtual Environment** (`.venv/`) - Can be recreated with `pip install -r requirements.txt`
- **Python Cache** (`__pycache__/`) - Auto-generated, not needed
- **Output Directory** (`output/`) - Temporary files, regenerated on use
- **Log Files** (`*.log`) - Temporary, can be regenerated

## 🔍 Verification

### Check Current Backups
```bash
ls -lh /home/ec2-user/backups/
```

### View Backup Logs
```bash
cat /home/ec2-user/backups/backup.log
```

### Verify Backup Contents
```bash
# List contents of codebase backup
tar -tzf /home/ec2-user/backups/codebase_YYYYMMDD.tar.gz | head -20

# List contents of saved labels backup
tar -tzf /home/ec2-user/backups/saved_labels_YYYYMMDD.tar.gz | head -20
```

## 🔄 Restore Process

### Restore Saved Labels
```bash
cd /home/ec2-user/barcode-app
tar -xzf /home/ec2-user/backups/saved_labels_YYYYMMDD.tar.gz
```

### Restore Codebase
```bash
cd /home/ec2-user
# Backup current code first!
cp -r barcode-app barcode-app.backup.$(date +%Y%m%d)

# Extract backup
tar -xzf /home/ec2-user/backups/codebase_YYYYMMDD.tar.gz

# Restart services
sudo systemctl restart barcode-app.service
```

### Full Restore (Complete Disaster Recovery)
```bash
# 1. Restore codebase
cd /home/ec2-user
tar -xzf /home/ec2-user/backups/codebase_YYYYMMDD.tar.gz

# 2. Restore saved labels
cd /home/ec2-user/barcode-app
tar -xzf /home/ec2-user/backups/saved_labels_YYYYMMDD.tar.gz

# 3. Recreate virtual environment
cd /home/ec2-user/barcode-app
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 4. Restart services
sudo systemctl restart barcode-app.service
sudo systemctl restart nginx
```

## 📊 Backup Summary

| Item | Location | Backup File | Size | Retention |
|------|----------|-------------|------|-----------|
| Saved Labels | `/home/ec2-user/barcode-app/saved_labels/` | `saved_labels_*.tar.gz` | ~3.9M | 7 days |
| Codebase | `/home/ec2-user/barcode-app/` | `codebase_*.tar.gz` | ~8.3M | 7 days |

## 🔐 Additional Backup Recommendations

### Option 1: Git Repository (Recommended)
Your codebase should be in git:
```bash
# On your local machine
cd /Applications/barcode-app
git add .
git commit -m "Backup before deployment"
git push origin main
```

### Option 2: S3 Backup
Upload backups to S3 for long-term storage:
```bash
aws s3 sync /home/ec2-user/backups/ s3://your-bucket/barcode-app-backups/
```

### Option 3: EBS Snapshots
Create regular EBS snapshots of the volume containing the app directory.

## ✅ Current Status

- ✅ Daily backups configured
- ✅ Saved labels backed up
- ✅ Codebase backed up
- ✅ 7-day retention active
- ✅ Automatic cleanup working
- ✅ Logs being maintained

## Last Updated
- Date: 2025-11-04
- Status: Full backup system active
- Next Backup: Tomorrow at 2:00 AM UTC



