#!/usr/bin/env python3
"""
Test script για τις φόρμες newsletter και επικοινωνίας
"""

import requests
import json

# Test URLs
BASE_URL = "http://vlasia.gr"  # ή http://138.68.21.230 αν δεν έχει domain

def test_newsletter_form():
    """Test τη φόρμα newsletter"""
    print("🧪 Testing Newsletter Form...")
    
    url = f"{BASE_URL}/subscribe-newsletter"
    data = {
        'email': 'test@example.com'
    }
    
    try:
        response = requests.post(url, data=data, allow_redirects=False)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text[:200]}...")
        
        if response.status_code in [200, 302]:
            print("✅ Newsletter form works!")
        else:
            print("❌ Newsletter form failed!")
            
    except Exception as e:
        print(f"❌ Error testing newsletter: {e}")

def test_contact_form():
    """Test τη φόρμα επικοινωνίας"""
    print("\n🧪 Testing Contact Form...")
    
    url = f"{BASE_URL}/contact"
    data = {
        'firstName': 'Test',
        'lastName': 'User',
        'email': 'test@example.com',
        'subject': 'Test Message',
        'message': 'This is a test message from the test script.'
    }
    
    try:
        response = requests.post(url, data=data, allow_redirects=False)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text[:200]}...")
        
        if response.status_code in [200, 302]:
            print("✅ Contact form works!")
        else:
            print("❌ Contact form failed!")
            
    except Exception as e:
        print(f"❌ Error testing contact form: {e}")

def test_homepage():
    """Test την αρχική σελίδα"""
    print("\n🧪 Testing Homepage...")
    
    url = f"{BASE_URL}/"
    
    try:
        response = requests.get(url)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Homepage works!")
        else:
            print("❌ Homepage failed!")
            
    except Exception as e:
        print(f"❌ Error testing homepage: {e}")

if __name__ == "__main__":
    print("🚀 Starting Form Tests...")
    print(f"Testing against: {BASE_URL}")
    
    test_homepage()
    test_newsletter_form()
    test_contact_form()
    
    print("\n✨ Tests completed!")
