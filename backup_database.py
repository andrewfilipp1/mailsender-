#!/usr/bin/env python3
"""
Database Backup Script for Vlasia Blog
This script helps backup and restore PostgreSQL database on Digital Ocean
"""
import os
import sys
import subprocess
from datetime import datetime
from pathlib import Path
import argparse

def backup_database(host='localhost', port='5432', database='vlasia_blog', 
                   username='vlasia_user', password=None, backup_dir='backups'):
    """Backup PostgreSQL database"""
    
    # Create backup directory if it doesn't exist
    Path(backup_dir).mkdir(exist_ok=True)
    
    # Generate backup filename with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_file = f"{backup_dir}/vlasia_blog_backup_{timestamp}.sql"
    
    # Set password environment variable
    env = os.environ.copy()
    if password:
        env['PGPASSWORD'] = password
    
    # Create backup command
    cmd = [
        'pg_dump',
        f'--host={host}',
        f'--port={port}',
        f'--dbname={database}',
        f'--username={username}',
        '--verbose',
        '--clean',
        '--no-owner',
        '--no-privileges',
        f'--file={backup_file}'
    ]
    
    try:
        print(f"🔄 Creating backup: {backup_file}")
        result = subprocess.run(cmd, env=env, capture_output=True, text=True, check=True)
        print(f"✅ Backup created successfully: {backup_file}")
        print(f"📊 Backup size: {Path(backup_file).stat().st_size / 1024:.2f} KB")
        return backup_file
    except subprocess.CalledProcessError as e:
        print(f"❌ Backup failed: {e}")
        print(f"Error output: {e.stderr}")
        return None

def restore_database(backup_file, host='localhost', port='5432', database='vlasia_blog',
                    username='vlasia_user', password=None, drop_existing=True):
    """Restore PostgreSQL database from backup"""
    
    if not Path(backup_file).exists():
        print(f"❌ Backup file not found: {backup_file}")
        return False
    
    # Set password environment variable
    env = os.environ.copy()
    if password:
        env['PGPASSWORD'] = password
    
    try:
        if drop_existing:
            # Drop and recreate database
            print("🗑️ Dropping existing database...")
            drop_cmd = [
                'psql',
                f'--host={host}',
                f'--port={port}',
                f'--username={username}',
                '--command=DROP DATABASE IF EXISTS vlasia_blog;'
            ]
            subprocess.run(drop_cmd, env=env, check=True)
            
            create_cmd = [
                'psql',
                f'--host={host}',
                f'--port={port}',
                f'--username={username}',
                '--command=CREATE DATABASE vlasia_blog;'
            ]
            subprocess.run(create_cmd, env=env, check=True)
            print("✅ Database recreated")
        
        # Restore from backup
        print(f"🔄 Restoring from backup: {backup_file}")
        restore_cmd = [
            'psql',
            f'--host={host}',
            f'--port={port}',
            f'--dbname={database}',
            f'--username={username}',
            f'--file={backup_file}'
        ]
        
        result = subprocess.run(restore_cmd, env=env, capture_output=True, text=True, check=True)
        print("✅ Database restored successfully")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Restore failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def list_backups(backup_dir='backups'):
    """List available backups"""
    backup_path = Path(backup_dir)
    if not backup_path.exists():
        print(f"❌ Backup directory not found: {backup_dir}")
        return
    
    backups = list(backup_path.glob('vlasia_blog_backup_*.sql'))
    if not backups:
        print(f"📭 No backups found in {backup_dir}")
        return
    
    print(f"📋 Available backups in {backup_dir}:")
    for backup in sorted(backups, reverse=True):
        size = backup.stat().st_size / 1024
        mtime = datetime.fromtimestamp(backup.stat().st_mtime)
        print(f"  {backup.name} ({size:.2f} KB) - {mtime.strftime('%Y-%m-%d %H:%M:%S')}")

def create_automated_backup_script():
    """Create automated backup script for cron"""
    script_content = """#!/bin/bash
# Automated backup script for Vlasia Blog database
# Add this to crontab: 0 2 * * * /path/to/backup_script.sh

BACKUP_DIR="/var/backups/vlasia_blog"
LOG_FILE="/var/log/vlasia_backup.log"
DATE=$(date +%Y%m%d_%H%M%S)

# Create backup directory
mkdir -p $BACKUP_DIR

# Set database credentials (replace with actual values)
DB_HOST="localhost"
DB_PORT="5432"
DB_NAME="vlasia_blog"
DB_USER="vlasia_user"
DB_PASS="your_password_here"

# Create backup
echo "$(date): Starting backup..." >> $LOG_FILE
pg_dump --host=$DB_HOST --port=$DB_PORT --dbname=$DB_NAME --username=$DB_USER --verbose --clean --no-owner --no-privileges --file=$BACKUP_DIR/vlasia_blog_backup_$DATE.sql >> $LOG_FILE 2>&1

if [ $? -eq 0 ]; then
    echo "$(date): Backup completed successfully" >> $LOG_FILE
    
    # Compress backup
    gzip $BACKUP_DIR/vlasia_blog_backup_$DATE.sql
    
    # Keep only last 7 backups
    cd $BACKUP_DIR
    ls -t vlasia_blog_backup_*.sql.gz | tail -n +8 | xargs -r rm
    
    echo "$(date): Backup compressed and old backups cleaned" >> $LOG_FILE
else
    echo "$(date): Backup failed!" >> $LOG_FILE
fi
"""
    
    with open('automated_backup.sh', 'w') as f:
        f.write(script_content)
    
    # Make it executable
    os.chmod('automated_backup.sh', 0o755)
    print("✅ Created automated backup script")

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Vlasia Blog Database Backup Tool')
    parser.add_argument('action', choices=['backup', 'restore', 'list', 'setup'], 
                       help='Action to perform')
    parser.add_argument('--host', default='localhost', help='Database host')
    parser.add_argument('--port', default='5432', help='Database port')
    parser.add_argument('--database', default='vlasia_blog', help='Database name')
    parser.add_argument('--username', default='vlasia_user', help='Database username')
    parser.add_argument('--password', help='Database password')
    parser.add_argument('--backup-file', help='Backup file for restore')
    parser.add_argument('--backup-dir', default='backups', help='Backup directory')
    
    args = parser.parse_args()
    
    if args.action == 'backup':
        backup_database(
            host=args.host,
            port=args.port,
            database=args.database,
            username=args.username,
            password=args.password,
            backup_dir=args.backup_dir
        )
    elif args.action == 'restore':
        if not args.backup_file:
            print("❌ --backup-file is required for restore action")
            sys.exit(1)
        restore_database(
            backup_file=args.backup_file,
            host=args.host,
            port=args.port,
            database=args.database,
            username=args.username,
            password=args.password
        )
    elif args.action == 'list':
        list_backups(args.backup_dir)
    elif args.action == 'setup':
        create_automated_backup_script()

if __name__ == "__main__":
    main()
