# Environment Configuration for Email
import os

# Email Configuration
os.environ['MAIL_SERVER'] = 'smtp.gmail.com'
os.environ['MAIL_PORT'] = '587'
os.environ['MAIL_USE_TLS'] = 'True'
os.environ['MAIL_USERNAME'] = 'vlasia.blog@gmail.com'
os.environ['MAIL_PASSWORD'] = 'nxwh upvi kges tfqd'
os.environ['MAIL_DEFAULT_SENDER'] = 'vlasia.blog@gmail.com'

# Mailgun Configuration (Alternative email service)
os.environ['MAILGUN_API_KEY'] = 'your_mailgun_api_key_here'
os.environ['MAILGUN_DOMAIN'] = 'your_mailgun_domain_here'
os.environ['MAILGUN_SENDER_EMAIL'] = 'vlasia.blog@gmail.com'

# Flask Configuration
os.environ['SECRET_KEY'] = 'your-secret-key-change-this-in-production'
os.environ['FLASK_ENV'] = 'development'

print("Environment variables set successfully!")
