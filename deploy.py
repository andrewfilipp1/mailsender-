#!/usr/bin/env python3
"""
Deployment script for Vlasia Village Website
This script helps set up the website for production deployment
"""

import os
import secrets
import sqlite3
from pathlib import Path

def generate_secret_key():
    """Generate a secure secret key for production"""
    return secrets.token_hex(32)

def create_production_config():
    """Create production configuration file"""
    config_content = '''# Production Configuration for Vlasia Website
# Copy this to your production environment

# Flask Configuration
FLASK_ENV=production
SECRET_KEY={secret_key}
DEBUG=False

# Database Configuration
DATABASE_URL=postgresql://username:password@localhost/vlasia_db
# or for MySQL:
# DATABASE_URL=mysql://username:password@localhost/vlasia_db

# File Upload Configuration
MAX_CONTENT_LENGTH=16777216  # 16MB
UPLOAD_FOLDER=static/uploads

# Security Configuration
WTF_CSRF_ENABLED=True
SESSION_COOKIE_SECURE=True
SESSION_COOKIE_HTTPONLY=True
PERMANENT_SESSION_LIFETIME=3600

# Logging Configuration
LOG_LEVEL=INFO
LOG_FILE=logs/vlasia.log
'''.format(secret_key=generate_secret_key())
    
    with open('production.env', 'w') as f:
        f.write(config_content)
    
    print("✅ Production configuration file created: production.env")

def create_wsgi_file():
    """Create WSGI file for production servers"""
    wsgi_content = '''#!/usr/bin/env python3
"""
WSGI entry point for Vlasia Website
Use this file with Gunicorn, uWSGI, or other WSGI servers
"""

from app import app

if __name__ == "__main__":
    app.run()
'''
    
    with open('wsgi.py', 'w') as f:
        f.write(wsgi_content)
    
    print("✅ WSGI file created: wsgi.py")

def create_gunicorn_config():
    """Create Gunicorn configuration file"""
    gunicorn_content = '''# Gunicorn configuration for Vlasia Website
bind = "0.0.0.0:8000"
workers = 4
worker_class = "sync"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 100
timeout = 30
keepalive = 2
preload_app = True
'''
    
    with open('gunicorn.conf.py', 'w') as f:
        f.write(gunicorn_content)
    
    print("✅ Gunicorn configuration created: gunicorn.conf.py")

def create_nginx_config():
    """Create Nginx configuration template"""
    nginx_content = '''# Nginx configuration for Vlasia Website
# Place this in /etc/nginx/sites-available/vlasia

server {
    listen 80;
    server_name www.vlasia.gr vlasia.gr;
    
    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name www.vlasia.gr vlasia.gr;
    
    # SSL Configuration
    ssl_certificate /path/to/your/certificate.crt;
    ssl_certificate_key /path/to/your/private.key;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;
    
    # Security headers
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    
    # Static files
    location /static/ {
        alias /path/to/your/vlasia-website/static/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
    
    # Proxy to Gunicorn
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }
    
    # Upload size limit
    client_max_body_size 16M;
}
'''
    
    with open('nginx.conf', 'w') as f:
        f.write(nginx_content)
    
    print("✅ Nginx configuration template created: nginx.conf")

def create_systemd_service():
    """Create systemd service file"""
    service_content = '''[Unit]
Description=Vlasia Website Gunicorn Service
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/your/vlasia-website
Environment="PATH=/path/to/your/vlasia-website/venv/bin"
ExecStart=/path/to/your/vlasia-website/venv/bin/gunicorn --config gunicorn.conf.py wsgi:app
ExecReload=/bin/kill -s HUP $MAINPID
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
'''
    
    with open('vlasia.service', 'w') as f:
        f.write(service_content)
    
    print("✅ Systemd service file created: vlasia.service")

def create_deployment_script():
    """Create deployment script"""
    deploy_script = '''#!/bin/bash
# Deployment script for Vlasia Website
# Run this script on your production server

echo "🚀 Starting Vlasia Website deployment..."

# Update system packages
echo "📦 Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install required packages
echo "🔧 Installing required packages..."
sudo apt install -y python3 python3-pip python3-venv nginx certbot python3-certbot-nginx

# Create application directory
echo "📁 Creating application directory..."
sudo mkdir -p /var/www/vlasia
sudo chown $USER:$USER /var/www/vlasia

# Copy application files
echo "📋 Copying application files..."
cp -r . /var/www/vlasia/
cd /var/www/vlasia

# Create virtual environment
echo "🐍 Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo "📚 Installing Python dependencies..."
pip install -r requirements.txt
pip install gunicorn

# Set up environment variables
echo "⚙️ Setting up environment variables..."
cp production.env .env
source .env

# Create uploads directory
echo "📁 Creating uploads directory..."
mkdir -p static/uploads
chmod 755 static/uploads

# Set up Nginx
echo "🌐 Setting up Nginx..."
sudo cp nginx.conf /etc/nginx/sites-available/vlasia
sudo ln -sf /etc/nginx/sites-available/vlasia /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Set up systemd service
echo "🔧 Setting up systemd service..."
sudo cp vlasia.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable vlasia
sudo systemctl start vlasia

# Test Nginx configuration
echo "🧪 Testing Nginx configuration..."
sudo nginx -t

# Restart Nginx
echo "🔄 Restarting Nginx..."
sudo systemctl restart nginx

# Set up SSL certificate
echo "🔒 Setting up SSL certificate..."
sudo certbot --nginx -d www.vlasia.gr -d vlasia.gr

echo "✅ Deployment completed successfully!"
echo "🌐 Your website should be available at: https://www.vlasia.gr"
echo "🔧 To check service status: sudo systemctl status vlasia"
echo "📝 To view logs: sudo journalctl -u vlasia -f"
'''
    
    with open('deploy.sh', 'w') as f:
        f.write(deploy_script)
    
    # Make script executable
    os.chmod('deploy.sh', 0o755)
    print("✅ Deployment script created: deploy.sh")

def create_docker_files():
    """Create Docker configuration files"""
    dockerfile = '''# Dockerfile for Vlasia Website
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    gcc \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

# Copy application code
COPY . .

# Create uploads directory
RUN mkdir -p static/uploads && chmod 755 static/uploads

# Expose port
EXPOSE 8000

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "wsgi:app"]
'''
    
    docker_compose = '''# Docker Compose for Vlasia Website
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - FLASK_ENV=production
      - SECRET_KEY=your-secret-key-here
    volumes:
      - ./static/uploads:/app/static/uploads
    restart: unless-stopped
  
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/conf.d/default.conf
      - ./static:/var/www/static
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - web
    restart: unless-stopped
'''
    
    with open('Dockerfile', 'w') as f:
        f.write(dockerfile)
    
    with open('docker-compose.yml', 'w') as f:
        f.write(docker_compose)
    
    print("✅ Docker files created: Dockerfile, docker-compose.yml")

def main():
    """Main deployment setup function"""
    print("🌲 Vlasia Website - Production Deployment Setup")
    print("=" * 50)
    
    # Create necessary directories
    os.makedirs('logs', exist_ok=True)
    os.makedirs('ssl', exist_ok=True)
    
    # Generate configuration files
    create_production_config()
    create_wsgi_file()
    create_gunicorn_config()
    create_nginx_config()
    create_systemd_service()
    create_deployment_script()
    create_docker_files()
    
    print("\n🎉 Production setup completed!")
    print("\n📋 Next steps:")
    print("1. Review and customize the generated configuration files")
    print("2. Update the domain names in nginx.conf")
    print("3. Set up your SSL certificates")
    print("4. Run the deployment script on your production server")
    print("5. Update your DNS records to point to your server")
    
    print("\n📚 Documentation:")
    print("- README.md - Complete project documentation")
    print("- production.env - Environment variables template")
    print("- deploy.sh - Automated deployment script")
    print("- nginx.conf - Web server configuration")
    print("- vlasia.service - System service configuration")

if __name__ == "__main__":
    main()
