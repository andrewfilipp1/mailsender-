# Newsletter Mailer System - Οδηγίες Εγκατάστασης

## Επισκόπηση
Αυτό το σύστημα επιτρέπει την αυτόματη αποστολή newsletters από το site σου μέσω εξωτερικού SMTP server, παρακάμπτοντας τους περιορισμούς του server σου.

## Αρχιτεκτονική
```
[Site σου] ←→ [Newsletter Mailer Script] ←→ [SMTP Provider (Gmail/SendGrid)]
     ↑                                           ↑
  API Endpoints                              Email Delivery
```

## Βήμα 1: Προετοιμασία του Site σου

### 1.1 Δημιουργία API Endpoint για Ανάκτηση Δεδομένων

Δημιούργησε ένα endpoint στο site σου: `/api/get-newsletter-batch`

**Παράδειγμα σε Flask:**
```python
@app.route('/api/get-newsletter-batch', methods=['GET'])
def get_newsletter_batch():
    # Έλεγχος API key
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({'error': 'Unauthorized'}), 401
    
    api_key = auth_header.split(' ')[1]
    if api_key != 'YOUR_SECRET_API_KEY':
        return jsonify({'error': 'Invalid API key'}), 401
    
    # Βρες την τελευταία ανακοίνωση που δεν έχει σταλεί σε όλους
    # Επιστροφή σε μορφή JSON:
    return jsonify({
        'announcement_id': 123,
        'subject': 'Νέα Ανακοίνωση',
        'body_html': '<h1>Τίτλος</h1><p>Περιεχόμενο...</p>',
        'recipients': [
            {'user_id': 1, 'email': 'user1@example.com'},
            {'user_id': 2, 'email': 'user2@example.com'}
        ]
    })
```

### 1.2 Δημιουργία API Endpoint για Ενημέρωση Κατάστασης

Δημιούργησε ένα endpoint: `/api/mark-email-sent`

**Παράδειγμα σε Flask:**
```python
@app.route('/api/mark-email-sent', methods=['POST'])
def mark_email_sent():
    # Έλεγχος API key
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({'error': 'Unauthorized'}), 401
    
    api_key = auth_header.split(' ')[1]
    if api_key != 'YOUR_SECRET_API_KEY':
        return jsonify({'error': 'Invalid API key'}), 401
    
    data = request.get_json()
    user_id = data.get('user_id')
    announcement_id = data.get('announcement_id')
    
    # Ενημέρωσε τη βάση δεδομένων ότι το email στάλθηκε
    # UPDATE newsletter_sent SET sent_at = NOW() WHERE user_id = ? AND announcement_id = ?
    
    return jsonify({'success': True})
```

## Βήμα 2: Ρύθμιση SMTP Provider

### Επιλογή 1: Gmail (Δωρεάν)
1. Πήγαινε στο [Google Account Settings](https://myaccount.google.com/security)
2. Ενεργοποίησε "2-Step Verification"
3. Δημιούργησε "App Password" για "Mail"
4. Χρησιμοποίησε αυτόν τον κωδικό ως `SMTP_PASSWORD`

### Επιλογή 2: SendGrid (Δωρεάν έως 100 emails/ημέρα)
1. Δημιούργησε λογαριασμό στο [SendGrid](https://sendgrid.com/)
2. Δημιούργησε API Key
3. Χρησιμοποίησε `smtp.sendgrid.net` ως SMTP server

## Βήμα 3: Ρύθμιση GitHub Actions

### 3.1 Δημιουργία Repository
1. Δημιούργησε νέο repository στο GitHub
2. Ανέβασε όλα τα αρχεία (συμπεριλαμβανομένου του `.github/workflows/`)

### 3.2 Ρύθμιση Secrets
Πήγαινε στο repository → Settings → Secrets and variables → Actions

Δημιούργησε τα παρακάτω secrets:

| Secret Name | Περιγραφή | Παράδειγμα |
|-------------|-----------|------------|
| `API_URL_GET_EMAILS` | URL για ανάκτηση δεδομένων | `https://yoursite.com/api/get-newsletter-batch` |
| `API_URL_MARK_SENT` | URL για ενημέρωση κατάστασης | `https://yoursite.com/api/mark-email-sent` |
| `API_SECRET_KEY` | Το μυστικό κλειδί του API σου | `your_secret_key_here` |
| `SMTP_SERVER` | SMTP server | `smtp.gmail.com` |
| `SMTP_PORT` | SMTP port | `587` |
| `SMTP_USERNAME` | Το email σου | `your_email@gmail.com` |
| `SMTP_PASSWORD` | Ο κωδικός εφαρμογής | `your_app_password` |
| `SENDER_EMAIL` | Email αποστολέα | `your_email@gmail.com` |

### 3.3 Ενεργοποίηση Workflow
Μετά το push, το workflow θα ενεργοποιηθεί αυτόματα και θα τρέχει κάθε 15 λεπτά.

## Βήμα 4: Δοκιμή και Επιβεβαίωση

### 4.1 Χειροκίνητη Εκτέλεση
1. Πήγαινε στο repository → Actions
2. Επίλεξε "Send Newsletter Emails"
3. Πάτα "Run workflow"

### 4.2 Έλεγχος Logs
Τα logs θα είναι διαθέσιμα στο Actions tab και θα ανεβαίνουν ως artifacts.

## Δομή Βάσης Δεδομένων

### Πίνακας Newsletter Subscribers
```sql
CREATE TABLE newsletter_subscribers (
    id INTEGER PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    subscribed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);
```

### Πίνακας Announcements
```sql
CREATE TABLE announcements (
    id INTEGER PRIMARY KEY,
    subject VARCHAR(255) NOT NULL,
    body_html TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_published BOOLEAN DEFAULT FALSE
);
```

### Πίνακας Newsletter Sent
```sql
CREATE TABLE newsletter_sent (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    announcement_id INTEGER,
    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(50) DEFAULT 'sent',
    FOREIGN KEY (user_id) REFERENCES newsletter_subscribers(id),
    FOREIGN KEY (announcement_id) REFERENCES announcements(id)
);
```

## Αντιμετώπιση Προβλημάτων

### Συνήθη Σφάλματα
1. **"Missing required environment variables"**: Έλεγξε τα GitHub Secrets
2. **"SMTP Authentication failed"**: Έλεγξε το SMTP password
3. **"API endpoint not found"**: Έλεγξε τα URLs στο site σου

### Έλεγχος Κατάστασης
- Πήγαινε στο Actions tab για να δεις αν τρέχει το workflow
- Έλεγξε τα logs για σφάλματα
- Επιβεβαίωσε ότι τα API endpoints λειτουργούν

## Ασφάλεια

- Χρησιμοποίησε HTTPS για όλα τα API endpoints
- Κάνε rotate τα API keys τακτικά
- Περιορίσε την πρόσβαση στα API endpoints μόνο από το GitHub Actions
- Χρησιμοποίησε rate limiting στα API endpoints

## Υποστήριξη

Για ερωτήσεις ή προβλήματα:
1. Έλεγξε τα logs στο GitHub Actions
2. Επιβεβαίωσε τη σύνδεση SMTP
3. Ελέγξε τα API endpoints με Postman ή curl
