#!/bin/bash
# Daily backup script for saved labels
# Keeps only the last 7 days of backups

BACKUP_DIR="/home/ec2-user/backups"
SAVED_LABELS_DIR="/home/ec2-user/barcode-app/saved_labels"
DATE=$(date +%Y%m%d)
BACKUP_FILE="$BACKUP_DIR/saved_labels_${DATE}.tar.gz"

# Create backup directory if it doesn't exist
mkdir -p "$BACKUP_DIR"

# Create backup
if [ -d "$SAVED_LABELS_DIR" ]; then
    tar -czf "$BACKUP_FILE" -C "$(dirname "$SAVED_LABELS_DIR")" "$(basename "$SAVED_LABELS_DIR")" 2>/dev/null
    
    if [ $? -eq 0 ]; then
        echo "$(date): Backup created: $BACKUP_FILE" >> "$BACKUP_DIR/backup.log"
    else
        echo "$(date): Backup failed: $BACKUP_FILE" >> "$BACKUP_DIR/backup.log"
        exit 1
    fi
else
    echo "$(date): Saved labels directory not found: $SAVED_LABELS_DIR" >> "$BACKUP_DIR/backup.log"
    exit 1
fi

# Delete backups older than 7 days
find "$BACKUP_DIR" -name "saved_labels_*.tar.gz" -type f -mtime +7 -delete

# Log cleanup
if [ $? -eq 0 ]; then
    echo "$(date): Old backups cleaned (kept last 7 days)" >> "$BACKUP_DIR/backup.log"
fi

# List current backups
echo "Current backups:" >> "$BACKUP_DIR/backup.log"
ls -lh "$BACKUP_DIR"/saved_labels_*.tar.gz 2>/dev/null >> "$BACKUP_DIR/backup.log" || echo "No backups found" >> "$BACKUP_DIR/backup.log"



