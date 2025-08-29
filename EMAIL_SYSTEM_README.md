# 📧 Vlasia Blog Email System

## 🎯 **Σκοπός**
Το email system του Vlasia Blog διαχειρίζεται την αποστολή emails για:
- **Welcome emails** σε νέους newsletter subscribers
- **Announcements** σε όλους τους newsletter subscribers  
- **Contact notifications** στον admin για νέα μηνύματα επικοινωνίας

## 🏗️ **Αρχιτεκτονική**

### **Server Side** (Digital Ocean)
- **Flask App** με email tracking models
- **API Endpoints** για email management
- **Database** με tracking fields (`welcome_email_sent`, `sent_to_newsletter`, `notification_sent`)

### **Local Side** (PC)
- **EMAIL_SENDER_APP** με web UI στο port 5002
- **Automated email sender** κάθε 5 λεπτά
- **Gmail SMTP** για αποστολή emails

## 🚀 **Πώς Λειτουργεί**

1. **Website** → Δημιουργεί pending emails (newsletter subscriptions, announcements)
2. **Local Email Sender** → Ελέγχει κάθε 5 λεπτά για νέα emails
3. **Gmail SMTP** → Στέλνει τα emails
4. **Server API** → Mark emails ως sent (send-once logic)

## 📁 **File Structure**

```
EMAIL_SENDER_APP/
├── app.py                 # Main Flask application
├── data/
│   ├── config.json       # Configuration settings
│   └── email_logs.log    # Email sending logs
├── templates/
│   ├── dashboard.html    # Main dashboard
│   ├── logs.html         # Logs viewer
│   └── settings.html     # Configuration settings
├── static/               # CSS/JS files
├── requirements.txt      # Python dependencies
└── start.sh             # Startup script
```

## ⚙️ **Configuration**

### **Gmail SMTP Settings**
```json
{
  "gmail_user": "vlasia.blog@gmail.com",
  "gmail_password": "nxwh upvi kges tfqd",
  "server_url": "http://138.68.21.230",
  "check_interval": 300
}
```

### **Server API Endpoints**
- `GET /api/pending_newsletters` - Newsletter subscribers waiting for welcome emails
- `GET /api/pending_announcements` - Announcements waiting to be sent
- `GET /api/pending_contacts` - Contact messages waiting for notifications
- `POST /api/mark_newsletter_sent/{id}` - Mark welcome email as sent
- `POST /api/mark_announcement_sent/{id}` - Mark announcement as sent
- `POST /api/mark_contact_notification_sent/{id}` - Mark contact notification as sent

## 🚀 **Installation & Setup**

### **1. Start the Email Sender App**
```bash
cd EMAIL_SENDER_APP
chmod +x start.sh
./start.sh
```

### **2. Access the Web UI**
Ανοιχτό το browser στο: http://localhost:5002

### **3. Configure Settings**
- Πηγαίνετε στο "Settings" tab
- Εισάγετε το Gmail App Password
- Ρυθμίστε το check interval (προτεινόμενο: 300 seconds)

### **4. Start Email Sender**
- Πατήστε "Εκκίνηση Email Sender"
- Το system θα αρχίσει να στέλνει emails αυτόματα

## 📧 **Email Types**

### **Welcome Emails**
- **Trigger**: Νέα newsletter subscription
- **Recipient**: Newsletter subscriber
- **Content**: Καλώς ήρθατε μήνυμα με πληροφορίες
- **Frequency**: Μία φορά ανά subscriber

### **Announcements**
- **Trigger**: Νέα ανακοίνωση από admin
- **Recipient**: Όλοι οι active newsletter subscribers
- **Content**: Τίτλος, περιεχόμενο, κατηγορία, προτεραιότητα
- **Frequency**: Μία φορά ανά ανακοίνωση

### **Contact Notifications**
- **Trigger**: Νέα επικοινωνία από contact form
- **Recipient**: Admin (vlasia.blog@gmail.com)
- **Content**: Στοιχεία επικοινωνίας και μήνυμα
- **Frequency**: Μία φορά ανά contact message

## 🔍 **Monitoring & Logs**

### **Dashboard Status**
- ✅ **Ενεργό/Ανενεργό** - Current status
- ⏰ **Τελευταία Εκτέλεση** - Last email check
- 📊 **Συνολικά Emails** - Total emails sent
- ⚠️ **Τελευταίο Σφάλμα** - Last error (if any)

### **Logs**
- **Location**: `data/email_logs.log`
- **Content**: Email sending attempts, successes, errors
- **View**: Web UI → Logs tab

### **Real-time Updates**
- Status auto-refreshes κάθε 10 δευτερόλεπτα
- Current task display
- Live error reporting

## 🛠️ **Troubleshooting**

### **Common Issues**

#### **1. Gmail Authentication Failed**
- ✅ Ελέγξτε ότι το App Password είναι σωστό
- ✅ Βεβαιωθείτε ότι το 2FA είναι ενεργό
- ✅ Δοκιμάστε το "Test Email" button

#### **2. Server Connection Failed**
- ✅ Ελέγξτε ότι ο server τρέχει (http://138.68.21.230)
- ✅ Δοκιμάστε το "Test Server Connection" button
- ✅ Ελέγξτε το firewall settings

#### **3. No Emails Being Sent**
- ✅ Ελέγξτε ότι υπάρχουν pending emails στο server
- ✅ Βεβαιωθείτε ότι το email sender είναι ενεργό
- ✅ Ελέγξτε τα logs για errors

### **Debug Steps**
1. **Check Server Status**: `curl http://138.68.21.230/`
2. **Check Pending Emails**: `curl http://138.68.21.230/api/pending_newsletters`
3. **View Local Logs**: Web UI → Logs tab
4. **Test Email Sending**: Web UI → Test Email button

## 🔐 **Security Notes**

- **Gmail App Password** αποθηκεύεται τοπικά στο `config.json`
- **Server API** είναι public (μόνο για email data)
- **Email content** δεν περιέχει ευαίσθητες πληροφορίες
- **Logs** αποθηκεύονται τοπικά

## 📈 **Performance**

### **Check Intervals**
- **60 seconds** - Γρήγορη ελέγχιση (για testing)
- **300 seconds** - Κάθε 5 λεπτά (προτεινόμενο)
- **900 seconds** - Κάθε 15 λεπτά (για production)

### **Email Limits**
- **Gmail SMTP**: 500 emails/day (free account)
- **Rate Limiting**: 1 email/second για Gmail
- **Batch Processing**: Newsletter subscribers processed in batches

## 🎉 **Success Indicators**

- ✅ **Dashboard Status**: "Ενεργό" με green indicator
- ✅ **Test Email**: Successful delivery
- ✅ **Server Connection**: "Server connection successful"
- ✅ **Logs**: Regular "Email sent successfully" messages
- ✅ **Pending Counts**: Decreasing pending email counts

## 📞 **Support**

Για technical support ή questions:
- **Email**: vlasia.blog@gmail.com
- **Logs**: Check the web UI logs tab
- **Status**: Monitor the dashboard in real-time

---

**Created**: 2025-08-27  
**Version**: 1.0  
**Status**: ✅ Production Ready
