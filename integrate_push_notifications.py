#!/usr/bin/env python3
"""
Integration Script for Push Notifications System
This script shows how to integrate the push notification system into your existing Flask app
"""

import os
import shutil

def create_directories():
    """Create necessary directories for the push notification system"""
    directories = [
        'static/js',
        'templates'
    ]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"✅ Created directory: {directory}")
        else:
            print(f"📁 Directory exists: {directory}")

def copy_files():
    """Copy push notification files to their proper locations"""
    files_to_copy = [
        ('push_notification_system.py', 'push_notification_system.py'),
        ('static/js/push-sw.js', 'static/js/push-sw.js'),
        ('static/js/push-notifications.js', 'static/js/push-notifications.js'),
        ('templates/push_notifications.html', 'templates/push_notifications.html'),
        ('templates/admin_push_notifications.html', 'templates/admin_push_notifications.html')
    ]
    
    for src, dst in files_to_copy:
        if os.path.exists(src):
            shutil.copy2(src, dst)
            print(f"✅ Copied: {src} -> {dst}")
        else:
            print(f"❌ Source file not found: {src}")

def create_integration_guide():
    """Create integration guide for the developer"""
    guide = """# 🔔 Push Notifications Integration Guide

## 📋 Files Created/Modified

### New Files:
- `push_notification_system.py` - Main push notification system class
- `static/js/push-sw.js` - Service Worker for push notifications
- `static/js/push-notifications.js` - Frontend JavaScript
- `templates/push_notifications.html` - User subscription page
- `templates/admin_push_notifications.html` - Admin management page
- `requirements_push_notifications.txt` - Dependencies

## 🚀 Integration Steps

### 1. Install Dependencies
```bash
pip install -r requirements_push_notifications.txt
```

### 2. Add to Flask App (app.py)
Add these lines to your Flask app:

```python
# Import the push notification system
from push_notification_system import push_notifications

# Initialize with your app
push_notifications.init_app(app)

# Add routes for push notifications
@app.route('/push-notifications')
def push_notifications_page():
    return render_template('push_notifications.html')

# API routes for push notifications
@app.route('/api/push/vapid-key')
def get_vapid_key():
    stats = push_notifications.get_statistics()
    return jsonify({'public_key': stats.get('vapid_public_key')})

@app.route('/api/push/subscribe', methods=['POST'])
def subscribe_push():
    data = request.get_json()
    success = push_notifications.subscribe(data)
    return jsonify({'success': success})

@app.route('/api/push/unsubscribe', methods=['POST'])
def unsubscribe_push():
    data = request.get_json()
    success = push_notifications.unsubscribe(data.get('endpoint'))
    return jsonify({'success': success})

# Admin routes
@app.route('/admin/push-notifications')
@admin_required  # Your admin authentication
def admin_push_notifications():
    stats = push_notifications.get_statistics()
    subscribers = push_notifications.subscriptions
    return render_template('admin_push_notifications.html', 
                         stats=stats, subscribers=subscribers)

@app.route('/admin/push/send-test', methods=['POST'])
@admin_required
def send_test_notification():
    title = request.form.get('title')
    body = request.form.get('body')
    count = push_notifications.send_notification(title, body)
    flash(f'Test notification sent to {count} subscribers', 'success')
    return redirect(url_for('admin_push_notifications'))

# Auto-send notifications when announcements are created
@app.route('/create_announcement', methods=['POST'])
@admin_required
def create_announcement():
    # Your existing announcement creation code...
    
    # After saving the announcement, send push notification
    if announcement:
        push_notifications.send_announcement_notification({
            'id': announcement.id,
            'title': announcement.title,
            'content': announcement.content
        })
    
    return redirect(url_for('admin_dashboard'))
```

### 3. Add Navigation Links
Add to your base template:

```html
<!-- User navigation -->
<li class="nav-item">
    <a class="nav-link" href="{{ url_for('push_notifications_page') }}">
        <i class="fas fa-bell"></i> Ειδοποιήσεις
    </a>
</li>

<!-- Admin navigation -->
<li class="nav-item">
    <a class="nav-link" href="{{ url_for('admin_push_notifications') }}">
        <i class="fas fa-bell"></i> Push Notifications
    </a>
</li>
```

### 4. Test the System
1. Visit `/push-notifications` to test user subscription
2. Visit `/admin/push-notifications` to test admin panel
3. Create a test announcement to test auto-notifications

## 🔧 Configuration

### VAPID Keys
The system automatically generates VAPID keys on first run:
- `vapid_keys.json` - Contains your VAPID keys
- Keep these keys secure and don't share them

### Subscriptions Storage
- `push_subscriptions.json` - Stores user subscriptions
- Back up this file regularly

## 📱 How It Works

1. **User subscribes** to push notifications
2. **Service Worker** is registered in their browser
3. **When you create announcement**, system automatically sends notifications
4. **Users receive notifications** even when not on your site
5. **Admin panel** shows statistics and management tools

## 🚨 Important Notes

- **HTTPS Required**: Push notifications only work over HTTPS
- **Browser Support**: Works in all modern browsers
- **No SMTP Needed**: Uses Web Push API instead of email
- **Automatic**: Sends notifications automatically when announcements are created

## 🆘 Troubleshooting

### Common Issues:
1. **Notifications not working**: Check browser permissions
2. **Service Worker errors**: Check browser console
3. **VAPID key errors**: Regenerate keys by deleting `vapid_keys.json`

### Debug Mode:
Check browser console and server logs for detailed error messages.

## 🎯 Next Steps

1. Test the system thoroughly
2. Customize notification content and styling
3. Add analytics tracking
4. Consider adding notification categories

---
🎉 Your push notification system is ready! Users will now receive instant notifications for new announcements!
"""
    
    with open('PUSH_NOTIFICATIONS_INTEGRATION.md', 'w', encoding='utf-8') as f:
        f.write(guide)
    
    print("✅ Created integration guide: PUSH_NOTIFICATIONS_INTEGRATION.md")

def main():
    """Main integration function"""
    print("🚀 Starting Push Notifications Integration...")
    print("=" * 50)
    
    # Create directories
    create_directories()
    print()
    
    # Copy files
    copy_files()
    print()
    
    # Create integration guide
    create_integration_guide()
    print()
    
    print("🎉 Integration completed successfully!")
    print()
    print("📋 Next steps:")
    print("1. Install dependencies: pip install -r requirements_push_notifications.txt")
    print("2. Follow the integration guide in PUSH_NOTIFICATIONS_INTEGRATION.md")
    print("3. Test the system")
    print()
    print("🔔 Your users will now receive push notifications for new announcements!")

if __name__ == "__main__":
    main()
