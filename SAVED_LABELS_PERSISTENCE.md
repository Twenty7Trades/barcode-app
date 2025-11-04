# Saved Labels Persistence Guide

## Problem
Saved labels were being stored in `/tmp/barcode_app_saved` which gets cleared on server reboot, causing data loss.

## Solution
Changed to use persistent directory: `/home/ec2-user/barcode-app/saved_labels`

## Configuration

### Environment Variable
The saved labels directory can be set via environment variable:
```bash
export SAVED_LABELS_DIR=/home/ec2-user/barcode-app/saved_labels
```

### Default Behavior
- If `SAVED_LABELS_DIR` is not set, it defaults to `saved_labels/` directory in the app folder
- This ensures labels persist across reboots

### Server Configuration
In `wsgi.py`, the environment variable is set:
```python
os.environ.setdefault('SAVED_LABELS_DIR', '/home/ec2-user/barcode-app/saved_labels')
```

## Backup Recommendations

### ✅ Automated Daily Backups (Configured)
A daily backup script runs automatically at 2 AM:
- **Script**: `/home/ec2-user/barcode-app/backup_saved_labels.sh`
- **Backup Location**: `/home/ec2-user/backups/`
- **Retention**: Keeps last 7 days, deletes older backups automatically
- **Cron Schedule**: `0 2 * * *` (Daily at 2 AM)
- **Logs**: `/home/ec2-user/backups/backup.log`

### Manual Backup
To create a backup manually:
```bash
/home/ec2-user/barcode-app/backup_saved_labels.sh
```

### Restore from Backup
To restore a backup:
```bash
cd /home/ec2-user/barcode-app
tar -xzf /home/ec2-user/backups/saved_labels_YYYYMMDD.tar.gz
```

### Check Backup Status
```bash
# View backup logs
cat /home/ec2-user/backups/backup.log

# List backups
ls -lh /home/ec2-user/backups/saved_labels_*.tar.gz

# Check cron job
crontab -l
```

## Current Location
- **Saved Labels**: `/home/ec2-user/barcode-app/saved_labels/`
- **Output Directory**: `/tmp/barcode_app/output/` (temporary, can be cleared)
- **App Directory**: `/home/ec2-user/barcode-app/`

## Recovery
If labels are lost:
1. Check backups if configured
2. Check S3 if S3 backup is set up
3. Check EBS snapshots
4. Re-generate labels from original spreadsheets

## Prevention
- ✅ Saved labels now use persistent directory
- ✅ Environment variable set in wsgi.py
- ⚠️ Consider setting up automated backups
- ⚠️ Consider moving to S3 or EBS for critical data

## Last Updated
- Date: 2025-11-04
- Issue: Saved labels stored in /tmp (cleared on reboot)
- Fix: Changed to persistent directory `/home/ec2-user/barcode-app/saved_labels`

