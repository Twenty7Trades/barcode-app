#!/bin/bash
# Daily backup script for barcode app
# Backs up both saved labels AND application code
# Keeps only the last 7 days of backups

BACKUP_DIR="/home/ec2-user/backups"
SAVED_LABELS_DIR="/home/ec2-user/barcode-app/saved_labels"
APP_DIR="/home/ec2-user/barcode-app"
DATE=$(date +%Y%m%d)

# Create backup directory if it doesn't exist
mkdir -p "$BACKUP_DIR"

# Backup 1: Saved Labels
echo "$(date): Starting backups..." >> "$BACKUP_DIR/backup.log"

if [ -d "$SAVED_LABELS_DIR" ]; then
    LABELS_BACKUP="$BACKUP_DIR/saved_labels_${DATE}.tar.gz"
    tar -czf "$LABELS_BACKUP" -C "$(dirname "$SAVED_LABELS_DIR")" "$(basename "$SAVED_LABELS_DIR")" 2>/dev/null
    
    if [ $? -eq 0 ]; then
        echo "$(date): Saved labels backup created: $LABELS_BACKUP" >> "$BACKUP_DIR/backup.log"
    else
        echo "$(date): Saved labels backup failed: $LABELS_BACKUP" >> "$BACKUP_DIR/backup.log"
    fi
else
    echo "$(date): Saved labels directory not found: $SAVED_LABELS_DIR" >> "$BACKUP_DIR/backup.log"
fi

# Backup 2: Application Code (exclude venv, __pycache__, temporary files)
CODE_BACKUP="$BACKUP_DIR/codebase_${DATE}.tar.gz"
cd "$(dirname "$APP_DIR")"

tar -czf "$CODE_BACKUP" \
    --exclude="$(basename "$APP_DIR")/.venv" \
    --exclude="$(basename "$APP_DIR")/venv" \
    --exclude="$(basename "$APP_DIR")/__pycache__" \
    --exclude="$(basename "$APP_DIR")/*/__pycache__" \
    --exclude="$(basename "$APP_DIR")/*.pyc" \
    --exclude="$(basename "$APP_DIR")/*.pyo" \
    --exclude="$(basename "$APP_DIR")/.DS_Store" \
    --exclude="$(basename "$APP_DIR")/output" \
    --exclude="$(basename "$APP_DIR")/saved_labels" \
    --exclude="$(basename "$APP_DIR")/*.log" \
    "$(basename "$APP_DIR")" 2>/dev/null

if [ $? -eq 0 ]; then
    echo "$(date): Codebase backup created: $CODE_BACKUP" >> "$BACKUP_DIR/backup.log"
else
    echo "$(date): Codebase backup failed: $CODE_BACKUP" >> "$BACKUP_DIR/backup.log"
fi

# Delete backups older than 7 days
find "$BACKUP_DIR" -name "saved_labels_*.tar.gz" -type f -mtime +7 -delete
find "$BACKUP_DIR" -name "codebase_*.tar.gz" -type f -mtime +7 -delete

# Log cleanup
if [ $? -eq 0 ]; then
    echo "$(date): Old backups cleaned (kept last 7 days)" >> "$BACKUP_DIR/backup.log"
fi

# List current backups
echo "Current backups:" >> "$BACKUP_DIR/backup.log"
ls -lh "$BACKUP_DIR"/saved_labels_*.tar.gz "$BACKUP_DIR"/codebase_*.tar.gz 2>/dev/null >> "$BACKUP_DIR/backup.log" || echo "No backups found" >> "$BACKUP_DIR/backup.log"

echo "$(date): Backup completed" >> "$BACKUP_DIR/backup.log"



