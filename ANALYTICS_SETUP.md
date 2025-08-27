# 📊 Analytics Setup Guide - Βλασία Website

## 🎯 **Τι Έχουμε Προσθέσει:**

### **1. Google Analytics 4 (GA4)**
- **Tracking Code**: Προσθήκη στο `base.html`
- **Page Views**: Αυτόματη παρακολούθηση σελίδων
- **User Sessions**: Παρακολούθηση επισκεπτών
- **Real-time Data**: Άμεσα στατιστικά

### **2. Enhanced Event Tracking**
- **📧 Newsletter Subscriptions**: Παρακολούθηση εγγραφών
- **📝 Contact Form Submissions**: Παρακολούθηση φορμών επικοινωνίας
- **🖼️ Image Views**: Παρακολούθηση προβολών εικόνων
- **🗺️ Map Interactions**: Παρακολούθηση χρήσης χάρτη
- **🔗 External Links**: Παρακολούθηση εξωτερικών συνδέσμων

### **3. Admin Dashboard**
- **📊 Statistics Cards**: Συνολικές ανακοινώσεις, δημοσιευμένες, newsletter
- **📈 Media Statistics**: Αριθμός εικόνων και βίντεο
- **⏰ Recent Activity**: Πρόσφατες ανακοινώσεις
- **⚡ Quick Actions**: Γρήγορες ενέργειες admin

## 🚀 **Βήματα Ενεργοποίησης:**

### **Βήμα 1: Δημιουργία Google Analytics Account**
1. Επισκεφθείτε [analytics.google.com](https://analytics.google.com)
2. Δημιουργήστε νέο account για "Βλασία"
3. Δημιουργήστε νέο property για `www.vlasia.gr`
4. Επιλέξτε "Web" ως platform

### **Βήμα 2: Λήψη Tracking ID**
1. Από το property settings, αντιγράψτε το **Measurement ID**
2. Θα είναι στη μορφή: `G-XXXXXXXXXX`
3. Αντικαταστήστε το `G-XXXXXXXXXX` στο `base.html`

### **Βήμα 3: Ενημέρωση Tracking Code**
```html
<!-- Αντικαταστήστε το G-XXXXXXXXXX με το πραγματικό ID σας -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', 'G-XXXXXXXXXX', {
        'page_title': document.title,
        'page_location': window.location.href
    });
</script>
```

## 📈 **Τι Θα Παρακολουθείτε:**

### **📊 Βασικά Metrics:**
- **Page Views**: Πόσες φορές επισκέφθηκε κάθε σελίδα
- **Users**: Πόσοι μοναδικοί επισκέπτες
- **Sessions**: Πόσες επισκέψεις συνολικά
- **Bounce Rate**: Ποσοστό άμεσης εξόδου

### **🎯 Custom Events:**
- **Newsletter Signups**: Πόσοι εγγράφηκαν
- **Contact Form Submissions**: Πόσα μηνύματα στάλθηκαν
- **Image Views**: Πόσες εικόνες προβλήθηκαν
- **Map Interactions**: Πόσες φορές χρησιμοποιήθηκε ο χάρτης

### **🌍 Demographics:**
- **Location**: Από πού επισκέπτονται
- **Device**: Κινητά, tablets, desktop
- **Browser**: Chrome, Safari, Firefox, κλπ
- **Language**: Ελληνικά, Αγγλικά, κλπ

## 🔧 **Προσαρμογές για Βλασία:**

### **1. Local Business Setup**
- **Business Category**: Village/Tourism
- **Location**: Βλασία, Ελλάδα
- **Industry**: Community/News

### **2. Enhanced Ecommerce (Μελλοντικά)**
- **Product Views**: Για e-shop
- **Add to Cart**: Για αγορές
- **Checkout**: Για ολοκλήρωση παραγγελιών

### **3. Custom Dimensions**
- **News Category**: Τύπος ανακοίνωσης
- **Media Type**: Εικόνα ή βίντεο
- **User Role**: Επισκέπτης ή Admin

## 📱 **Mobile Analytics:**
- **Mobile Performance**: Ταχύτητα φόρτωσης
- **User Experience**: Εύκολη χρήση σε κινητά
- **Conversion Rates**: Ποσοστό επιτυχίας σε κινητά

## 🎨 **Dashboard Customization:**
- **Brand Colors**: Χρώματα της Βλασίας
- **Local Language**: Ελληνικά labels
- **Relevant Metrics**: Στατιστικά για χωριό

## 🔒 **Privacy & GDPR:**
- **Cookie Consent**: Συγκατάθεση για cookies
- **Data Retention**: Διατήρηση δεδομένων 26 μηνών
- **User Rights**: Δικαίωμα διαγραφής δεδομένων

## 📊 **Προτεινόμενα Reports:**

### **1. Weekly Reports:**
- Επισκέπτες ανά εβδομάδα
- Δημοφιλέστερες σελίδες
- Newsletter εγγραφές

### **2. Monthly Reports:**
- Τάσεις επισκεψιμότητας
- Επιδόσεις content
- User engagement

### **3. Quarterly Reports:**
- Ανάλυση ανά εποχή
- Tourism patterns
- Content effectiveness

## 🚀 **Επόμενα Βήματα:**

1. **✅ Ενεργοποίηση GA4** - Δημιουργία account
2. **🔄 Testing** - Έλεγχος tracking
3. **📊 Data Collection** - Συλλογή δεδομένων 2-4 εβδομάδες
4. **📈 Analysis** - Ανάλυση patterns
5. **🎯 Optimization** - Βελτίωση βάσει δεδομένων

## 💡 **Tips για Καλύτερα Results:**

- **Regular Monitoring**: Ελέγχος κάθε εβδομάδα
- **Goal Setting**: Ορισμός στόχων (π.χ. 100 newsletter εγγραφές/μήνα)
- **A/B Testing**: Δοκιμή διαφορετικών layouts
- **Content Optimization**: Βελτίωση βάσει analytics
- **User Feedback**: Συνδυασμός με άμεση ανατροφοδότηση

---

**🎉 Με αυτό το setup, θα έχετε πλήρη visibility στο site σας και θα μπορείτε να παίρνετε data-driven αποφάσεις για τη βελτίωση της εμπειρίας των επισκεπτών!**
