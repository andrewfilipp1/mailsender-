# 🌊 Οδηγίες για την Εικόνα του Καταρράκτη

## 📸 **Πώς να προσθέσετε την εικόνα σας:**

### **Επιλογή 1: Απευθείας στο φάκελο (Προτεινόμενο)**
1. Αντιγράψτε την εικόνα του καταρράκτη στο φάκελο `static/uploads/`
2. Μετονομάστε την σε `vlasia_waterfall.jpg` (ή .png)
3. Ενημερώστε το `templates/base.html`:

```css
.hero-section.vlasia-waterfall {
    background: linear-gradient(rgba(45, 80, 22, 0.5), rgba(74, 124, 89, 0.5)), 
                url('/static/uploads/vlasia_waterfall.jpg');
    /* ... υπόλοιπα styles ... */
}
```

### **Επιλογή 2: Μέσω Admin Panel**
1. Πηγαίνετε στο http://localhost:5001/admin/
2. Συνδεθείτε με admin/admin123
3. Δημιουργήστε νέο άρθρο με την εικόνα
4. Η εικόνα θα αποθηκευτεί στο `static/uploads/`

## 🎯 **Προτεινόμενες προδιαγραφές:**
- **Μέγεθος:** 1920x1080 pixels ή μεγαλύτερο
- **Μορφή:** JPG, PNG, ή WebP
- **Ποιότητα:** Υψηλή (για καλό background)
- **Θέμα:** Καταρράκτης, ρέμα, δάσος της Βλασίας

## 🌟 **Τι έχει αλλάξει:**
- ✅ Hero section με ειδική κλάση `vlasia-waterfall`
- ✅ Full-height background (100vh)
- ✅ Parallax effect (fixed background)
- ✅ Καλύτερα shadows για το κείμενο
- ✅ Responsive design για mobile
- ✅ Gradient overlay για καλύτερη αναγνωσιμότητα

## 🔄 **Για να δείτε τις αλλαγές:**
1. Ανανεώστε τον browser
2. Πηγαίνετε στο http://localhost:5001
3. Η εικόνα θα εμφανιστεί στο hero section!

---

**Η εικόνα του καταρράκτη θα κάνει το site της Βλασίας ακόμα πιο όμορφο!** 🌲💧✨
