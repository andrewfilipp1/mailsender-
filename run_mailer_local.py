#!/usr/bin/env python3
"""
Local Newsletter Mailer Runner
Run this script locally to send newsletters manually
"""

import os
import sys
from pathlib import Path

# Add the newsletter_mailer directory to Python path
sys.path.insert(0, str(Path(__file__).parent / 'newsletter_mailer'))

def load_env_file():
    """Load environment variables from config.env file if it exists"""
    env_file = Path(__file__).parent / 'config.env'
    if env_file.exists():
        print(f"📁 Loading environment from {env_file}")
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip().strip('"\'')
        print("✅ Environment variables loaded")
    else:
        print("⚠️ No config.env file found. Using system environment variables.")

def run_mailer():
    """Run the newsletter mailer"""
    try:
        from mailer import NewsletterMailer
        
        print("🚀 Starting Newsletter Mailer...")
        print("=" * 50)
        
        # Create and run mailer
        mailer = NewsletterMailer()
        mailer.run()
        
        print("=" * 50)
        print("🎯 Newsletter Mailer completed!")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure you're running this from the correct directory")
    except Exception as e:
        print(f"❌ Mailer failed: {e}")

if __name__ == "__main__":
    print("📧 Newsletter Mailer - Local Runner")
    print()
    
    # Load environment variables
    load_env_file()
    
    # Check required environment variables
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
        print("❌ Missing required environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\nPlease set these variables in your .env file or system environment.")
        print("\nExample .env file:")
        print("API_URL_GET_EMAILS=http://localhost:5001/api/get-newsletter-batch")
        print("API_URL_MARK_SENT=http://localhost:5001/api/mark-email-sent")
        print("API_SECRET_KEY=owsz_hfbw_pycx_ngfq")
        print("SMTP_SERVER=smtp.gmail.com")
        print("SMTP_PORT=587")
        print("SMTP_USERNAME=vlasia.blog@gmail.com")
        print("SMTP_PASSWORD=owsz hfbw pycx ngfq")
        print("SENDER_EMAIL=vlasia.blog@gmail.com")
    else:
        print("✅ All required environment variables are set")
        print()
        run_mailer()
