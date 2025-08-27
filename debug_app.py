#!/usr/bin/env python3
"""
Debug script to check Flask app configuration
"""

import os
from dotenv import load_dotenv

def debug_app_config():
    """Debug Flask app configuration"""
    print("🔍 Debugging Flask app configuration...")
    
    # Load environment variables
    print("📥 Loading .env file...")
    load_dotenv()
    
    # Check environment variables
    print(f"\n🌍 Environment variables:")
    print(f"   FLASK_ENV: {os.environ.get('FLASK_ENV', 'NOT SET')}")
    print(f"   SECRET_KEY: {os.environ.get('SECRET_KEY', 'NOT SET')}")
    
    # Import config
    print(f"\n📋 Importing config...")
    try:
        from config import config
        
        # Check config
        config_name = os.environ.get('FLASK_ENV', 'development')
        print(f"   Config name: {config_name}")
        
        # Get config class
        config_class = config[config_name]
        print(f"   Config class: {config_class}")
        
        # Check SECRET_KEY in config
        secret_key = config_class.SECRET_KEY
        print(f"   Config SECRET_KEY: {secret_key}")
        
        if secret_key and secret_key != 'your-secret-key-change-this-in-production':
            print("✅ SECRET_KEY is properly set in config")
        else:
            print("❌ SECRET_KEY is not properly set in config")
            
    except Exception as e:
        print(f"❌ Error importing config: {e}")

if __name__ == '__main__':
    debug_app_config()
