#!/bin/bash

# 🚀 Quick Start Script για το Site της Βλασίας
# Χρήση: ./start_app.sh

echo "🌲 Ξεκινάει το Site της Βλασίας..."
echo ""

# Έλεγχος αν υπάρχει ο φάκελος WORKING_APP
if [ ! -d "WORKING_APP" ]; then
    echo "❌ Σφάλμα: Ο φάκελος WORKING_APP δεν βρέθηκε!"
    echo "📁 Βεβαιωθείτε ότι είστε στο σωστό directory"
    exit 1
fi

# Μετάβαση στον φάκελο εργασίας
cd WORKING_APP

echo "📁 Εργαζόμενος φάκελος: $(pwd)"
echo ""

# Έλεγχος αν υπάρχει το virtual environment
if [ ! -d ".venv" ]; then
    echo "❌ Σφάλμα: Το virtual environment δεν βρέθηκε!"
    echo "🔧 Δημιουργήστε το με: python3 -m venv .venv"
    exit 1
fi

# Ενεργοποίηση του virtual environment
echo "🐍 Ενεργοποίηση virtual environment..."
source .venv/bin/activate

# Έλεγχος αν υπάρχει το app.py
if [ ! -f "app.py" ]; then
    echo "❌ Σφάλμα: Το app.py δεν βρέθηκε!"
    echo "📁 Βεβαιωθείτε ότι έχετε κάνει backup σωστά"
    exit 1
fi

echo "✅ Όλα έτοιμα!"
echo ""
echo "🌐 Το site θα είναι διαθέσιμο στο: http://localhost:5001"
echo "👨‍💼 Admin panel: http://localhost:5001/admin"
echo ""
echo "⏹️  Για να σταματήσετε, πατήστε Ctrl+C"
echo ""

# Εκκίνηση του Flask app
python3 app.py
