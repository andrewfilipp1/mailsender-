#!/usr/bin/env python3
"""
Test script για το Resend API integration
Resend: 3,000 emails/month δωρεάν, πολύ απλό API
"""

import os
import sys
import requests
import json

# Load environment variables first
import env_config

def test_resend_config():
    """Test Resend configuration"""
    print("=== Testing Resend Configuration ===")
    print("Note: You need to set RESEND_API_KEY environment variable")
    print(f"RESEND_API_KEY: {'*' * len(os.environ.get('RESEND_API_KEY', ''))}")
    print(f"MAIL_USERNAME: {os.environ.get('MAIL_USERNAME', 'Not found')}")
    print()

def test_resend_api():
    """Test Resend API"""
    print("=== Testing Resend API ===")
    
    api_key = os.environ.get('RESEND_API_KEY')
    if not api_key:
        print("❌ RESEND_API_KEY not found")
        print("To get a free Resend API key:")
        print("1. Go to https://resend.com/")
        print("2. Sign up for free account")
        print("3. Get API key from API Keys section")
        print("4. Set RESEND_API_KEY in env_config.py")
        print("5. Verify your domain or use resend.dev for testing")
        return
    
    try:
        url = "https://api.resend.com/emails"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "from": "Vlasia Blog <onboarding@resend.dev>",
            "to": ["vlasia.blog@gmail.com"],
            "subject": "Test Email από το Resend API",
            "html": """
            <h2>Test Email από το Resend API</h2>
            <p>Αυτό είναι ένα test email για να δω αν λειτουργεί το Resend API.</p>
            <p>Με εκτίμηση,<br>Η ομάδα της Βλασίας</p>
            """,
            "text": """
            Test Email από το Resend API
            
            Αυτό είναι ένα test email για να δω αν λειτουργεί το Resend API.
            
            Με εκτίμηση,
            Η ομάδα της Βλασίας
            """
        }
        
        response = requests.post(url, headers=headers, json=data)
        
        if response.status_code == 201:
            print("✅ Resend API test email sent successfully!")
            result = response.json()
            print(f"Email ID: {result.get('id', 'N/A')}")
        else:
            print(f"❌ Resend API error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Resend API error: {e}")
    print()

if __name__ == "__main__":
    test_resend_config()
    test_resend_api()
    print("=== Resend Test Complete ===")
