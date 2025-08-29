#!/usr/bin/env python3
"""
Test script for Newsletter Mailer
Run this locally to test the mailer functionality
"""

import os
import sys
from pathlib import Path

# Add the newsletter_mailer directory to Python path
sys.path.insert(0, str(Path(__file__).parent / 'newsletter_mailer'))

# Load configuration from config.env
def load_config():
    config_file = Path(__file__).parent / 'config.env'
    if config_file.exists():
        print(f"📁 Loading configuration from {config_file}")
        with open(config_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip().strip('"\'')
        print("✅ Configuration loaded")
    else:
        print("⚠️ No config.env file found, using default values")

# Load configuration
load_config()

# Set test environment variables (with fallbacks)
os.environ.update({
    'API_URL_GET_EMAILS': os.getenv('API_URL_GET_EMAILS', 'http://localhost:5001/api/get-newsletter-batch'),
    'API_URL_MARK_SENT': os.getenv('API_URL_MARK_SENT', 'http://localhost:5001/api/mark-email-sent'),
    'API_SECRET_KEY': os.getenv('NEWSLETTER_API_KEY', 'owsz_hfbw_pycx_ngfq'),
    'SMTP_SERVER': os.getenv('SMTP_SERVER', 'smtp.gmail.com'),
    'SMTP_PORT': os.getenv('SMTP_PORT', '587'),
    'SMTP_USERNAME': os.getenv('SMTP_USERNAME', 'vlasia.blog@gmail.com'),
    'SMTP_PASSWORD': os.getenv('SMTP_PASSWORD', 'owsz hfbw pycx ngfq'),
    'SENDER_EMAIL': os.getenv('SENDER_EMAIL', 'vlasia.blog@gmail.com')
})

def test_mailer():
    """Test the newsletter mailer locally"""
    try:
        from mailer import NewsletterMailer
        
        print("🧪 Testing Newsletter Mailer...")
        print("=" * 50)
        
        # Test configuration validation
        print("1. Testing configuration...")
        mailer = NewsletterMailer()
        print("✅ Configuration OK")
        
        # Test API connection (this will fail if the site is not accessible)
        print("\n2. Testing API connection...")
        try:
            data = mailer.get_newsletter_data()
            if data:
                print(f"✅ API connection OK - Found {len(data.get('recipients', []))} recipients")
            else:
                print("⚠️ API connection failed - Check your API endpoints")
        except Exception as e:
            print(f"❌ API connection error: {e}")
        
        # Test SMTP connection
        print("\n3. Testing SMTP connection...")
        try:
            import smtplib
            server = smtplib.SMTP(mailer.smtp_server, mailer.smtp_port)
            server.starttls()
            server.login(mailer.smtp_username, mailer.smtp_password)
            server.quit()
            print("✅ SMTP connection OK")
        except Exception as e:
            print(f"❌ SMTP connection error: {e}")
            print("   Make sure you have the correct SMTP credentials")
        
        print("\n" + "=" * 50)
        print("🎯 Test completed!")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure you're running this from the correct directory")
    except Exception as e:
        print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    print("📧 Newsletter Mailer Test Script")
    print("Make sure to update the environment variables in this script first!")
    print()
    
    # Check if environment variables are set
    required_vars = [
        'API_URL_GET_EMAILS',
        'API_URL_MARK_SENT', 
        'API_SECRET_KEY',
        'SMTP_USERNAME',
        'SMTP_PASSWORD',
        'SENDER_EMAIL'
    ]
    
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print("❌ Missing environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\nPlease update the script with your actual values first!")
    else:
        test_mailer()
