# 🔄 Migration Guide: SQLite to PostgreSQL

## 📋 Overview

This guide helps you migrate your existing SQLite database to PostgreSQL when deploying to Digital Ocean. This ensures **no data loss** during the transition.

## 🚨 Important: Backup First!

Before starting migration, create a backup of your current SQLite database:

```bash
# Stop the application first
pkill -f "python3 app.py"

# Create backup
cp instance/vlasia.db instance/vlasia_backup_$(date +%Y%m%d_%H%M%S).db

# Verify backup
ls -la instance/vlasia_backup_*.db
```

## 🔧 Migration Steps

### Step 1: Export SQLite Data

```bash
# Export all data from SQLite
sqlite3 instance/vlasia.db .dump > sqlite_export.sql

# Check the export file
head -20 sqlite_export.sql
```

### Step 2: Clean SQLite Export

The SQLite export contains SQLite-specific commands that PostgreSQL doesn't understand. Edit `sqlite_export.sql`:

```bash
# Remove these lines from the beginning:
# PRAGMA foreign_keys=OFF;
# BEGIN TRANSACTION;

# Remove these lines from the end:
# COMMIT;

# Remove any SQLite-specific commands like:
# CREATE TABLE sqlite_sequence(...);
# INSERT INTO sqlite_sequence VALUES(...);
```

### Step 3: Fix Data Types

PostgreSQL is stricter about data types. Common fixes needed:

```sql
-- Change TEXT to VARCHAR where appropriate
-- Ensure TIMESTAMP columns have proper format
-- Fix any invalid characters in text fields
```

### Step 4: Create PostgreSQL Database

```bash
# Connect to PostgreSQL
sudo -u postgres psql

# Create database and user
CREATE DATABASE vlasia_blog;
CREATE USER vlasia_user WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE vlasia_blog TO vlasia_user;
\q
```

### Step 5: Import Data

```bash
# Import the cleaned SQL file
psql -h localhost -U vlasia_user -d vlasia_blog -f sqlite_export.sql
```

### Step 6: Verify Migration

```bash
# Connect to PostgreSQL
psql -h localhost -U vlasia_user -d vlasia_blog

# Check tables
\dt

# Check data counts
SELECT COUNT(*) FROM user;
SELECT COUNT(*) FROM news_item;
SELECT COUNT(*) FROM newsletter_subscriber;

# Check sample data
SELECT * FROM user LIMIT 3;
SELECT * FROM news_item LIMIT 3;

\q
```

## 🛠️ Automated Migration Script

For easier migration, use the provided script:

```bash
# Create migration script
cat > migrate_sqlite_to_postgres.py << 'EOF'
#!/usr/bin/env python3
"""
SQLite to PostgreSQL Migration Script
"""
import sqlite3
import psycopg2
import os
from datetime import datetime

def migrate_sqlite_to_postgres():
    # SQLite connection
    sqlite_conn = sqlite3.connect('instance/vlasia.db')
    sqlite_cursor = sqlite_conn.cursor()
    
    # PostgreSQL connection
    pg_conn = psycopg2.connect(
        host="localhost",
        database="vlasia_blog",
        user="vlasia_user",
        password="your_secure_password"
    )
    pg_cursor = pg_conn.cursor()
    
    try:
        # Migrate users
        print("🔄 Migrating users...")
        sqlite_cursor.execute("SELECT * FROM user")
        users = sqlite_cursor.fetchall()
        
        for user in users:
            pg_cursor.execute("""
                INSERT INTO "user" (id, username, email, password_hash, is_admin, created_at)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING
            """, user)
        
        # Migrate news items
        print("🔄 Migrating news items...")
        sqlite_cursor.execute("SELECT * FROM news_item")
        news_items = sqlite_cursor.fetchall()
        
        for news in news_items:
            pg_cursor.execute("""
                INSERT INTO news_item (id, title, content, media_path, media_type, is_published, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING
            """, news)
        
        # Migrate media files
        print("🔄 Migrating media files...")
        sqlite_cursor.execute("SELECT * FROM media")
        media_files = sqlite_cursor.fetchall()
        
        for media in media_files:
            pg_cursor.execute("""
                INSERT INTO media (id, filename, file_path, media_type, "order", news_item_id, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING
            """, media)
        
        # Migrate newsletter subscribers
        print("🔄 Migrating newsletter subscribers...")
        sqlite_cursor.execute("SELECT * FROM newsletter_subscriber")
        subscribers = sqlite_cursor.fetchall()
        
        for subscriber in subscribers:
            pg_cursor.execute("""
                INSERT INTO newsletter_subscriber (id, email, subscribed_at, is_active)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING
            """, subscriber)
        
        # Commit all changes
        pg_conn.commit()
        print("✅ Migration completed successfully!")
        
        # Print statistics
        pg_cursor.execute("SELECT COUNT(*) FROM \"user\"")
        user_count = pg_cursor.fetchone()[0]
        
        pg_cursor.execute("SELECT COUNT(*) FROM news_item")
        news_count = pg_cursor.fetchone()[0]
        
        pg_cursor.execute("SELECT COUNT(*) FROM media")
        media_count = pg_cursor.fetchone()[0]
        
        pg_cursor.execute("SELECT COUNT(*) FROM newsletter_subscriber")
        subscriber_count = pg_cursor.fetchone()[0]
        
        print(f"\n📊 Migration Statistics:")
        print(f"  Users: {user_count}")
        print(f"  News Items: {news_count}")
        print(f"  Media Files: {media_count}")
        print(f"  Newsletter Subscribers: {subscriber_count}")
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        pg_conn.rollback()
        raise
    finally:
        sqlite_conn.close()
        pg_conn.close()

if __name__ == "__main__":
    migrate_sqlite_to_postgres()
EOF

# Make it executable
chmod +x migrate_sqlite_to_postgres.py

# Edit the script with your actual PostgreSQL credentials
nano migrate_sqlite_to_postgres.py

# Run migration
python3 migrate_sqlite_to_postgres.py
```

## 🔍 Verification Checklist

After migration, verify:

- [ ] All users exist in PostgreSQL
- [ ] All news items are present
- [ ] Media files are linked correctly
- [ ] Newsletter subscribers are preserved
- [ ] Application can connect to PostgreSQL
- [ ] Data is accessible through the web interface

## 🚨 Common Issues & Solutions

### Issue: Data Type Mismatches
**Solution**: Check PostgreSQL logs for type errors and fix the migration script.

### Issue: Foreign Key Violations
**Solution**: Ensure tables are created in the correct order (users first, then news items, then media).

### Issue: Character Encoding Problems
**Solution**: Use UTF-8 encoding and check for special characters in text fields.

### Issue: Timestamp Format Issues
**Solution**: Ensure datetime fields are in ISO format (YYYY-MM-DD HH:MM:SS).

## 📊 Performance Comparison

| Feature | SQLite | PostgreSQL |
|---------|--------|------------|
| Data Persistence | ❌ Memory-based | ✅ Disk-based |
| Concurrent Users | ❌ Single writer | ✅ Multiple writers |
| Backup/Recovery | ❌ Manual | ✅ Automated |
| Scalability | ❌ Limited | ✅ High |
| Production Ready | ❌ No | ✅ Yes |

## 🔄 Rollback Plan

If migration fails:

1. **Stop the application**
2. **Restore SQLite backup**:
   ```bash
   cp instance/vlasia_backup_*.db instance/vlasia.db
   ```
3. **Revert environment variables**:
   ```bash
   export FLASK_ENV=development
   ```
4. **Restart with SQLite**:
   ```bash
   python3 app.py
   ```

## 📞 Support

- Check PostgreSQL logs: `sudo tail -f /var/log/postgresql/postgresql-*.log`
- Verify database connection: `psql -h localhost -U vlasia_user -d vlasia_blog`
- Test application connectivity
- Review migration script for errors

---

**Remember**: Always test migration on a copy of your data first, and keep multiple backups throughout the process!
