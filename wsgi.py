#!/usr/bin/env python3
"""
WSGI entry point for production deployment on Digital Ocean
"""
import os
from app import app

if __name__ == "__main__":
    # Set production environment
    os.environ['FLASK_ENV'] = 'production'
    
    # Run the application
    app.run()
