# Digital Ocean Deployment Checklist

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
