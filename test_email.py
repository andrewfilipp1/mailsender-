#!/usr/bin/env python3
"""
Test script για το email functionality της εφαρμογής
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set environment variables for testing
os.environ['MAIL_SERVER'] = 'smtp.gmail.com'
os.environ['MAIL_PORT'] = '587'
os.environ['MAIL_USE_TLS'] = 'True'
os.environ['MAIL_USE_SSL'] = 'False'
os.environ['MAIL_USERNAME'] = 'vlasia.blog@gmail.com'
os.environ['MAIL_PASSWORD'] = 'nxwh upvi kges tfqd'
os.environ['MAIL_DEFAULT_SENDER'] = 'vlasia.blog@gmail.com'

# Import Flask app
from app import app, send_contact_email, send_welcome_email

def test_email_config():
    """Test email configuration"""
    print("=== Testing Email Configuration ===")
    print(f"MAIL_SERVER: {app.config.get('MAIL_SERVER')}")
    print(f"MAIL_PORT: {app.config.get('MAIL_PORT')}")
    print(f"MAIL_USE_TLS: {app.config.get('MAIL_USE_TLS')}")
    print(f"MAIL_USE_SSL: {app.config.get('MAIL_USE_SSL')}")
    print(f"MAIL_USERNAME: {app.config.get('MAIL_USERNAME')}")
    print(f"MAIL_PASSWORD: {'*' * len(app.config.get('MAIL_PASSWORD', ''))}")
    print(f"MAIL_DEFAULT_SENDER: {app.config.get('MAIL_DEFAULT_SENDER')}")
    print()

def test_contact_email():
    """Test contact email sending"""
    print("=== Testing Contact Email ===")
    try:
        result = send_contact_email(
            first_name="Test",
            last_name="User",
            email="test@example.com",
            subject="Test Message",
            message="This is a test message from the email test script."
        )
        if result:
            print("✅ Contact email sent successfully!")
        else:
            print("❌ Contact email failed to send")
    except Exception as e:
        print(f"❌ Error sending contact email: {e}")
    print()

def test_welcome_email():
    """Test welcome email sending"""
    print("=== Testing Welcome Email ===")
    try:
        result = send_welcome_email("test@example.com")
        if result:
            print("✅ Welcome email sent successfully!")
        else:
            print("❌ Welcome email failed to send")
    except Exception as e:
        print(f"❌ Error sending welcome email: {e}")
    print()

if __name__ == "__main__":
    with app.app_context():
        test_email_config()
        test_contact_email()
        test_welcome_email()
    
    print("=== Email Test Complete ===")
