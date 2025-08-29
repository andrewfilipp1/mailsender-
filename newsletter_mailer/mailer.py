#!/usr/bin/env python3
"""
Newsletter Mailer Script for Vlasia Site
This script runs independently to send newsletter emails via external SMTP
"""

import os
import requests
import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('newsletter_mailer.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class NewsletterMailer:
    def __init__(self):
        """Initialize the mailer with configuration from environment variables"""
        # API Configuration
        self.api_url_get_emails = os.getenv('API_URL_GET_EMAILS')
        self.api_url_mark_sent = os.getenv('API_URL_MARK_SENT')
        self.api_secret_key = os.getenv('API_SECRET_KEY')
        
        # SMTP Configuration
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', '587'))
        self.smtp_username = os.getenv('SMTP_USERNAME')
        self.smtp_password = os.getenv('SMTP_PASSWORD')
        self.sender_email = os.getenv('SENDER_EMAIL')
        
        # Validate configuration
        self._validate_config()
    
    def _validate_config(self):
        """Validate that all required configuration is present"""
        required_vars = [
            'API_URL_GET_EMails',
            'API_URL_MARK_SENT', 
            'API_SECRET_KEY',
            'SMTP_USERNAME',
            'SMTP_PASSWORD',
            'SENDER_EMAIL'
        ]
        
        missing_vars = []
        for var in required_vars:
            if not getattr(self, var.lower()):
                missing_vars.append(var)
        
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
    
    def get_newsletter_data(self):
        """Fetch newsletter data from the site API"""
        try:
            headers = {
                'Authorization': f'Bearer {self.api_secret_key}',
                'Content-Type': 'application/json'
            }
            
            logger.info(f"Fetching newsletter data from: {self.api_url_get_emails}")
            response = requests.get(self.api_url_get_emails, headers=headers, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            logger.info(f"Retrieved data for {len(data.get('recipients', []))} recipients")
            return data
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching newsletter data: {e}")
            return None
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing JSON response: {e}")
            return None
    
    def send_email(self, recipient_email, subject, body_html):
        """Send a single email via SMTP"""
        try:
            msg = MIMEMultipart('alternative')
            msg['From'] = self.sender_email
            msg['To'] = recipient_email
            msg['Subject'] = subject
            
            # Add HTML content
            html_part = MIMEText(body_html, 'html', 'utf-8')
            msg.attach(html_part)
            
            # Connect to SMTP server
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                
                # Send email
                server.send_message(msg)
                logger.info(f"Email sent successfully to: {recipient_email}")
                return True
                
        except Exception as e:
            logger.error(f"Failed to send email to {recipient_email}: {e}")
            return False
    
    def mark_email_sent(self, user_id, announcement_id):
        """Mark an email as sent in the site database"""
        try:
            headers = {
                'Authorization': f'Bearer {self.api_secret_key}',
                'Content-Type': 'application/json'
            }
            
            payload = {
                'user_id': user_id,
                'announcement_id': announcement_id,
                'sent_at': datetime.utcnow().isoformat()
            }
            
            response = requests.post(
                self.api_url_mark_sent, 
                headers=headers, 
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            
            logger.info(f"Marked email as sent for user {user_id}, announcement {announcement_id}")
            return True
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error marking email as sent: {e}")
            return False
    
    def run(self):
        """Main execution method"""
        logger.info("🚀 Starting Newsletter Mailer...")
        
        # Get newsletter data
        data = self.get_newsletter_data()
        if not data:
            logger.warning("No newsletter data available. Exiting.")
            return
        
        if not data.get('recipients'):
            logger.info("No recipients found. Exiting.")
            return
        
        # Send emails to each recipient
        success_count = 0
        total_count = len(data['recipients'])
        
        for recipient in data['recipients']:
            user_id = recipient['user_id']
            email = recipient['email']
            
            logger.info(f"Processing recipient {user_id}: {email}")
            
            # Send email
            if self.send_email(email, data['subject'], data['body_html']):
                # Mark as sent
                if self.mark_email_sent(user_id, data['announcement_id']):
                    success_count += 1
                    logger.info(f"✅ Successfully processed: {email}")
                else:
                    logger.warning(f"⚠️ Email sent but failed to mark as sent: {email}")
            else:
                logger.error(f"❌ Failed to send email: {email}")
        
        # Summary
        logger.info(f"🎯 Newsletter processing complete!")
        logger.info(f"📊 Total recipients: {total_count}")
        logger.info(f"✅ Successful: {success_count}")
        logger.info(f"❌ Failed: {total_count - success_count}")

def main():
    """Main entry point"""
    try:
        mailer = NewsletterMailer()
        mailer.run()
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        exit(1)

if __name__ == "__main__":
    main()

