#!/bin/bash
# Setup Cron Job for Vlasia Blog Email Sender

echo "🚀 Setting up automated email sender for Vlasia Blog..."

# Get the current directory
CURRENT_DIR=$(pwd)
SCRIPT_PATH="$CURRENT_DIR/auto_email_sender.py"

# Make the script executable
chmod +x "$SCRIPT_PATH"

# Create cron job entry (every 15 minutes)
CRON_JOB="*/15 * * * * cd $CURRENT_DIR && python3 $SCRIPT_PATH >> $CURRENT_DIR/cron.log 2>&1"

# Add to crontab
(crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -

echo "✅ Cron job set up successfully!"
echo "📅 Will run every 15 minutes"
echo "📝 Logs will be saved to: $CURRENT_DIR/cron.log"
echo "📧 Script path: $SCRIPT_PATH"

# Show current crontab
echo ""
echo "📋 Current crontab:"
crontab -l

echo ""
echo "🎯 To test the script manually, run:"
echo "   python3 $SCRIPT_PATH"
echo ""
echo "📊 To view logs:"
echo "   tail -f $CURRENT_DIR/cron.log"
echo ""
echo "🛑 To remove the cron job:"
echo "   crontab -e"
echo "   (then delete the line with auto_email_sender.py)"
