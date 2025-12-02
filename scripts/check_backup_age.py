#!/usr/bin/env python3
"""
Check Backup Age
Determines if a new backup is needed based on:
- Time since last backup (48 hours)
- File changes since last backup
"""

import os
import time
import subprocess
from datetime import datetime
from pathlib import Path

def check_backup_age():
    """Check if backup is needed"""
    
    # Find most recent backup
    backups_dir = Path('backups')
    if not backups_dir.exists():
        print('⚠️  No backups directory found')
        print('✅ Recommended: Create initial backup')
        print('   Run: python3 scripts/create_backup.py "InitialBackup"')
        return 1
    
    # Get all backup directories
    backups = [d for d in backups_dir.iterdir() if d.is_dir()]
    if not backups:
        print('⚠️  No backups found')
        print('✅ Recommended: Create initial backup')
        print('   Run: python3 scripts/create_backup.py "InitialBackup"')
        return 1
    
    # Find most recent backup by modification time
    latest_backup = max(backups, key=lambda d: d.stat().st_mtime)
    backup_age_seconds = time.time() - latest_backup.stat().st_mtime
    backup_age_hours = backup_age_seconds / 3600
    
    print(f'📁 Latest backup: {latest_backup.name}')
    print(f'⏰ Backup age: {backup_age_hours:.1f} hours')
    
    # Check if backup is older than 48 hours
    if backup_age_hours >= 48:
        print(f'   ⚠️  Backup is {backup_age_hours:.1f} hours old (>48 hours)')
        
        # Check if there are uncommitted changes or new commits
        has_changes = False
        
        # Check git status
        try:
            result = subprocess.run(
                ['git', 'status', '--porcelain'],
                capture_output=True,
                text=True,
                cwd='.',
                check=False
            )
            has_changes = len(result.stdout.strip()) > 0
        except:
            print('   ⚠️  Could not check git status')
            has_changes = True  # Assume changes if we can't check
        
        # Check commits since last backup
        has_commits = False
        try:
            backup_time = datetime.fromtimestamp(latest_backup.stat().st_mtime)
            result = subprocess.run(
                ['git', 'log', '--since', backup_time.isoformat(), '--oneline'],
                capture_output=True,
                text=True,
                cwd='.',
                check=False
            )
            has_commits = len(result.stdout.strip()) > 0
        except:
            print('   ⚠️  Could not check git commits')
            has_commits = True  # Assume commits if we can't check
        
        if has_changes or has_commits:
            print('')
            print('⚠️  ⚠️  ⚠️  BACKUP NEEDED ⚠️  ⚠️  ⚠️')
            print(f'   - Last backup is {backup_age_hours:.1f} hours old')
            if has_changes:
                print('   - Uncommitted file changes detected')
            if has_commits:
                print('   - New commits since last backup')
            print('')
            print('🚀 Create backup now:')
            print('   python3 scripts/create_backup.py')
            print('')
            return 2  # Exit code 2 = backup needed
        else:
            print('✅ No backup needed (no changes in 48 hours)')
            return 0
    else:
        print(f'✅ Backup is recent ({backup_age_hours:.1f} hours old)')
        return 0

if __name__ == '__main__':
    exit(check_backup_age())

