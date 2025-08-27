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
os.environ['MAILGUN_API_KEY'] = 'key-8d988cf1f54cfb296e0f9d49ff06cef4-5a4acb93-f5a74e62'
os.environ['MAILGUN_DOMAIN'] = 'sandboxbf21727432ee40a3b393924982f76229.mailgun.org'
os.environ['MAILGUN_SENDER_EMAIL'] = 'postmaster@sandboxbf21727432ee40a3b393924982f76229.mailgun.org'

# SendGrid Configuration (Alternative email service)
os.environ['SENDGRID_API_KEY'] = 'your_sendgrid_api_key_here'
os.environ['SENDGRID_FROM_EMAIL'] = 'vlasia.blog@gmail.com'
os.environ['SENDGRID_FROM_NAME'] = 'Vlasia Blog'

# Resend Configuration (RECOMMENDED - 3,000 emails/month free)
os.environ['RESEND_API_KEY'] = 'your_resend_api_key_here'
os.environ['RESEND_FROM_EMAIL'] = 'vlasia.blog@gmail.com'
os.environ['RESEND_FROM_NAME'] = 'Vlasia Blog'

# Flask Configuration
os.environ['SECRET_KEY'] = 'vlasia-super-secret-key-2025-development'
os.environ['FLASK_ENV'] = 'development'

print("Environment variables set successfully!")
