# 🚀 Vlasia Blog - Digital Ocean Deployment Guide

## 📋 Overview

This guide explains how to deploy the Vlasia Blog application on Digital Ocean with **PostgreSQL database** to ensure **data persistence** and prevent data loss.

## 🔧 Why PostgreSQL Instead of SQLite?

- **Data Persistence**: PostgreSQL stores data on disk, not in memory
- **Production Ready**: Designed for high-traffic applications
- **Backup & Recovery**: Built-in backup and restore capabilities
- **Scalability**: Can handle multiple concurrent users
- **Reliability**: ACID compliance ensures data integrity

## 📁 New Files Created

1. **`config.py`** - Configuration management for different environments
2. **`wsgi.py`** - Production WSGI entry point
3. **`deploy_digital_ocean.py`** - Automated deployment setup
4. **`backup_database.py`** - Database backup and restore tool
5. **`DIGITAL_OCEAN_DEPLOYMENT.md`** - Step-by-step deployment guide

## 🚀 Quick Start

### 1. Setup Deployment Files
```bash
python3 deploy_digital_ocean.py
```

### 2. Edit Configuration
Edit the generated `.env` file with your actual database credentials:
```bash
nano .env
```

### 3. Follow Deployment Guide
Read and follow `DIGITAL_OCEAN_DEPLOYMENT.md` for complete setup.

## 🗄️ Database Setup

### PostgreSQL Installation
```bash
# Install PostgreSQL
sudo apt install postgresql postgresql-contrib -y

# Create database and user
sudo -u postgres psql
CREATE DATABASE vlasia_blog;
CREATE USER vlasia_user WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE vlasia_blog TO vlasia_user;
\q
```

### Environment Variables
```bash
# In your .env file
FLASK_ENV=production
DATABASE_URL=postgresql://vlasia_user:your_secure_password@localhost:5432/vlasia_blog
```

## 💾 Database Backup & Recovery

### Automated Backups
```bash
# Setup automated backup script
python3 backup_database.py setup

# Add to crontab (daily at 2 AM)
0 2 * * * /path/to/automated_backup.sh
```

### Manual Backups
```bash
# Create backup
python3 backup_database.py backup --username vlasia_user --password your_password

# List backups
python3 backup_database.py list

# Restore from backup
python3 backup_database.py restore --backup-file backups/vlasia_blog_backup_20240826_120000.sql --username vlasia_user --password your_password
```

## 🔒 Security Considerations

1. **Strong Passwords**: Use complex passwords for database users
2. **Environment Variables**: Never commit `.env` files to version control
3. **Firewall**: Only allow necessary ports (22, 80, 443)
4. **SSL**: Use Let's Encrypt for HTTPS
5. **Regular Updates**: Keep system and packages updated

## 📊 Monitoring & Maintenance

### Check Application Status
```bash
# Check service status
sudo systemctl status vlasia_blog

# View logs
sudo journalctl -u vlasia_blog -f

# Check Nginx status
sudo systemctl status nginx
```

### Database Maintenance
```bash
# Connect to database
psql -h localhost -U vlasia_user -d vlasia_blog

# Check table sizes
SELECT schemaname, tablename, pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size FROM pg_tables WHERE schemaname = 'public';

# Vacuum database
VACUUM ANALYZE;
```

## 🚨 Troubleshooting

### Common Issues

1. **Database Connection Failed**
   - Check PostgreSQL service: `sudo systemctl status postgresql`
   - Verify credentials in `.env` file
   - Check firewall settings

2. **Application Won't Start**
   - Check logs: `sudo journalctl -u vlasia_blog -f`
   - Verify virtual environment and dependencies
   - Check file permissions

3. **Nginx Errors**
   - Test configuration: `sudo nginx -t`
   - Check error logs: `sudo tail -f /var/log/nginx/error.log`
   - Verify file paths in configuration

### Recovery Procedures

1. **Database Corruption**
   ```bash
   # Stop application
   sudo systemctl stop vlasia_blog
   
   # Restore from latest backup
   python3 backup_database.py restore --backup-file latest_backup.sql
   
   # Restart application
   sudo systemctl start vlasia_blog
   ```

2. **Application Failure**
   ```bash
   # Check logs for errors
   sudo journalctl -u vlasia_blog -f
   
   # Restart service
   sudo systemctl restart vlasia_blog
   
   # Check status
   sudo systemctl status vlasia_blog
   ```

## 📈 Performance Optimization

1. **Database Indexing**: Add indexes for frequently queried columns
2. **Connection Pooling**: Configure PostgreSQL connection limits
3. **Caching**: Implement Redis for session storage
4. **CDN**: Use Cloudflare for static assets
5. **Load Balancing**: Consider multiple application instances

## 🔄 Migration from SQLite

If you have existing data in SQLite:

1. **Export SQLite Data**
   ```bash
   sqlite3 instance/vlasia.db .dump > sqlite_dump.sql
   ```

2. **Convert to PostgreSQL Format**
   ```bash
   # Edit sqlite_dump.sql to fix syntax differences
   # Remove SQLite-specific commands
   # Fix data types if needed
   ```

3. **Import to PostgreSQL**
   ```bash
   psql -h localhost -U vlasia_user -d vlasia_blog -f sqlite_dump.sql
   ```

## 📞 Support

- **Documentation**: Check `DIGITAL_OCEAN_DEPLOYMENT.md`
- **Logs**: Application and system logs for debugging
- **Backups**: Regular database backups for data safety
- **Monitoring**: Set up alerts for critical issues

## 🎯 Success Metrics

- ✅ Application runs without data loss
- ✅ Database survives server restarts
- ✅ Automated backups working
- ✅ SSL certificate active
- ✅ Performance monitoring in place
- ✅ Regular maintenance scheduled

---

**Remember**: PostgreSQL ensures your data is **permanently stored** and **easily recoverable**, unlike SQLite which can lose data during server restarts or deployments.
