#!/usr/bin/env python3
"""
Simple test script for Flask app
"""

from app import app

def test_app():
    print("🚀 Testing Flask App...")
    
    # Check routes
    print("\n📋 Push Notification Routes:")
    for rule in app.url_map.iter_rules():
        if 'push' in rule.rule:
            print(f"  ✅ {rule.rule}")
    
    # Test VAPID endpoint
    print("\n🔑 Testing VAPID endpoint...")
    with app.test_client() as client:
        response = client.get('/api/push/vapid-key')
        print(f"  Status: {response.status_code}")
        if response.status_code == 200:
            data = response.get_json()
            print(f"  Data: {data}")
        else:
            print(f"  Error: {response.data}")
    
    # Test push notifications page
    print("\n📱 Testing push notifications page...")
    with app.test_client() as client:
        response = client.get('/push-notifications')
        print(f"  Status: {response.status_code}")
        if response.status_code == 200:
            print("  ✅ Page loads successfully")
        else:
            print(f"  ❌ Error: {response.data}")
    
    print("\n🎉 Test completed!")

if __name__ == "__main__":
    test_app()

