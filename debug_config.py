#!/usr/bin/env python3
"""
Debug script to check configuration loading
"""

import os
from dotenv import load_dotenv

def debug_config():
    """Debug configuration loading"""
    print("🔍 Debugging configuration...")
    
    # Check current working directory
    print(f"📁 Current working directory: {os.getcwd()}")
    
    # Check if .env file exists
    env_file = '.env'
    if os.path.exists(env_file):
        print(f"✅ .env file exists: {env_file}")
        
        # Read .env file content
        with open(env_file, 'r') as f:
            content = f.read()
            print(f"📄 .env content:\n{content}")
    else:
        print(f"❌ .env file not found: {env_file}")
    
    # Check environment variables before load_dotenv
    print(f"\n🌍 Environment variables before load_dotenv:")
    print(f"   FLASK_ENV: {os.environ.get('FLASK_ENV', 'NOT SET')}")
    print(f"   SECRET_KEY: {os.environ.get('SECRET_KEY', 'NOT SET')}")
    
    # Load .env file
    print(f"\n📥 Loading .env file...")
    load_dotenv()
    
    # Check environment variables after load_dotenv
    print(f"\n🌍 Environment variables after load_dotenv:")
    print(f"   FLASK_ENV: {os.environ.get('FLASK_ENV', 'NOT SET')}")
    print(f"   SECRET_KEY: {os.environ.get('SECRET_KEY', 'NOT SET')}")
    
    # Check if SECRET_KEY is valid
    secret_key = os.environ.get('SECRET_KEY', '')
    if secret_key and secret_key != 'your-secret-key-change-this-in-production':
        print(f"✅ SECRET_KEY is set and valid")
    else:
        print(f"❌ SECRET_KEY is not set or invalid")

if __name__ == '__main__':
    debug_config()
