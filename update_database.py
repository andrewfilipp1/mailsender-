#!/usr/bin/env python3
"""
Update database schema with new columns
"""

from app import app, db

def update_database():
    with app.app_context():
        print("🔧 Updating database schema...")
        
        try:
            # Add new columns to existing tables
            print("📊 Adding welcome_email_sent to newsletter_subscriber...")
            db.session.execute(db.text("ALTER TABLE newsletter_subscriber ADD COLUMN welcome_email_sent BOOLEAN DEFAULT FALSE"))
            
            print("📊 Adding notification_sent to contact_message...")
            db.session.execute(db.text("ALTER TABLE contact_message ADD COLUMN notification_sent BOOLEAN DEFAULT FALSE"))
            
            # Commit changes
            db.session.commit()
            print("✅ Database schema updated successfully!")
            
            # Verify the changes
            print("\n🔍 Verifying changes...")
            
            # Check newsletter_subscriber columns
            columns = db.session.execute(db.text("PRAGMA table_info(newsletter_subscriber)")).fetchall()
            print("📋 Newsletter subscriber columns:")
            for col in columns:
                print(f"  - {col[1]} ({col[2]})")
            
            # Check contact_message columns
            columns = db.session.execute(db.text("PRAGMA table_info(contact_message)")).fetchall()
            print("\n📋 Contact message columns:")
            for col in columns:
                print(f"  - {col[1]} ({col[2]})")
                
        except Exception as e:
            print(f"❌ Error updating database: {e}")
            db.session.rollback()

if __name__ == "__main__":
    update_database()
