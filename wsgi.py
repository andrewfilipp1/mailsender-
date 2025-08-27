#!/usr/bin/env python3
"""
WSGI entry point for Vlasia Blog
"""

from app import app, db

# Create all tables when the app starts
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run()
