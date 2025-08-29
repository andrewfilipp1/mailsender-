#!/usr/bin/env python3
"""
Create test newsletter subscriber for testing
"""

import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Load configuration
from dotenv import load_dotenv
load_dotenv('config.env')

# Import Flask app and database
from app import app, db, NewsletterSubscriber

def create_test_subscriber():
    """Create a test newsletter subscriber"""
    with app.app_context():
        try:
            # Check if test subscriber already exists
            existing = NewsletterSubscriber.query.filter_by(
                email="test@vlasia-blog.com"
            ).first()
            
            if existing:
                print(f"✅ Test subscriber already exists with ID: {existing.id}")
                return existing.id
            
            # Create new test subscriber
            test_subscriber = NewsletterSubscriber(
                email="test@vlasia-blog.com"
            )
            
            db.session.add(test_subscriber)
            db.session.commit()
            
            print(f"✅ Test subscriber created successfully with ID: {test_subscriber.id}")
            print(f"   Email: {test_subscriber.email}")
            print(f"   Subscribed at: {test_subscriber.subscribed_at}")
            print(f"   Active: {test_subscriber.is_active}")
            
            return test_subscriber.id
            
        except Exception as e:
            print(f"❌ Error creating test subscriber: {e}")
            db.session.rollback()
            return None

def list_all_subscribers():
    """List all newsletter subscribers"""
    with app.app_context():
        try:
            subscribers = NewsletterSubscriber.query.filter_by(is_active=True).all()
            print(f"\n📧 Active Newsletter Subscribers ({len(subscribers)}):")
            print("-" * 50)
            
            for sub in subscribers:
                print(f"ID: {sub.id} | Email: {sub.email} | Active: {sub.is_active}")
            
            return subscribers
            
        except Exception as e:
            print(f"❌ Error listing subscribers: {e}")
            return []

if __name__ == "__main__":
    print("🎯 Creating test newsletter subscriber...")
    subscriber_id = create_test_subscriber()
    
    if subscriber_id:
        print(f"\n🎉 Test subscriber ready! ID: {subscriber_id}")
        
        # List all subscribers
        list_all_subscribers()
        
        print("\nNow you can test the newsletter system!")
    else:
        print("\n❌ Failed to create test subscriber")
