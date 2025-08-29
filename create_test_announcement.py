#!/usr/bin/env python3
"""
Create test announcement for newsletter testing
"""

import os
import sys
from datetime import datetime

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Load configuration
from dotenv import load_dotenv
load_dotenv('config.env')

# Import Flask app and database
from app import app, db, Announcement

def create_test_announcement():
    """Create a test announcement for newsletter testing"""
    with app.app_context():
        try:
            # Check if test announcement already exists
            existing = Announcement.query.filter_by(
                title="🎉 Test Newsletter - Δοκιμή Συστήματος"
            ).first()
            
            if existing:
                print(f"✅ Test announcement already exists with ID: {existing.id}")
                return existing.id
            
            # Create new test announcement
            test_announcement = Announcement(
                title="🎉 Test Newsletter - Δοκιμή Συστήματος",
                content="""
                <h2>🎯 Καλώς ήρθατε στο Newsletter Test!</h2>
                
                <p>Αυτή είναι μια <strong>δοκιμαστική ανακοίνωση</strong> για να ελέγξουμε ότι το newsletter σύστημα λειτουργεί σωστά.</p>
                
                <h3>📋 Τι Ελέγχουμε:</h3>
                <ul>
                    <li>✅ API endpoints λειτουργούν</li>
                    <li>✅ SMTP σύνδεση με Gmail</li>
                    <li>✅ Email αποστολή</li>
                    <li>✅ Tracking στη βάση δεδομένων</li>
                </ul>
                
                <p><em>Αυτή η ανακοίνωση θα σταλεί σε όλους τους εγγεγραμμένους στο newsletter.</em></p>
                
                <hr>
                <p><small>Δημιουργήθηκε στις: {}</small></p>
                """.format(datetime.now().strftime('%d/%m/%Y %H:%M')),
                category="test",
                priority="high",
                is_published=True,
                sent_to_newsletter=False
            )
            
            db.session.add(test_announcement)
            db.session.commit()
            
            print(f"✅ Test announcement created successfully with ID: {test_announcement.id}")
            print(f"   Title: {test_announcement.title}")
            print(f"   Category: {test_announcement.category}")
            print(f"   Priority: {test_announcement.priority}")
            print(f"   Published: {test_announcement.is_published}")
            print(f"   Sent to newsletter: {test_announcement.sent_to_newsletter}")
            
            return test_announcement.id
            
        except Exception as e:
            print(f"❌ Error creating test announcement: {e}")
            db.session.rollback()
            return None

if __name__ == "__main__":
    print("🎯 Creating test announcement for newsletter testing...")
    announcement_id = create_test_announcement()
    
    if announcement_id:
        print(f"\n🎉 Test announcement ready! ID: {announcement_id}")
        print("Now you can test the newsletter system!")
    else:
        print("\n❌ Failed to create test announcement")
