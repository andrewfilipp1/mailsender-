# 📁 Οργάνωση Φακέλων - Βλασία Website

## 🎯 **Σκοπός:**
Αυτή η οργάνωση χωρίζει τα backup files από την εργαζόμενη εφαρμογή για καλύτερη διαχείριση και ασφάλεια.

## 📂 **Δομή Φακέλων:**

### **1. 🗂️ `WORKING_APP/` - Η Εργαζόμενη Εφαρμογή**
```
WORKING_APP/
├── app.py                    # Κύριο Flask application
├── vlasia.db                # Βάση δεδομένων
├── requirements.txt          # Python dependencies
├── .venv/                   # Virtual environment
├── templates/               # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── news.html
│   ├── news_detail.html
│   ├── contact.html
│   ├── about.html
│   ├── admin_dashboard.html
│   └── send_newsletter.html
├── static/                  # Static files
│   ├── css/
│   ├── js/
│   └── uploads/
├── BACKUP_README.md         # Οδηγός backup
└── ANALYTICS_SETUP.md       # Οδηγός analytics
```

**🎯 Χρήση:** Εδώ βρίσκεται η τρέχουσα, εργαζόμενη έκδοση του site.

### **2. 🗂️ `BACKUP_SAFE/` - Ασφαλές Backup**
```
BACKUP_SAFE/
├── app_working_backup.py    # Backup του Flask app
├── vlasia_working_backup.db # Backup της βάσης
├── requirements_working_backup.txt # Backup dependencies
├── backup_templates/        # Backup όλων των templates
└── backup_static/           # Backup όλων των static files
```

**🎯 Χρήση:** Ασφαλές backup της εργαζόμενης έκδοσης. Μην αγγίζετε αυτά τα αρχεία!

## 🚀 **Πώς Να Εργαστείτε:**

### **Για Καθημερινή Εργασία:**
```bash
cd WORKING_APP
source .venv/bin/activate
python3 app.py
```

### **Για Backup:**
```bash
# Αν θέλετε να κάνετε νέο backup
cp -r WORKING_APP/* BACKUP_SAFE/

# Αν θέλετε να επαναφέρετε από backup
cp -r BACKUP_SAFE/* WORKING_APP/
```

## 🔒 **Ασφάλεια:**

### **✅ Ασφαλές:**
- **`WORKING_APP/`** - Εδώ κάνετε αλλαγές
- **`BACKUP_SAFE/`** - Μην αγγίζετε αυτά τα αρχεία

### **⚠️ Προσοχή:**
- Μην διαγράψετε το `BACKUP_SAFE/`
- Κάντε backup πριν από μεγάλες αλλαγές
- Δοκιμάστε αλλαγές στο `WORKING_APP/` πρώτα

## 📋 **Εντολές για Διαχείριση:**

### **Εκκίνηση Εργασίας:**
```bash
cd WORKING_APP
source .venv/bin/activate
python3 app.py
```

### **Δημιουργία Νέου Backup:**
```bash
# Δημιουργία timestamp
timestamp=$(date +"%Y%m%d_%H%M%S")

# Δημιουργία νέου backup
mkdir -p BACKUP_SAFE/backup_$timestamp
cp -r WORKING_APP/* BACKUP_SAFE/backup_$timestamp/
```

### **Επαναφορά από Backup:**
```bash
# Επαναφορά όλων των αρχείων
cp -r BACKUP_SAFE/* WORKING_APP/

# Επαναφορά μόνο του app.py
cp BACKUP_SAFE/app_working_backup.py WORKING_APP/app.py

# Επαναφορά μόνο της βάσης
cp BACKUP_SAFE/vlasia_working_backup.db WORKING_APP/vlasia.db
```

## 🎯 **Προτεινόμενη Ρουτίνα:**

### **Πριν από Αλλαγές:**
1. **📋 Backup** - Κάντε backup του `WORKING_APP/`
2. **🧪 Test** - Δοκιμάστε τις αλλαγές
3. **✅ Commit** - Αν δουλεύει, κρατήστε το

### **Μετά από Αλλαγές:**
1. **🔄 Restart** - Restart τον server
2. **🧪 Test** - Δοκιμάστε τη λειτουργικότητα
3. **💾 Save** - Αποθηκεύστε τις αλλαγές

## 💡 **Tips:**

1. **🔒 Κρατήστε το `BACKUP_SAFE/` ασφαλές**
2. **📝 Document τις αλλαγές**
3. **🧪 Test πριν deploy**
4. **💾 Regular backups** κάθε σημαντική αλλαγή

## 🚨 **Emergency Procedures:**

### **Αν Χαλάσει Κάτι:**
```bash
# Επαναφορά από backup
cp -r BACKUP_SAFE/* WORKING_APP/

# Restart server
cd WORKING_APP
source .venv/bin/activate
python3 app.py
```

### **Αν Χάσετε Αρχεία:**
```bash
# Επαναφορά όλων των αρχείων
cp -r BACKUP_SAFE/backup_templates/* WORKING_APP/templates/
cp -r BACKUP_SAFE/backup_static/* WORKING_APP/static/
```

---

**🎉 Με αυτή την οργάνωση, έχετε ξεκάθαρο διαχωρισμό μεταξύ εργασίας και backup!**
