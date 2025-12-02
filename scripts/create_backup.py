#!/usr/bin/env python3
"""
Create Versioned Backup
Automatically increments version and creates backup with timestamp
"""

import shutil
import os
import re
from datetime import datetime
from pathlib import Path

def get_next_version():
    """Find the latest version and increment it"""
    backups_dir = Path('backups')
    if not backups_dir.exists():
        return 'V1.0'
    
    backups = list(backups_dir.iterdir())
    if not backups:
        return 'V1.0'
    
    # Extract version numbers from backup names
    versions = []
    for backup in backups:
        match = re.search(r'V(\d+)\.(\d+)', backup.name)
        if match:
            major, minor = int(match.group(1)), int(match.group(2))
            versions.append((major, minor))
    
    if not versions:
        return 'V1.0'
    
    # Get highest version and increment minor
    major, minor = max(versions)
    return f'V{major}.{minor + 1}'

def create_backup(description='AutoBackup'):
    """Create a versioned backup"""
    version = get_next_version()
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_name = f'{version}-{description}-{timestamp}'
    backup_dir = Path(f'backups/{backup_name}')
    
    # List of critical files/directories
    items = [
        'app.py',
        'database.py',
        'mockup_generator.py',
        'layer_mockup_generator.py',
        'mockup_learning.db',
        'agents/',
        'templates/',
        'static/',
        'tests/',
        'SESSION_LOG.md',
        'PROJECT_NOTES.md',
        'DEPLOYMENT_LOG.md',
        'requirements.txt',
        '.cursorrules',
    ]
    
    print(f'📦 Creating backup: {backup_name}')
    os.makedirs(backup_dir, exist_ok=True)
    
    copied_count = 0
    for item in items:
        if os.path.exists(item):
            print(f'   Copying {item}...')
            try:
                if os.path.isdir(item):
                    shutil.copytree(item, backup_dir / item, dirs_exist_ok=True)
                else:
                    shutil.copy2(item, backup_dir)
                copied_count += 1
            except Exception as e:
                print(f'   ⚠️  Warning: Could not copy {item}: {e}')
    
    print(f'✅ Backup created: {backup_dir}')
    print(f'   Version: {version}')
    print(f'   Files/directories copied: {copied_count}/{len(items)}')
    print(f'   Size: {get_dir_size(backup_dir):.1f} MB')
    
    return backup_dir

def get_dir_size(path):
    """Calculate directory size in MB"""
    total = 0
    for entry in Path(path).rglob('*'):
        if entry.is_file():
            try:
                total += entry.stat().st_size
            except:
                pass
    return total / (1024 * 1024)

if __name__ == '__main__':
    import sys
    
    description = sys.argv[1] if len(sys.argv) > 1 else 'AutoBackup'
    create_backup(description)

