import imaplib
import email
from email.header import decode_header
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from nlp_classifier.process_email import process_email
from data_storage.store_complaint import store_complaint

# ------------------ CONFIG ------------------ #
EMAIL = "civicpalo1@gmail.com"  # your Gmail
PASSWORD = "rbit dlck xznx qbsp"  # your App Password from Gmail
IMAP_SERVER = "imap.gmail.com"
# -------------------------------------------- #

def clean_text(text):
    return "".join(c if c.isalnum() or c.isspace() else " " for c in text)

def fetch_unread_emails():
    print("📥 Connecting to Gmail...")

    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL, PASSWORD)
    mail.select("inbox")

    # DEBUG MODE: Fetch all emails for testing
    status, messages = mail.search(None, 'ALL')  # You can switch to '(UNSEEN)' later
    print("🔍 IMAP Search Status:", status)
    print("🔍 IMAP Response (email IDs):", messages)

    email_ids = messages[0].split()
    print(f"📨 Found {len(email_ids)} emails.")

    for eid in email_ids:
        print(f"📩 Fetching email ID: {eid.decode()}")
        status, msg_data = mail.fetch(eid, "(RFC822)")
        raw_email = msg_data[0][1]
        msg = email.message_from_bytes(raw_email)

        subject, encoding = decode_header(msg["Subject"])[0]
        if isinstance(subject, bytes):
            subject = subject.decode(encoding or "utf-8", errors="ignore")

        from_ = msg.get("From")

        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode(errors="ignore")
                    break
        else:
            body = msg.get_payload(decode=True).decode(errors="ignore")

        # Clean and analyze
        subject = clean_text(subject)
        body = clean_text(body)

        print(f"🔍 Processing email from {from_}: {subject}")
        result = process_email(subject, body)
        store_complaint(subject, body, result)

        print("✅ Complaint stored.\n")

    mail.logout()

# Run it!
if __name__ == "__main__":
    fetch_unread_emails()
