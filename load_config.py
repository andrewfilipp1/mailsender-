#!/usr/bin/env python3
"""
Load configuration from config.env file
"""

import os

def load_config():
    """Load configuration from config.env file"""
    config_file = 'config.env'
    if os.path.exists(config_file):
        print(f"📁 Loading configuration from {config_file}")
        with open(config_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip().strip('"\'')
        print("✅ Configuration loaded successfully")
        return True
    else:
        print(f"❌ Configuration file {config_file} not found")
        return False

if __name__ == "__main__":
    load_config()
    print("\nCurrent environment variables:")
    for key in ['NEWSLETTER_API_KEY', 'SMTP_USERNAME', 'SENDER_EMAIL']:
        value = os.getenv(key, 'NOT SET')
        print(f"  {key}: {value}")
