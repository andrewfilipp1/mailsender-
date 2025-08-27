# Digital Ocean Deployment Guide for Vlasia Blog

## 1. Create Droplet
- Create a new Ubuntu 22.04 LTS droplet
- Choose your preferred size (1GB RAM minimum recommended)
- Add your SSH key

## 2. Connect to Droplet
```bash
ssh root@your-droplet-ip
```

## 3. Update System
```bash
apt update && apt upgrade -y
```

## 4. Install Dependencies
```bash
# Install Python and pip
apt install python3 python3-pip python3-venv nginx postgresql postgresql-contrib -y

# Install additional packages
apt install build-essential python3-dev libpq-dev -y
```

## 5. Setup PostgreSQL
```bash
# Switch to postgres user
sudo -u postgres psql

# Create database and user
CREATE DATABASE vlasia_blog;
CREATE USER vlasia_user WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE vlasia_blog TO vlasia_user;
\q

# Update PostgreSQL configuration
sudo nano /etc/postgresql/*/main/postgresql.conf
# Uncomment and set: listen_addresses = 'localhost'
sudo nano /etc/postgresql/*/main/pg_hba.conf
# Add: host vlasia_blog vlasia_user 127.0.0.1/32 md5

# Restart PostgreSQL
sudo systemctl restart postgresql
```

## 6. Deploy Application
```bash
# Create application directory
mkdir -p /var/www/vlasia_blog
cd /var/www/vlasia_blog

# Clone your repository or upload files
# git clone your-repo-url .

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install requirements
pip install -r requirements.txt

# Create .env file with your database URL
nano .env
# DATABASE_URL=postgresql://vlasia_user:your_secure_password@localhost:5432/vlasia_blog

# Initialize database
python3 -c "from app import app, db; app.app_context().push(); db.create_all()"
```

## 7. Setup Gunicorn
```bash
# Copy service file
sudo cp vlasia_blog.service /etc/systemd/system/

# Edit service file with correct paths
sudo nano /etc/systemd/system/vlasia_blog.service

# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable vlasia_blog
sudo systemctl start vlasia_blog
```

## 8. Setup Nginx
```bash
# Copy Nginx configuration
sudo cp nginx_vlasia.conf /etc/nginx/sites-available/vlasia_blog

# Edit configuration with correct paths and domain
sudo nano /etc/nginx/sites-available/vlasia_blog

# Enable site
sudo ln -s /etc/nginx/sites-available/vlasia_blog /etc/nginx/sites-enabled/

# Test configuration
sudo nginx -t

# Restart Nginx
sudo systemctl restart nginx
```

## 9. Setup Firewall
```bash
# Allow SSH, HTTP, and HTTPS
ufw allow ssh
ufw allow 80
ufw allow 443
ufw enable
```

## 10. Setup SSL (Optional but Recommended)
```bash
# Install Certbot
apt install certbot python3-certbot-nginx -y

# Get SSL certificate
certbot --nginx -d your-domain.com
```

## 11. Test Application
- Visit your domain in browser
- Check logs: sudo journalctl -u vlasia_blog
- Check Nginx logs: sudo tail -f /var/log/nginx/error.log

## Important Notes:
- Replace all placeholder values (paths, passwords, domain names)
- Keep your .env file secure and never commit it to version control
- Regularly backup your PostgreSQL database
- Monitor your application logs for errors
- Consider setting up automated backups
