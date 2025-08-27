import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Base configuration class"""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key-change-this-in-production')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = 'static/uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    
    # Email configuration
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'True').lower() == 'true'
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME', 'vlasia.blog@gmail.com')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', 'nxwh upvi kges tfqd')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER', 'vlasia.blog@gmail.com')

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///vlasia.db'

class ProductionConfig(Config):
    """Production configuration for Digital Ocean"""
    DEBUG = False
    
    # Use PostgreSQL in production
    database_url = os.environ.get('DATABASE_URL')
    if database_url and database_url != 'postgresql://username:password@host:port/database_name':
        SQLALCHEMY_DATABASE_URI = database_url
    else:
        # Fallback to SQLite if no valid DATABASE_URL is set
        SQLALCHEMY_DATABASE_URI = 'sqlite:///vlasia.db'

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
