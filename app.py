from flask import Flask, render_template, request, redirect, url_for, flash, abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime
import os
import uuid
from PIL import Image
from config import config
from dotenv import load_dotenv
from flask_mail import Mail, Message

# Load environment variables first
load_dotenv()

# Flask app configuration
app = Flask(__name__)

# Load configuration based on environment
config_name = os.environ.get('FLASK_ENV', 'development')
app.config.from_object(config[config_name])

# Initialize extensions
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
admin = Admin(app, name='Vlasia Blog Admin', template_mode='bootstrap3')
mail = Mail(app)

# Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    image_path = db.Column(db.String(500))
    media_type = db.Column(db.String(10))  # 'image' or 'video'

class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    media_path = db.Column(db.String(500))
    media_type = db.Column(db.String(10))

class Moment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(100), nullable=False)
    media_path = db.Column(db.String(500), nullable=False)
    media_type = db.Column(db.String(10), nullable=False)  # 'image' or 'video'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class NewsletterSubscriber(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    subscribed_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

class ContactMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Forms
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')

class ArticleForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    category = StringField('Category', validators=[DataRequired()])
    image = FileField('Image', validators=[FileAllowed(['jpg', 'png', 'gif', 'jpeg'])])
    submit = SubmitField('Create Article')

class NewsForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    media = FileField('Media', validators=[FileAllowed(['jpg', 'png', 'gif', 'jpeg', 'mp4', 'avi', 'mov'])])
    submit = SubmitField('Create News')

class MomentForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description')
    category = StringField('Category', validators=[DataRequired()])
    media = FileField('Media', validators=[FileAllowed(['jpg', 'png', 'gif', 'jpeg', 'mp4', 'avi', 'mov'])])
    submit = SubmitField('Create Moment')

# Admin Views
class ArticleAdmin(ModelView):
    form_extra_fields = {
        'image': FileField('Image')
    }
    
    def on_model_change(self, form, model, is_created):
        if form.image.data:
            file = form.image.data
            filename = secure_filename(file.filename)
            unique_filename = f"{uuid.uuid4().hex}_{filename}"
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            file.save(file_path)
            model.image_path = unique_filename
            model.media_type = 'image'

class NewsAdmin(ModelView):
    form_extra_fields = {
        'media': FileField('Media')
    }
    
    def on_model_change(self, form, model, is_created):
        if form.media.data:
            file = form.media.data
            filename = secure_filename(file.filename)
            unique_filename = f"{uuid.uuid4().hex}_{filename}"
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            file.save(file_path)
            model.media_path = unique_filename
            
            # Determine media type
            if filename.lower().endswith(('.mp4', '.avi', '.mov')):
                model.media_type = 'video'
            else:
                model.media_type = 'image'

class MomentAdmin(ModelView):
    form_extra_fields = {
        'media': FileField('Media')
    }
    
    form_choices = {
        'category': [
            ('landscape', 'Τοπία'),
            ('village', 'Χωριό'),
            ('people', 'Ανθρώποι'),
            ('events', 'Εκδηλώσεις'),
            ('nature', 'Φύση')
        ]
    }
    
    def on_model_change(self, form, model, is_created):
        if form.media.data:
            file = form.media.data
            filename = secure_filename(file.filename)
            unique_filename = f"{uuid.uuid4().hex}_{filename}"
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            file.save(file_path)
            model.media_path = unique_filename
            
            # Determine media type
            if filename.lower().endswith(('.mp4', '.avi', '.mov')):
                model.media_type = 'video'
            else:
                model.media_type = 'image'

# Add admin views
admin.add_view(ArticleAdmin(Article, db.session))
admin.add_view(NewsAdmin(News, db.session))
admin.add_view(MomentAdmin(Moment, db.session))

# Newsletter Subscribers Admin
class NewsletterSubscriberAdmin(ModelView):
    column_list = ['id', 'email', 'subscribed_at', 'is_active']
    column_searchable_list = ['email']
    column_filters = ['is_active', 'subscribed_at']
    can_create = False  # Users can only subscribe through the form
    can_delete = True
    can_edit = True
    
admin.add_view(NewsletterSubscriberAdmin(NewsletterSubscriber, db.session, name='Newsletter Subscribers'))

# Contact Messages Admin
class ContactMessageAdmin(ModelView):
    column_list = ['id', 'first_name', 'last_name', 'email', 'subject', 'created_at']
    column_searchable_list = ['email', 'first_name', 'last_name', 'subject']
    column_filters = ['created_at']
    can_create = False  # Users can only send through the form
    can_delete = True
    can_edit = True
    
admin.add_view(ContactMessageAdmin(ContactMessage, db.session, name='Contact Messages'))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def index():
    articles = Article.query.order_by(Article.created_at.desc()).limit(3).all()
    news = News.query.order_by(News.created_at.desc()).limit(3).all()
    return render_template('index.html', articles=articles, news=news)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Get form data - ΔΙΟΡΘΩΜΕΝΑ ΟΝΟΜΑΤΑ
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')
        
        # Basic validation
        if not all([first_name, last_name, email, subject, message]):
            flash('Παρακαλώ συμπληρώστε όλα τα πεδία!', 'error')
            return redirect(url_for('contact'))
        
        # Save contact message
        contact_msg = ContactMessage(
            first_name=first_name,
            last_name=last_name,
            email=email,
            subject=subject,
            message=message
        )
        db.session.add(contact_msg)
        db.session.commit()
        
        # Try to send email notification
        try:
            if save_contact_message(first_name, last_name, email, subject, message):
                flash('Το μήνυμά σας στάλθηκε επιτυχώς! Θα σας απαντήσουμε σύντομα.', 'success')
            else:
                flash('Το μήνυμά σας αποθηκεύθηκε αλλά η αποστολή email απέτυχε. Θα σας απαντήσουμε σύντομα.', 'warning')
        except Exception as e:
            print(f"Error sending contact email: {e}")
            flash('Το μήνυμά σας αποθηκεύθηκε αλλά η αποστολή email απέτυχε. Θα σας απαντήσουμε σύντομα.', 'warning')
        
        return redirect(url_for('contact'))
    
    return render_template('contact.html')

@app.route('/news')
def news():
    page = request.args.get('page', 1, type=int)
    news_items = News.query.order_by(News.created_at.desc()).paginate(
        page=page, per_page=6, error_out=False)
    return render_template('news.html', news_items=news_items)

@app.route('/news/<int:news_id>')
def news_detail(news_id):
    news_item = News.query.get_or_404(news_id)
    return render_template('news_detail.html', news=news_item)

@app.route('/articles')
def articles():
    page = request.args.get('page', 1, type=int)
    articles_list = Article.query.order_by(Article.created_at.desc()).paginate(
        page=page, per_page=6, error_out=False)
    return render_template('articles.html', articles=articles_list)

@app.route('/articles/<int:article_id>')
def article_detail(article_id):
    article = Article.query.get_or_404(article_id)
    return render_template('article_detail.html', article=article)

@app.route('/category/<category>')
def category(category):
    page = request.args.get('page', 1, type=int)
    articles_list = Article.query.filter_by(category=category).order_by(
        Article.created_at.desc()).paginate(page=page, per_page=6, error_out=False)
    return render_template('category.html', articles=articles_list, category=category)

@app.route('/moments')
def moments():
    category_filter = request.args.get('category', '')
    sort_by = request.args.get('sort', 'newest')
    
    query = Moment.query
    
    if category_filter:
        query = query.filter_by(category=category_filter)
    
    if sort_by == 'oldest':
        query = query.order_by(Moment.created_at.asc())
    else:  # newest
        query = query.order_by(Moment.created_at.desc())
    
    moments_list = query.all()
    
    # Get unique categories for filter
    categories = db.session.query(Moment.category).distinct().all()
    categories = [cat[0] for cat in categories]
    
    return render_template('moments.html', moments=moments_list, categories=categories, 
                         current_category=category_filter, current_sort=sort_by)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('index')
            return redirect(next_page)
        else:
            flash('Invalid username or password')
    
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/subscribe_newsletter', methods=['POST'])
def subscribe_newsletter():
    email = request.form.get('email')
    
    if not email:
        flash('Παρακαλώ εισάγετε ένα έγκυρο email.', 'error')
        return redirect(url_for('index'))
    
    # Save subscriber using the new function
    success, message = save_newsletter_subscriber(email)
    
    if success:
        flash('Επιτυχής εγγραφή στο newsletter!', 'success')
    else:
        flash(message, 'info')
    
    return redirect(url_for('index'))

def save_contact_message(first_name, last_name, email, subject, message):
    """Save contact form message to database"""
    try:
        contact_msg = ContactMessage(
            first_name=first_name,
            last_name=last_name,
            email=email,
            subject=subject,
            message=message
        )
        db.session.add(contact_msg)
        db.session.commit()
        print(f"Contact message saved successfully from {email}")
        return True
    except Exception as e:
        print(f"Error saving contact message: {e}")
        db.session.rollback()
        return False

def save_newsletter_subscriber(email):
    """Save newsletter subscriber to database"""
    try:
        # Check if email already exists
        existing = NewsletterSubscriber.query.filter_by(email=email).first()
        if existing:
            if existing.is_active:
                print(f"Email {email} already subscribed")
                return False, "Email already subscribed"
            else:
                existing.is_active = True
                db.session.commit()
                print(f"Email {email} reactivated")
                return True, "Email reactivated"
        
        subscriber = NewsletterSubscriber(email=email)
        db.session.add(subscriber)
        db.session.commit()
        print(f"Newsletter subscriber saved successfully: {email}")
        return True, "Subscribed successfully"
    except Exception as e:
        print(f"Error saving newsletter subscriber: {e}")
        db.session.rollback()
        return False, f"Error: {e}"

# API Endpoints for Email Sender
@app.route('/api/pending_contacts')
def api_pending_contacts():
    """Get pending contact messages for email sending"""
    try:
        # Get contact messages that haven't been processed yet
        # For now, return all recent ones (you can add a 'processed' field later)
        contacts = ContactMessage.query.order_by(ContactMessage.created_at.desc()).limit(50).all()
        
        result = []
        for contact in contacts:
            result.append({
                'id': contact.id,
                'first_name': contact.first_name,
                'last_name': contact.last_name,
                'email': contact.email,
                'subject': contact.subject,
                'message': contact.message,
                'created_at': contact.created_at.isoformat() if contact.created_at else None
            })
        
        return {'success': True, 'contacts': result}
    except Exception as e:
        return {'success': False, 'error': str(e)}, 500

@app.route('/api/pending_newsletters')
def api_pending_newsletters():
    """Get pending newsletter subscribers for welcome emails"""
    try:
        # Get recent newsletter subscribers
        subscribers = NewsletterSubscriber.query.filter_by(is_active=True).order_by(NewsletterSubscriber.subscribed_at.desc()).limit(100).all()
        
        result = []
        for subscriber in subscribers:
            result.append({
                'id': subscriber.id,
                'email': subscriber.email,
                'subscribed_at': subscriber.subscribed_at.isoformat() if subscriber.subscribed_at else None
            })
        
        return {'success': True, 'subscribers': result}
    except Exception as e:
        return {'success': False, 'error': str(e)}, 500

@app.route('/api/mark_contact_sent/<int:contact_id>', methods=['POST'])
def api_mark_contact_sent(contact_id):
    """Mark contact message as processed"""
    try:
        contact = ContactMessage.query.get_or_404(contact_id)
        # You can add a 'processed' field here if needed
        return {'success': True, 'message': f'Contact {contact_id} marked as sent'}
    except Exception as e:
        return {'success': False, 'error': str(e)}, 500

@app.route('/api/mark_newsletter_sent/<int:subscriber_id>', methods=['POST'])
def api_mark_newsletter_sent(subscriber_id):
    """Mark newsletter welcome as sent"""
    try:
        subscriber = NewsletterSubscriber.query.get_or_404(subscriber_id)
        # You can add a 'welcome_sent' field here if needed
        return {'success': True, 'message': f'Newsletter {subscriber_id} marked as sent'}
    except Exception as e:
        return {'success': False, 'error': str(e)}, 500

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5001)