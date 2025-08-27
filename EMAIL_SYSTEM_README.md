# 📧 Email System για το Vlasia Blog

## 🎯 **Τι κάνει αυτό το σύστημα;**

Αντί να στέλνει emails απευθείας από τον server (που μπλοκάρει το Digital Ocean), το σύστημα:

1. **Αποθηκεύει τα δεδομένα στον server** (contact forms, newsletter subscriptions)
2. **Εμφανίζει τα στοιχεία στο admin panel** για προβολή
3. **Έχει ένα τοπικό script** που τρέχει με Gmail SMTP για να στέλνει emails

## 🚀 **Πώς να το χρησιμοποιήσεις;**

### **1. Εκκίνηση του Server**

```bash
# Στον Digital Ocean server
cd /var/www/vlasia_blog
git pull origin main
systemctl restart vlasia_blog
```

### **2. Εκκίνηση του Τοπικού Email Script**

```bash
# Τοπικά στον υπολογιστή σου
cd "Site Βλασια Νεα εκδοση"
python email_sender.py
```

## 📋 **Τι συμβαίνει όταν κάποιος:**

### **Αποστέλλει Contact Form:**
1. ✅ Το μήνυμα αποθηκεύεται στη βάση δεδομένων
2. ✅ Εμφανίζεται στο admin panel (`/admin/contactmessage/`)
3. 🔄 Το τοπικό script το διαβάζει και στέλνει notification στο `vlasia.blog@gmail.com`

### **Εγγράφεται στο Newsletter:**
1. ✅ Το email αποθηκεύεται στη βάση δεδομένων
2. ✅ Εμφανίζεται στο admin panel (`/admin/newslettersubscriber/`)
3. 🔄 Το τοπικό script στέλνει welcome email στο subscriber

## 🔧 **Admin Panel Features**

### **Contact Messages:**
- Προβολή όλων των μηνυμάτων επικοινωνίας
- Αναζήτηση με email, όνομα, θέμα
- Φιλτράρισμα κατά ημερομηνία
- Διαγραφή μηνυμάτων

### **Newsletter Subscribers:**
- Προβολή όλων των εγγραφών
- Αναζήτηση με email
- Φιλτράρισμα κατά ημερομηνία και status
- Ενεργοποίηση/απενεργοποίηση subscribers

## 📡 **API Endpoints**

Το σύστημα παρέχει API endpoints για το τοπικό script:

- `GET /api/pending_contacts` - Λήψη pending contact messages
- `GET /api/pending_newsletters` - Λήψη pending newsletter subscribers
- `POST /api/mark_contact_sent/<id>` - Σήμανση contact ως αποσταλμένο
- `POST /api/mark_newsletter_sent/<id>` - Σήμανση newsletter ως αποσταλμένο

## ⚙️ **Ρύθμιση**

### **Gmail SMTP:**
Το τοπικό script χρησιμοποιεί:
- **Email:** `vlasia.blog@gmail.com`
- **Password:** `nxwh upvi kges tfqd` (App Password)
- **SMTP:** `smtp.gmail.com:587`

### **Server URL:**
- **Production:** `http://138.68.21.230`
- **Local:** `http://localhost:5001`

## 🚨 **Προσοχή!**

1. **Μην τρέξεις το email script πολλές φορές** - θα στείλεις διπλά emails
2. **Ελέγξε τα admin panels** πριν τρέξεις το script
3. **Το script χρειάζεται internet** για να συνδεθεί στον server

## 🔄 **Workflow**

### **Καθημερινά:**
1. Είσαι στο admin panel και βλέπεις νέα μηνύματα
2. Τρέχεις το `python email_sender.py` τοπικά
3. Το script στέλνει όλα τα pending emails
4. Ελέγχεις τα logs για επιτυχία/αποτυχία

### **Σε περίπτωση προβλήματος:**
1. Ελέγχεις τα server logs: `journalctl -u vlasia_blog -f`
2. Ελέγχεις τα τοπικά logs του email script
3. Ελέγχεις αν το Gmail SMTP λειτουργεί

## 📊 **Monitoring**

### **Server Logs:**
```bash
# Στον server
journalctl -u vlasia_blog -f
```

### **Email Script Logs:**
```bash
# Τοπικά
python email_sender.py 2>&1 | tee email_log.txt
```

## 🎉 **Πλεονεκτήματα**

✅ **Αξιόπιστο** - Δεν εξαρτάται από server SMTP  
✅ **Ελεγχόμενο** - Βλέπεις τι στέλνεται  
✅ **Ασφαλές** - Gmail SMTP με App Password  
✅ **Εύκολο** - Ένα script για όλα τα emails  
✅ **Οικονομικό** - Δωρεάν Gmail SMTP  

## 🆘 **Troubleshooting**

### **"Connection refused" στον server:**
- Ελέγξε αν τρέχει το app: `systemctl status vlasia_blog`
- Επανεκκίνηση: `systemctl restart vlasia_blog`

### **"Authentication failed" στο Gmail:**
- Ελέγξε το App Password
- Ενεργοποίησε 2FA στο Gmail

### **"No pending emails":**
- Ελέγξε τα admin panels για νέα δεδομένα
- Ελέγξε τα API endpoints: `curl http://138.68.21.230/api/pending_contacts`

---

**🎯 Το σύστημα είναι έτοιμο! Απλά τρέξε το `python email_sender.py` όταν θέλεις να στείλεις emails.**
