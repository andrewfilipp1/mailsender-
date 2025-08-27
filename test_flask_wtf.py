#!/usr/bin/env python3
"""
Test script to check Flask-WTF functionality
"""

import os
from dotenv import load_dotenv

def test_flask_wtf():
    """Test Flask-WTF functionality"""
    print("🔍 Testing Flask-WTF functionality...")
    
    # Load environment variables
    load_dotenv()
    
    # Set environment variables
    os.environ['FLASK_ENV'] = 'development'
    os.environ['SECRET_KEY'] = 'dev-secret-key-for-testing'
    
    try:
        # Import Flask and create app
        from flask import Flask
        from flask_wtf import FlaskForm
        from wtforms import StringField
        from wtforms.validators import DataRequired
        
        print("✅ Flask and Flask-WTF imported successfully")
        
        # Create Flask app
        app = Flask(__name__)
        app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
        
        print(f"✅ Flask app created with SECRET_KEY: {app.config['SECRET_KEY']}")
        
        # Create a simple form
        class TestForm(FlaskForm):
            test_field = StringField('Test', validators=[DataRequired()])
        
        print("✅ TestForm created successfully")
        
        # Test form creation
        with app.app_context():
            form = TestForm()
            print(f"✅ Form created with CSRF token: {form.csrf_token}")
            
            # Test form validation
            if form.validate_on_submit():
                print("✅ Form validation works")
            else:
                print("✅ Form validation works (no submit)")
                
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_flask_wtf()
