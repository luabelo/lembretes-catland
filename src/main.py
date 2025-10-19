from datetime import datetime
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from reminder_rules import check_reminders
from email_sender import send_reminder_email


def main():
    today = datetime.now()
    active_reminders = check_reminders(today)
    
    if not active_reminders:
        print("Nenhum lembrete para hoje.")
        return
    
    print(f"Enviando {len(active_reminders)} lembrete(s)...")
    
    for reminder in active_reminders:
        send_reminder_email(reminder['subject'], reminder['message'])
        print(f"✓ {reminder['subject']}")
    
    print("Concluído!")


if __name__ == "__main__":
    main()
