#!/usr/bin/env python3
"""
Automated Email Sender for Vlasia Blog
This script runs automatically and sends emails for new contact messages and newsletter subscriptions
"""

import os
import sys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
import json
from datetime import datetime
import time
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('email_sender.log'),
        logging.StreamHandler()
    ]
)

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
        
        logging.info(f"✅ Email sent successfully to {to_email}")
        return True
        
    except Exception as e:
        logging.error(f"❌ Error sending email to {to_email}: {e}")
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
                logging.error(f"API error: {data.get('error')}")
                return []
        else:
            logging.error(f"HTTP error: {response.status_code}")
            return []
    except Exception as e:
        logging.error(f"Error getting contact messages: {e}")
        return []

def get_pending_newsletter_subscribers():
    """Get pending newsletter subscribers for welcome emails (only those who haven't received welcome email)"""
    try:
        response = requests.get(f"{SERVER_URL}/api/pending_newsletters")
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                # Filter only subscribers who haven't received welcome email
                pending_subscribers = []
                for subscriber in data.get('subscribers', []):
                    if not subscriber.get('welcome_email_sent', False):
                        pending_subscribers.append(subscriber)
                return pending_subscribers
            else:
                logging.error(f"API error: {data.get('error')}")
                return []
        else:
            logging.error(f"HTTP error: {response.status_code}")
            return []
    except Exception as e:
        logging.error(f"Error getting newsletter subscribers: {e}")
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
                logging.info(f"✅ Contact message {contact_id} marked as sent on server")
                return True
            else:
                logging.error(f"❌ Server error: {data.get('error')}")
                return False
        else:
            logging.error(f"❌ HTTP error: {response.status_code}")
            return False
    except Exception as e:
        logging.error(f"❌ Error marking contact as sent: {e}")
        return False

def mark_newsletter_sent(subscriber_id):
    """Mark newsletter welcome as sent (update server)"""
    try:
        response = requests.post(f"{SERVER_URL}/api/mark_newsletter_sent/{subscriber_id}")
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                logging.info(f"✅ Newsletter welcome {subscriber_id} marked as sent on server")
                return True
            else:
                logging.error(f"❌ Server error: {data.get('error')}")
                return False
        else:
            logging.error(f"❌ HTTP error: {response.status_code}")
            return False
    except Exception as e:
        logging.error(f"❌ Error marking newsletter as sent: {e}")
        return False

def process_contact_notifications():
    """Process contact notifications (only unsent ones)"""
    try:
        # Get contact messages that haven't sent notifications yet
        response = requests.get(f"{SERVER_URL}/api/pending_contacts")
        if response.status_code != 200:
            logging.error(f"HTTP error getting contacts: {response.status_code}")
            return 0
        
        data = response.json()
        if not data.get('success'):
            logging.error(f"API error getting contacts: {data.get('error')}")
            return 0
        
        contacts = data.get('contacts', [])
        contact_count = 0
        
        for contact in contacts:
            if not contact.get('notification_sent', False):
                logging.info(f"📨 Sending contact notification for: {contact['email']}")
                if send_contact_notification(contact):
                    # Mark as sent
                    mark_contact_notification_sent(contact['id'])
                    contact_count += 1
                time.sleep(1)  # Small delay between emails
        
        return contact_count
        
    except Exception as e:
        logging.error(f"Error processing contact notifications: {e}")
        return 0

def mark_contact_notification_sent(contact_id):
    """Mark contact notification as sent (update server)"""
    try:
        response = requests.post(f"{SERVER_URL}/api/mark_contact_notification_sent/{contact_id}")
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                logging.info(f"✅ Contact notification {contact_id} marked as sent on server")
                return True
            else:
                logging.error(f"❌ Server error: {data.get('error')}")
                return False
        else:
            logging.error(f"❌ HTTP error: {response.status_code}")
            return False
    except Exception as e:
        logging.error(f"❌ Error marking contact notification as sent: {e}")
        return False

def process_announcements():
    """Process announcements (only unsent ones)"""
    try:
        # Get announcements that haven't been sent to newsletter yet
        response = requests.get(f"{SERVER_URL}/api/pending_announcements")
        if response.status_code != 200:
            logging.error(f"HTTP error getting announcements: {response.status_code}")
            return 0
        
        data = response.json()
        if not data.get('success'):
            logging.error(f"API error getting announcements: {data.get('error')}")
            return 0
        
        announcements = data.get('announcements', [])
        announcement_count = 0
        
        for announcement in announcements:
            logging.info(f"📢 Sending announcement: {announcement['title']}")
            if send_announcement_to_newsletter(announcement):
                # Mark as sent
                mark_announcement_sent(announcement['id'])
                announcement_count += 1
            time.sleep(1)  # Small delay between emails
        
        return announcement_count
        
    except Exception as e:
        logging.error(f"Error processing announcements: {e}")
        return 0

def send_announcement_to_newsletter(announcement):
    """Send announcement to all newsletter subscribers"""
    try:
        # Get all active subscribers
        response = requests.get(f"{SERVER_URL}/api/pending_newsletters")
        if response.status_code != 200:
            logging.error(f"HTTP error getting subscribers: {response.status_code}")
            return False
        
        data = response.json()
        if not data.get('success'):
            logging.error(f"API error getting subscribers: {data.get('error')}")
            return False
        
        # Get all active subscribers (not just pending ones)
        response = requests.get(f"{SERVER_URL}/api/all_newsletters")
        if response.status_code != 200:
            logging.error(f"HTTP error getting all subscribers: {response.status_code}")
            return False
        
        data = response.json()
        if not data.get('success'):
            logging.error(f"API error getting all subscribers: {data.get('error')}")
            return False
        
        subscribers = data.get('subscribers', [])
        
        if not subscribers:
            logging.warning("No newsletter subscribers found")
            return True
        
        for subscriber in subscribers:
            # Send announcement email
            subject = f"Ανακοίνωση: {announcement['title']}"
            
            body = f"""
🌟 Νέα Ανακοίνωση από τη Βλασία! 🌟

{announcement['title']}

{announcement['content']}

---
Κατηγορία: {announcement['category']}
Προτεραιότητα: {announcement['priority']}
Ημερομηνία: {announcement['created_at'][:10]}

Με εκτίμηση και φιλία,
Η ομάδα της Βλασίας
🌿 vlasia.gr 🌿
"""
            
            # Send email using Gmail SMTP
            if send_email(subscriber['email'], subject, body):
                logging.info(f"✅ Announcement sent to {subscriber['email']}")
            else:
                logging.error(f"❌ Failed to send announcement to {subscriber['email']}")
            
            time.sleep(1)  # Small delay between emails
        
        logging.info(f"✅ Announcement '{announcement['title']}' sent to {len(subscribers)} subscribers")
        return True
        
    except Exception as e:
        logging.error(f"❌ Error sending announcement to newsletter: {e}")
        return False

def mark_announcement_sent(announcement_id):
    """Mark announcement as sent (update server)"""
    try:
        response = requests.post(f"{SERVER_URL}/api/mark_announcement_sent/{announcement_id}")
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                logging.info(f"✅ Announcement {announcement_id} marked as sent on server")
                return True
            else:
                logging.error(f"❌ Server error: {data.get('error')}")
                return False
        else:
            logging.error(f"❌ HTTP error: {response.status_code}")
            return False
    except Exception as e:
        logging.error(f"❌ Error marking announcement as sent: {e}")
        return False

def main():
    """Main function to process pending emails"""
    logging.info("🚀 Starting Automated Email Sender for Vlasia Blog...")
    logging.info(f"📧 Using Gmail: {GMAIL_USER}")
    logging.info(f"🌐 Server: {SERVER_URL}")
    logging.info("-" * 50)
    
    # Process newsletter subscribers (welcome emails - only once)
    logging.info("📬 Processing newsletter subscribers...")
    subscribers = get_pending_newsletter_subscribers()
    
    subscriber_count = 0
    for subscriber in subscribers:
        logging.info(f"📨 Sending welcome email to: {subscriber['email']}")
        if send_welcome_newsletter(subscriber['email']):
            mark_newsletter_sent(subscriber['id'])
            subscriber_count += 1
        time.sleep(1)  # Small delay between emails
    
    # Process contact notifications (only once)
    logging.info("📝 Processing contact notifications...")
    contact_count = process_contact_notifications()
    
    # Process announcements (only once)
    logging.info("📢 Processing announcements...")
    announcement_count = process_announcements()
    
    logging.info("✅ Email processing completed!")
    logging.info(f"📊 Processed {contact_count} contact notifications")
    logging.info(f"📊 Processed {subscriber_count} newsletter subscribers")
    logging.info(f"📊 Processed {announcement_count} announcements")
    
    # Return exit code for cron job
    if contact_count > 0 or subscriber_count > 0 or announcement_count > 0:
        return 0  # Success
    else:
        return 1  # No emails to process

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        logging.info("🛑 Script interrupted by user")
        sys.exit(1)
    except Exception as e:
        logging.error(f"💥 Unexpected error: {e}")
        sys.exit(1)
