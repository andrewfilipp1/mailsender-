# 🌲 Βλασία - Χωριά του Βουνού Βλασίας

Ένα πλήρες website για τα χωριά Άνω Βλασία (1.100μ) και Κάτω Βλασία (800μ) που βρίσκονται στο βουνό Βλασίας, στην περιοχή των Καλαβρύτων της Αχαΐας. Το site περιλαμβάνει νέα, ανακοινώσεις, admin panel και υψηλή παραμετροποιησιμότητα για μελλοντικές επεκτάσεις.

## ✨ Χαρακτηριστικά

- **🌿 Nature Theme**: Όμορφο design με χρώματα φύσης και δάσους
- **📰 Νέα & Ανακοινώσεις**: Πλήρες σύστημα διαχείρισης περιεχομένου
- **🖼️ Εικόνες & Media**: Υποστήριξη για εικόνες και βίντεο
- **👨‍💼 Admin Panel**: Εύκολη διαχείριση περιεχομένου
- **📱 Responsive Design**: Προσαρμογή σε όλες τις συσκευές
- **🔍 Αναζήτηση & Φιλτράρισμα**: Εύκολη εύρεση περιεχομένου
- **🌐 SEO Friendly**: Βελτιστοποιημένο για μηχανές αναζήτησης
- **⚡ Γρήγορο**: Βελτιστοποιημένο για καλή απόδοση

## 🚀 Εγκατάσταση

### Προαπαιτούμενα

- Python 3.8+
- pip
- Virtual environment (προτεινόμενο)

### Βήματα εγκατάστασης

1. **Κλωνοποίηση του repository**
```bash
git clone <repository-url>
cd vlasia-website
```

2. **Δημιουργία virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ή
venv\Scripts\activate  # Windows
```

3. **Εγκατάσταση dependencies**
```bash
pip install -r requirements.txt
```

4. **Εκκίνηση της εφαρμογής**
```bash
python app.py
```

5. **Πρόσβαση στο site**
- Ανοίξτε τον browser στο: `http://localhost:5000`
- Admin panel: `http://localhost:5000/admin/`

## 🔑 Προεπιλεγμένα στοιχεία σύνδεσης

- **Username**: `admin`
- **Password**: `admin123`

**⚠️ Σημαντικό**: Αλλάξτε τον κωδικό πρόσβασης πριν το deployment!

## 🏗️ Αρχιτεκτονική

### Backend
- **Flask**: Web framework
- **SQLAlchemy**: Database ORM
- **SQLite**: Database (εύκολο για development)
- **Flask-Admin**: Admin interface
- **Flask-Login**: Authentication

### Frontend
- **Bootstrap 5**: CSS framework
- **Font Awesome**: Icons
- **Custom CSS**: Nature theme με CSS variables
- **Responsive design**: Mobile-first approach

### Database Models
- **User**: Χρήστες και διαχειριστές
- **Category**: Κατηγορίες άρθρων
- **Article**: Άρθρα και νέα
- **Media**: Αρχεία και εικόνες

## 📁 Δομή Project

```
vlasia-website/
├── app.py                 # Κύριο Flask application
├── requirements.txt       # Python dependencies
├── templates/            # HTML templates
│   ├── base.html        # Base template
│   ├── index.html       # Αρχική σελίδα
│   ├── news.html        # Σελίδα νέων
│   ├── article_detail.html # Λεπτομέρεια άρθρου
│   ├── category.html    # Σελίδα κατηγορίας
│   ├── about.html       # Σχετικά με το χωριό
│   ├── contact.html     # Επικοινωνία
│   ├── login.html       # Σύνδεση
│   ├── create_article.html # Δημιουργία άρθρου
│   ├── 404.html         # Error page
│   └── 500.html         # Server error
├── static/              # Static files
│   └── uploads/         # Uploaded images
└── README.md            # Αυτό το αρχείο
```

## 🌐 Deployment

### Επιλογές Hosting

#### Δωρεάν Επιλογές
1. **Render** - Δωρεάν tier με Python support
2. **Railway** - Δωρεάν tier για μικρά projects
3. **PythonAnywhere** - Εξαιρετικό για Python apps

#### Φτηνές Επιλογές
1. **DigitalOcean** - $5/μήνα (προτεινόμενο)
2. **Linode** - $5/μήνα
3. **Vultr** - $3.5/μήνα

### Βήματα Deployment

1. **Προετοιμασία για production**
```python
# Στο app.py, αλλάξτε:
app.config['SECRET_KEY'] = 'your-very-secure-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://...'  # ή MySQL
```

2. **Environment Variables**
```bash
export FLASK_ENV=production
export SECRET_KEY=your-secret-key
export DATABASE_URL=your-database-url
```

3. **WSGI Server**
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

## 🔧 Προσαρμογές

### Χρώματα Theme
Τα χρώματα μπορούν να αλλάξουν στο `templates/base.html`:

```css
:root {
    --primary-color: #2d5016;      /* Πράσινο δάσους */
    --secondary-color: #4a7c59;    /* Πράσινο βουνών */
    --accent-color: #8fbc8f;       /* Πράσινο φύλλων */
    --earth-color: #8b4513;        /* Καφέ γης */
    --forest-green: #228b22;       /* Πράσινο δάσους */
    --mountain-gray: #696969;      /* Γκρι βουνών */
    --light-beige: #f5f5dc;       /* Ανοιχτό μπεζ */
    --dark-brown: #3e2723;         /* Σκούρο καφέ */
}
```

### Προσθήκη νέων σελίδων
1. Δημιουργήστε νέο template στο `templates/`
2. Προσθέστε route στο `app.py`
3. Ενημερώστε το navigation στο `base.html`

### Προσθήκη νέων κατηγοριών
```python
# Στο app.py, προσθέστε:
new_category = Category(
    name='Νέα Κατηγορία',
    slug='nea-katigoria',
    description='Περιγραφή κατηγορίας'
)
db.session.add(new_category)
db.session.commit()
```

## 📱 Responsive Design

Το site είναι πλήρως responsive και προσαρμόζεται σε:
- 📱 Mobile phones
- 📱 Tablets
- 💻 Desktop computers
- 🖥️ Large screens

## 🔒 Ασφάλεια

- **CSRF Protection**: Με Flask-WTF
- **Password Hashing**: Με Werkzeug
- **Secure File Uploads**: Validation και sanitization
- **Admin Authentication**: Secure admin panel
- **SQL Injection Protection**: Με SQLAlchemy

## 🚀 Μελλοντικές Επεκτάσεις

- **🛒 E-shop**: Πωλήσεις τοπικών προϊόντων
- **📊 Analytics**: Google Analytics integration
- **📧 Newsletter**: Email subscriptions
- **🗺️ Maps**: Interactive maps με τοποθεσίες
- **📱 Mobile App**: Native mobile application
- **🌐 Multi-language**: Υποστήριξη για άλλες γλώσσες
- **📸 Gallery**: Photo gallery με albums
- **📅 Events Calendar**: Ημερολόγιο εκδηλώσεων

## 🐛 Troubleshooting

### Συνήθη προβλήματα

1. **Import errors**
```bash
pip install -r requirements.txt
```

2. **Database errors**
```bash
# Διαγράψτε το αρχείο vlasia.db και επανεκκινήστε
rm vlasia.db
python app.py
```

3. **Permission errors στα uploads**
```bash
chmod 755 static/uploads/
```

4. **Port already in use**
```bash
# Αλλάξτε το port στο app.py
app.run(debug=True, port=5001)
```

## 📞 Υποστήριξη

Για ερωτήσεις ή προβλήματα:
- 📧 Email: info@vlasia.gr
- 📱 Τηλέφωνο: +30 123 456 789
- 🌐 Website: www.vlasia.gr

## 📄 Άδεια

Αυτό το project είναι ανοιχτού κώδικα και διατίθεται υπό την άδεια MIT.

## 🙏 Ευχαριστίες

- **Flask** team για το εξαιρετικό web framework
- **Bootstrap** team για το CSS framework
- **Font Awesome** για τα icons
- **Unsplash** για τις εικόνες background

---

**Καλή χρήση! 🌲✨**
