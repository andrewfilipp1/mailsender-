#!/usr/bin/env python3
"""
Test script για το SendGrid API integration
"""

import os
import sys
import requests
import json

# Load environment variables first
import env_config

def test_sendgrid_config():
    """Test SendGrid configuration"""
    print("=== Testing SendGrid Configuration ===")
    print("Note: You need to set SENDGRID_API_KEY environment variable")
    print(f"SENDGRID_API_KEY: {'*' * len(os.environ.get('SENDGRID_API_KEY', ''))}")
    print(f"MAIL_USERNAME: {os.environ.get('MAIL_USERNAME', 'Not found')}")
    print()

def test_sendgrid_api():
    """Test SendGrid API"""
    print("=== Testing SendGrid API ===")
    
    api_key = os.environ.get('SENDGRID_API_KEY')
    if not api_key:
        print("❌ SENDGRID_API_KEY not found")
        print("To get a free SendGrid API key:")
        print("1. Go to https://sendgrid.com/")
        print("2. Sign up for free account")
        print("3. Get API key from Settings > API Keys")
        print("4. Set SENDGRID_API_KEY in env_config.py")
        return
    
    try:
        url = "https://api.sendgrid.com/v3/mail/send"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "personalizations": [
                {
                    "to": [
                        {
                            "email": "vlasia.blog@gmail.com",
                            "name": "Vlasia Blog"
                        }
                    ]
                }
            ],
            "from": {
                "email": os.environ.get('MAIL_USERNAME', 'vlasia.blog@gmail.com'),
                "name": "Vlasia Blog"
            },
            "subject": "Test Email από το SendGrid API",
            "content": [
                {
                    "type": "text/plain",
                    "value": """
Αυτό είναι ένα test email για να δω αν λειτουργεί το SendGrid API.

Με εκτίμηση,
Η ομάδα της Βλασίας
                    """
                }
            ]
        }
        
        response = requests.post(url, headers=headers, json=data)
        
        if response.status_code == 202:
            print("✅ SendGrid API test email sent successfully!")
        else:
            print(f"❌ SendGrid API error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ SendGrid API error: {e}")
    print()

if __name__ == "__main__":
    test_sendgrid_config()
    test_sendgrid_api()
    print("=== SendGrid Test Complete ===")
