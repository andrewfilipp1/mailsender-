#!/usr/bin/env python3
"""
Check database structure and create missing tables
"""

from app import app, db
from app import Announcement, NewsletterSubscriber, ContactMessage

def check_database():
    with app.app_context():
        print("🔍 Checking database structure...")
        
        # Check if tables exist
        try:
            # Try to create all tables
            db.create_all()
            print("✅ All tables created/updated successfully!")
            
            # Check Announcement table
            try:
                result = db.session.execute(db.text("SELECT name FROM sqlite_master WHERE type='table' AND name='announcement'")).fetchone()
                print(f"📋 Announcement table exists: {result is not None}")
                
                if result:
                    # Check columns
                    columns = db.session.execute(db.text("PRAGMA table_info(announcement)")).fetchall()
                    print("📊 Announcement table columns:")
                    for col in columns:
                        print(f"  - {col[1]} ({col[2]})")
                        
                    # Check if table has data
                    count = db.session.execute(db.text("SELECT COUNT(*) FROM announcement")).fetchone()[0]
                    print(f"📈 Announcement records: {count}")
                    
            except Exception as e:
                print(f"❌ Error checking Announcement table: {e}")
                
        except Exception as e:
            print(f"❌ Error creating tables: {e}")
            
        print("\n🎯 Database check completed!")

if __name__ == "__main__":
    check_database()
