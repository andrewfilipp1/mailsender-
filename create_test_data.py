#!/usr/bin/env python3
"""
Create Test Data - Δημιουργία test δεδομένων για το site
"""

from app import app, db, News, NewsletterSubscriber, ContactMessage
from datetime import datetime

def create_test_data():
    """Create test data for the site"""
    with app.app_context():
        print("🚀 Creating test data...")
        
        # Create test news
        test_news = [
            {
                'title': 'Καλώς ήρθατε στη Βλασία!',
                'content': 'Η Βλασία σας καλωσορίζει με τα πράσινα δάση και τα ψηλά βουνά της. Εδώ θα βρείτε όλα τα νέα και τις ανακοινώσεις που αφορούν τα χωριά μας.',
                'media_path': 'vlasia_waterfal.jpg',
                'media_type': 'image'
            },
            {
                'title': 'Εκδρομή στο βουνό Βλασίας',
                'content': 'Οργανώνουμε εκδρομή στο βουνό Βλασίας για την ερχόμενη Κυριακή. Θα δούμε τα πιο όμορφα σημεία και θα γευτούμε την τοπική κουζίνα.',
                'media_path': '',
                'media_type': ''
            },
            {
                'title': 'Γιορτή του χωριού',
                'content': 'Την ερχόμενη εβδομάδα θα γιορτάσουμε την επέτειο του χωριού μας. Θα υπάρχει μουσική, χορός και φαγητό για όλους!',
                'media_path': '',
                'media_type': ''
            }
        ]
        
        for news_data in test_news:
            news = News(
                title=news_data['title'],
                content=news_data['content'],
                media_path=news_data['media_path'],
                media_type=news_data['media_type'],
                created_at=datetime.utcnow()
            )
            db.session.add(news)
            print(f"✅ Added news: {news_data['title']}")
        
        # Create test newsletter subscribers
        test_subscribers = [
            'test1@example.com',
            'test2@example.com',
            'vlasia.blog@gmail.com'
        ]
        
        for email in test_subscribers:
            subscriber = NewsletterSubscriber(
                email=email,
                subscribed_at=datetime.utcnow(),
                is_active=True
            )
            db.session.add(subscriber)
            print(f"✅ Added subscriber: {email}")
        
        # Create test contact messages
        test_contacts = [
            {
                'first_name': 'Γιώργος',
                'last_name': 'Παπαδόπουλος',
                'email': 'giorgos@example.com',
                'subject': 'Ερώτηση για διαμονή',
                'message': 'Θα ήθελα να μάθω περισσότερα για τις επιλογές διαμονής στη Βλασία.'
            },
            {
                'first_name': 'Μαρία',
                'last_name': 'Κωνσταντίνου',
                'email': 'maria@example.com',
                'subject': 'Εκδρομές',
                'message': 'Ψάχνω πληροφορίες για οργανωμένες εκδρομές στη περιοχή.'
            }
        ]
        
        for contact_data in test_contacts:
            contact = ContactMessage(
                first_name=contact_data['first_name'],
                last_name=contact_data['last_name'],
                email=contact_data['email'],
                subject=contact_data['subject'],
                message=contact_data['message'],
                created_at=datetime.utcnow()
            )
            db.session.add(contact)
            print(f"✅ Added contact: {contact_data['email']}")
        
        # Commit all changes
        try:
            db.session.commit()
            print("✅ All test data created successfully!")
            
            # Show summary
            news_count = News.query.count()
            subscribers_count = NewsletterSubscriber.query.count()
            contacts_count = ContactMessage.query.count()
            
            print(f"\n📊 Database Summary:")
            print(f"📰 News: {news_count}")
            print(f"📧 Newsletter Subscribers: {subscribers_count}")
            print(f"📝 Contact Messages: {contacts_count}")
            
        except Exception as e:
            print(f"❌ Error creating test data: {e}")
            db.session.rollback()

if __name__ == "__main__":
    create_test_data()

