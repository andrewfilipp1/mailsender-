#!/usr/bin/env python3
"""
Simple test script to test login functionality
"""

import requests
from bs4 import BeautifulSoup

def test_login():
    """Test login functionality"""
    base_url = "http://localhost:5001"
    
    # First, get the login page to get CSRF token
    print("🔍 Getting login page...")
    response = requests.get(f"{base_url}/login")
    
    if response.status_code != 200:
        print(f"❌ Failed to get login page: {response.status_code}")
        return
    
    # Parse the HTML to find CSRF token
    soup = BeautifulSoup(response.text, 'html.parser')
    csrf_token = soup.find('input', {'name': 'csrf_token'})
    
    if csrf_token:
        csrf_value = csrf_token.get('value')
        print(f"✅ Found CSRF token: {csrf_value[:20]}...")
    else:
        print("⚠️  No CSRF token found")
        csrf_value = ""
    
    # Try to login
    print("\n🔐 Attempting login...")
    login_data = {
        'username': 'vlasia_admin',
        'password': 'admin123'
    }
    
    if csrf_value:
        login_data['csrf_token'] = csrf_value
    
    # Send login request
    login_response = requests.post(
        f"{base_url}/login",
        data=login_data,
        allow_redirects=False,
        headers={'Content-Type': 'application/x-www-form-urlencoded'}
    )
    
    print(f"📊 Login response status: {login_response.status_code}")
    print(f"📊 Response headers: {dict(login_response.headers)}")
    
    if login_response.status_code == 302:
        print("✅ Login successful! Redirecting...")
        redirect_url = login_response.headers.get('Location', '')
        print(f"🔄 Redirect URL: {redirect_url}")
    else:
        print("❌ Login failed")
        print(f"📄 Response content: {login_response.text[:500]}...")

if __name__ == '__main__':
    try:
        test_login()
    except Exception as e:
        print(f"❌ Error: {e}")
