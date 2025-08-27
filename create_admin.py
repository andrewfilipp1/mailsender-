#!/usr/bin/env python3
"""
Simple script to create admin user directly in database
"""

import sqlite3
from werkzeug.security import generate_password_hash

def create_admin_user():
    """Create admin user directly in database"""
    try:
        # Connect to database
        conn = sqlite3.connect('instance/vlasia.db')
        cursor = conn.cursor()
        
        # Create new admin user with different username and email
        username = 'admin'
        email = 'admin2@vlasia.gr'
        password_hash = generate_password_hash('password123')
        
        # Check if user exists
        cursor.execute("SELECT username FROM user WHERE username = ?", (username,))
        if cursor.fetchone():
            print(f"✅ User '{username}' already exists")
            return
        
        # Create admin user
        cursor.execute("""
            INSERT INTO user (username, email, password_hash, is_admin, created_at)
            VALUES (?, ?, ?, ?, datetime('now'))
        """, (username, email, password_hash, True))
        
        conn.commit()
        print("✅ New admin user created successfully!")
        print(f"   Username: {username}")
        print(f"   Email: {email}")
        print("   Password: password123")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        conn.close()

if __name__ == '__main__':
    create_admin_user()
