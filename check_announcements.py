#!/usr/bin/env python3
"""
Check announcements and newsletter subscribers
"""

from app import app, db
from app import Announcement, NewsletterSubscriber

def check_announcements():
    with app.app_context():
        print("🔍 Checking announcements and newsletter...")
        
        # Check announcements
        announcements = Announcement.query.all()
        print(f"📢 Total announcements: {len(announcements)}")
        
        for a in announcements:
            print(f"  - {a.title}")
            print(f"    Category: {a.category}")
            print(f"    Priority: {a.priority}")
            print(f"    Published: {a.is_published}")
            print(f"    Sent to newsletter: {a.sent_to_newsletter}")
            print(f"    Created: {a.created_at}")
            print()
        
        # Check newsletter subscribers
        subscribers = NewsletterSubscriber.query.filter_by(is_active=True).all()
        print(f"📧 Active newsletter subscribers: {len(subscribers)}")
        
        for s in subscribers[:5]:  # Show first 5
            print(f"  - {s.email} (welcome sent: {s.welcome_email_sent})")
        
        if len(subscribers) > 5:
            print(f"  ... and {len(subscribers) - 5} more")

if __name__ == "__main__":
    check_announcements()
