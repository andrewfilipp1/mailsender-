#!/usr/bin/env python3
"""
Email Sender Script for Vlasia Blog
This script runs locally and sends emails using Gmail SMTP
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
import json
from datetime import datetime
import time

# Configuration
GMAIL_USER = "vlasia.blog@gmail.com"
GMAIL_PASSWORD = "nxwh upvi kges tfqd"  # App password
SERVER_URL = "http://138.68.21.230"  # Your Digital Ocean server

def send_email(to_email, subject, body, is_html=False):
    """Send email using Gmail SMTP"""
    try:
        msg = MIMEMultipart()
        msg['From'] = GMAIL_USER
        msg['To'] = to_email
        msg['Subject'] = subject
        
        if is_html:
            msg.attach(MIMEText(body, 'html'))
        else:
            msg.attach(MIMEText(body, 'plain'))
        
        # Connect to Gmail SMTP
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(GMAIL_USER, GMAIL_PASSWORD)
        
        # Send email
        text = msg.as_string()
        server.sendmail(GMAIL_USER, to_email, text)
        server.quit()
        
        print(f"✅ Email sent successfully to {to_email}")
        return True
        
    except Exception as e:
        print(f"❌ Error sending email to {to_email}: {e}")
        return False

def get_pending_contact_messages():
    """Get pending contact messages from server"""
    try:
        response = requests.get(f"{SERVER_URL}/api/pending_contacts")
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                return data.get('contacts', [])
            else:
                print(f"API error: {data.get('error')}")
                return []
        else:
            print(f"HTTP error: {response.status_code}")
            return []
    except Exception as e:
        print(f"Error getting contact messages: {e}")
        return []

def get_pending_newsletter_subscribers():
    """Get pending newsletter subscribers from server"""
    try:
        response = requests.get(f"{SERVER_URL}/api/pending_newsletters")
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                return data.get('subscribers', [])
            else:
                print(f"API error: {data.get('error')}")
                return []
        else:
            print(f"HTTP error: {response.status_code}")
            return []
    except Exception as e:
        print(f"Error getting newsletter subscribers: {e}")
        return []

def send_contact_notification(contact_data):
    """Send contact form notification to admin"""
    subject = f"Νέο μήνυμα επικοινωνίας: {contact_data['subject']}"
    
    body = f"""
Νέα επικοινωνία από το site:

Όνομα: {contact_data['first_name']} {contact_data['last_name']}
Email: {contact_data['email']}
Θέμα: {contact_data['subject']}

Μήνυμα:
{contact_data['message']}

---
Αποστάλθηκε: {contact_data['created_at']}
"""
    
    return send_email(GMAIL_USER, subject, body)

def send_welcome_newsletter(subscriber_email):
    """Send welcome email to newsletter subscriber"""
    subject = "Καλώς ήρθατε στο Newsletter της Βλασίας! 🎉"
    
    body = f"""
🌟 Καλώς ήρθατε στο Newsletter της Βλασίας! 🌟

Ευχαριστούμε που εγγραφήκατε στο newsletter μας! 
Θα είστε από τους πρώτους που θα ενημερώνονται για:

📰 Τα τελευταία νέα του χωριού
📝 Νέες δημοσιεύσεις και άρθρα
🎭 Εκδηλώσεις και δραστηριότητες
🏞️ Τοπία και στιγμές από τη Βλασία
👥 Ενημερώσεις για την κοινότητα

Θα λαμβάνετε τα newsletters μας κάθε φορά που έχουμε κάτι σημαντικό να μοιραστούμε μαζί σας.

Με εκτίμηση και φιλία,
Η ομάδα της Βλασίας
🌿 vlasia.gr 🌿
"""
    
    return send_email(subscriber_email, subject, body)

def mark_contact_sent(contact_id):
    """Mark contact message as sent (update server)"""
    try:
        response = requests.post(f"{SERVER_URL}/api/mark_contact_sent/{contact_id}")
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print(f"✅ Contact message {contact_id} marked as sent on server")
                return True
            else:
                print(f"❌ Server error: {data.get('error')}")
                return False
        else:
            print(f"❌ HTTP error: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error marking contact as sent: {e}")
        return False

def mark_newsletter_sent(subscriber_id):
    """Mark newsletter welcome as sent (update server)"""
    try:
        response = requests.post(f"{SERVER_URL}/api/mark_newsletter_sent/{subscriber_id}")
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print(f"✅ Newsletter welcome {subscriber_id} marked as sent on server")
                return True
            else:
                print(f"❌ Server error: {data.get('error')}")
                return False
        else:
            print(f"❌ HTTP error: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error marking newsletter as sent: {e}")
        return False

def main():
    """Main function to process pending emails"""
    print("🚀 Starting Email Sender for Vlasia Blog...")
    print(f"📧 Using Gmail: {GMAIL_USER}")
    print(f"🌐 Server: {SERVER_URL}")
    print("-" * 50)
    
    # Process contact messages
    print("\n📝 Processing contact messages...")
    contacts = get_pending_contact_messages()
    
    for contact in contacts:
        if not contact.get('email_sent', False):
            print(f"📨 Sending contact notification for: {contact['email']}")
            if send_contact_notification(contact):
                mark_contact_sent(contact['id'])
                contact['email_sent'] = True
            time.sleep(1)  # Small delay between emails
    
    # Process newsletter subscribers
    print("\n📬 Processing newsletter subscribers...")
    subscribers = get_pending_newsletter_subscribers()
    
    for subscriber in subscribers:
        if not subscriber.get('welcome_sent', False):
            print(f"📨 Sending welcome email to: {subscriber['email']}")
            if send_welcome_newsletter(subscriber['email']):
                mark_newsletter_sent(subscriber['id'])
                subscriber['welcome_sent'] = True
            time.sleep(1)  # Small delay between emails
    
    print("\n✅ Email processing completed!")
    print(f"📊 Processed {len(contacts)} contact messages")
    print(f"📊 Processed {len(subscribers)} newsletter subscribers")

if __name__ == "__main__":
    main()
