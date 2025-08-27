#!/usr/bin/env python3
"""
Backup script for Vlasia Blog before Digital Ocean deployment
This script creates a backup of the current SQLite database and prepares data for PostgreSQL
"""
import sqlite3
import json
import os
from datetime import datetime

def backup_sqlite_data():
    """Backup all data from SQLite database"""
    backup_dir = "deployment_backup"
    os.makedirs(backup_dir, exist_ok=True)
    
    # Connect to SQLite database
    conn = sqlite3.connect('vlasia.db')
    cursor = conn.cursor()
    
    # Get all table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    backup_data = {}
    
    print("📊 Backing up database tables...")
    
    for table in tables:
        table_name = table[0]
        print(f"  - Backing up table: {table_name}")
        
        # Get table schema
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        
        # Get all data
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        
        # Store table data
        backup_data[table_name] = {
            'columns': [col[1] for col in columns],
            'data': rows
        }
    
    # Save backup to JSON file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = os.path.join(backup_dir, f"vlasia_backup_{timestamp}.json")
    
    with open(backup_file, 'w', encoding='utf-8') as f:
        json.dump(backup_data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Database backup saved to: {backup_file}")
    
    # Create SQL insert statements for PostgreSQL
    sql_file = os.path.join(backup_dir, f"vlasia_postgresql_{timestamp}.sql")
    
    with open(sql_file, 'w', encoding='utf-8') as f:
        f.write("-- PostgreSQL Insert Statements for Vlasia Blog\n")
        f.write(f"-- Generated on: {datetime.now().isoformat()}\n\n")
        
        for table_name, table_info in backup_data.items():
            if table_info['data']:
                f.write(f"\n-- Table: {table_name}\n")
                
                for row in table_info['data']:
                    # Handle different data types
                    formatted_values = []
                    for value in row:
                        if value is None:
                            formatted_values.append('NULL')
                        elif isinstance(value, str):
                            # Escape single quotes
                            escaped_value = value.replace("'", "''")
                            formatted_values.append(f"'{escaped_value}'")
                        elif isinstance(value, int):
                            formatted_values.append(str(value))
                        elif isinstance(value, float):
                            formatted_values.append(str(value))
                        else:
                            formatted_values.append(f"'{str(value)}'")
                    
                    columns_str = ', '.join(table_info['columns'])
                    values_str = ', '.join(formatted_values)
                    
                    f.write(f"INSERT INTO {table_name} ({columns_str}) VALUES ({values_str});\n")
    
    print(f"✅ PostgreSQL SQL file created: {sql_file}")
    
    # Create summary
    summary_file = os.path.join(backup_dir, f"backup_summary_{timestamp}.txt")
    
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write("Vlasia Blog Database Backup Summary\n")
        f.write("=" * 40 + "\n")
        f.write(f"Backup Date: {datetime.now().isoformat()}\n\n")
        
        for table_name, table_info in backup_data.items():
            f.write(f"Table: {table_name}\n")
            f.write(f"  Columns: {len(table_info['columns'])}\n")
            f.write(f"  Rows: {len(table_info['data'])}\n")
            f.write(f"  Columns: {', '.join(table_info['columns'])}\n\n")
    
    print(f"✅ Backup summary created: {summary_file}")
    
    conn.close()
    
    return backup_file, sql_file, summary_file

def create_deployment_checklist():
    """Create a deployment checklist"""
    checklist = """# Digital Ocean Deployment Checklist

## Pre-Deployment
- [ ] Database backup completed
- [ ] All files committed to git
- [ ] Requirements.txt updated
- [ ] Environment variables configured

## Server Setup
- [ ] Ubuntu 22.04 droplet created
- [ ] SSH access configured
- [ ] System updated
- [ ] Python, Nginx, PostgreSQL installed

## Database Migration
- [ ] PostgreSQL database created
- [ ] Database user created with proper permissions
- [ ] Data migrated from SQLite backup
- [ ] Database connection tested

## Application Deployment
- [ ] Application files uploaded to server
- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] Environment variables set
- [ ] Database tables created
- [ ] Gunicorn service configured and started

## Web Server
- [ ] Nginx configuration updated
- [ ] Site enabled
- [ ] Configuration tested
- [ ] Nginx restarted

## Security & SSL
- [ ] Firewall configured
- [ ] SSL certificate obtained (optional)
- [ ] HTTPS redirect configured (if SSL)

## Testing
- [ ] Homepage loads correctly
- [ ] All pages accessible
- [ ] Admin panel working
- [ ] File uploads working
- [ ] Database persistence verified

## Post-Deployment
- [ ] Monitor logs for errors
- [ ] Set up automated backups
- [ ] Configure monitoring
- [ ] Update DNS records
"""
    
    with open("deployment_checklist.md", 'w', encoding='utf-8') as f:
        f.write(checklist)
    
    print("✅ Deployment checklist created: deployment_checklist.md")

def main():
    """Main backup function"""
    print("🚀 Starting deployment preparation...")
    
    try:
        backup_file, sql_file, summary_file = backup_sqlite_data()
        create_deployment_checklist()
        
        print("\n🎉 Deployment preparation completed successfully!")
        print(f"\n📁 Backup files created in 'deployment_backup' directory:")
        print(f"  - Database backup: {os.path.basename(backup_file)}")
        print(f"  - PostgreSQL SQL: {os.path.basename(sql_file)}")
        print(f"  - Backup summary: {os.path.basename(summary_file)}")
        print(f"  - Deployment checklist: deployment_checklist.md")
        
        print("\n📋 Next steps:")
        print("1. Review the backup files")
        print("2. Follow the deployment checklist")
        print("3. Set up your Digital Ocean droplet")
        print("4. Use the PostgreSQL SQL file to migrate data")
        
    except Exception as e:
        print(f"❌ Error during backup: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
