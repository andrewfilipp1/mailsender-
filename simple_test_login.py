#!/usr/bin/env python3
"""
Simple test script to test login functionality without external dependencies
"""

import urllib.request
import urllib.parse
import urllib.error

def test_login():
    """Test login functionality"""
    base_url = "http://localhost:5001"
    
    # First, get the login page
    print("🔍 Getting login page...")
    try:
        response = urllib.request.urlopen(f"{base_url}/login")
        print(f"✅ Login page status: {response.status}")
        
        # Read the content
        content = response.read().decode('utf-8')
        
        # Simple check for CSRF token
        if 'csrf_token' in content:
            print("✅ CSRF token found in page")
        else:
            print("⚠️  No CSRF token found in page")
            
    except Exception as e:
        print(f"❌ Failed to get login page: {e}")
        return
    
    # Try to login
    print("\n🔐 Attempting login...")
    login_data = {
        'username': 'vlasia_admin',
        'password': 'admin123'
    }
    
    # Encode data
    data = urllib.parse.urlencode(login_data).encode('utf-8')
    
    try:
        # Create request
        req = urllib.request.Request(
            f"{base_url}/login",
            data=data,
            headers={'Content-Type': 'application/x-www-form-urlencoded'}
        )
        
        # Send request
        login_response = urllib.request.urlopen(req)
        
        print(f"✅ Login response status: {login_response.status}")
        print(f"🔄 Response URL: {login_response.url}")
        
        # Check if we got redirected
        if login_response.url != f"{base_url}/login":
            print("🎉 Login successful! You were redirected!")
        else:
            print("⚠️  Login may have failed - still on login page")
            
    except urllib.error.HTTPError as e:
        print(f"❌ HTTP Error: {e.code} - {e.reason}")
        if e.code == 302:
            print("✅ Login successful! Got redirect response!")
        else:
            print("❌ Login failed")
    except Exception as e:
        print(f"❌ Error during login: {e}")

if __name__ == '__main__':
    test_login()
