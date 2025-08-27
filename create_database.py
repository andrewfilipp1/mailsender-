#!/usr/bin/env python3
"""
Script to manually create the database and admin user for Vlasia Blog
"""

import os
import sys
from datetime import datetime

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db, User, NewsItem, Media, NewsletterSubscriber, Moment
from werkzeug.security import generate_password_hash

def create_database():
    """Create database tables and admin user"""
    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        print("✅ Database tables created successfully!")
        
        # Check if admin user already exists
        admin_user = User.query.filter_by(username='vlasia_admin').first()
        if admin_user:
            print("✅ Admin user already exists")
            return
        
        # Create admin user
        print("Creating admin user...")
        admin_user = User(
            username='vlasia_admin',
            email='admin@vlasia.gr',
            password_hash=generate_password_hash('admin123'),
            is_admin=True,
            created_at=datetime.utcnow()
        )
        
        db.session.add(admin_user)
        db.session.commit()
        print("✅ Admin user created successfully!")
        print("   Username: vlasia_admin")
        print("   Password: admin123")
        print("   Email: admin@vlasia.gr")

if __name__ == '__main__':
    try:
        create_database()
        print("\n🎉 Database setup completed successfully!")
        print("You can now login with:")
        print("   Username: vlasia_admin")
        print("   Password: admin123")
    except Exception as e:
        print(f"❌ Error creating database: {e}")
        sys.exit(1)
