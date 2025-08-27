#!/usr/bin/env python3
"""
Test script to test login with new admin user
"""

import urllib.request
import urllib.parse
import urllib.error
import re

def test_new_admin_login():
    """Test login with new admin user"""
    base_url = "http://localhost:5001"
    
    print("🔍 Step 1: Getting login page...")
    try:
        response = urllib.request.urlopen(f"{base_url}/login")
        print(f"✅ Login page status: {response.status}")
        
        # Read the content
        content = response.read().decode('utf-8')
        
        # Extract CSRF token manually
        csrf_match = re.search(r'name="csrf_token" value="([^"]+)"', content)
        if csrf_match:
            csrf_token = csrf_match.group(1)
            print(f"✅ Found CSRF token: {csrf_token[:20]}...")
        else:
            print("❌ No CSRF token found")
            return
            
    except Exception as e:
        print(f"❌ Failed to get login page: {e}")
        return
    
    print("\n🔐 Step 2: Attempting login with new admin user...")
    login_data = {
        'username': 'admin',
        'password': 'password123',
        'csrf_token': csrf_token
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
            # Try to read error response
            try:
                error_content = e.read().decode('utf-8')
                print(f"📄 Error content: {error_content[:500]}...")
            except:
                pass
    except Exception as e:
        print(f"❌ Error during login: {e}")

if __name__ == '__main__':
    test_new_admin_login()
