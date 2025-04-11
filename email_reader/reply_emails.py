import imaplib
import email
from email.header import decode_header
import os
import sys
import re
from datetime import datetime
from collections import defaultdict
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib

# Add import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from data_storage.store_complaint import store_complaint, get_all_complaints

# Email login for IMAP and SMTP
EMAIL = "civicpalo1@gmail.com"
PASSWORD = "rbit dlck xznx qbsp"
IMAP_SERVER = "imap.gmail.com"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
THRESHOLD = 5  # Complaints per constituency

def clean(text):
    return re.sub(r'\W+', ' ', text)

def extract_complaint_details(subject, body):
    category_keywords = {
        "water": "Water",
        "electricity": "Electricity",
        "sewage": "Sewage",
        "garbage": "Garbage",
        "road": "Road"
    }

    category = "Unknown"
    for word, cat in category_keywords.items():
        if word in body.lower():
            category = cat
            break

    constituency = "Unknown"
    for area in ["BTM", "Jayanagar", "Dasarahalli", "Whitefield", "Indiranagar"]:
        if area.lower() in body.lower():
            constituency = area
            break

    department_map = {
        "Water": "BWSSB",
        "Electricity": "BESCOM",
        "Sewage": "BBMP - Sewage",
        "Garbage": "BBMP - Waste",
        "Road": "BBMP - Roads"
    }

    department = department_map.get(category, "Unassigned")

    result = {
        "category": category,
        "constituency": constituency,
        "department": department,
        "confidence": 0.9
    }

    return subject.strip(), body.strip(), result

def send_constituency_alert(constituency, complaints):
    subject = f"🚨 Alert: {len(complaints)} Complaints from {constituency}"
    body_lines = [f"🔸 {c.get('subject', '')} — {c.get('category', '')}" for c in complaints]
    body = (
        f"Hello,\n\n"
        f"The following {len(complaints)} complaints have been received from {constituency}:\n\n"
        + "\n".join(body_lines) +
        "\n\nPlease take appropriate action.\n\nRegards,\nCivic Portal - QuantumX"
    )

    msg = MIMEMultipart()
    msg["From"] = EMAIL
    msg["To"] = EMAIL
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL, PASSWORD)
            server.sendmail(EMAIL, EMAIL, msg.as_string())
            print(f"✅ Sent alert email for {constituency} ({len(complaints)} complaints)")
    except Exception as e:
        print(f"❌ Failed to send alert: {e}")

def fetch_unread_emails():
    print("📥 Connecting to Gmail...")
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL, PASSWORD)
    mail.select("inbox")

    status, messages = mail.search(None, '(UNSEEN)')
    email_ids = messages[0].split()
    print(f"🔍 Found {len(email_ids)} unread email(s).")

    for eid in email_ids:
        _, msg_data = mail.fetch(eid, "(RFC822)")
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding if encoding else "utf-8")

                if msg.is_multipart():
                    for part in msg.walk():
                        content_type = part.get_content_type()
                        content_disposition = str(part.get("Content-Disposition"))
                        if content_type == "text/plain" and "attachment" not in content_disposition:
                            body = part.get_payload(decode=True).decode()
                            break
                else:
                    body = msg.get_payload(decode=True).decode()

                print(f"📨 Processing email: {subject}")
                subject_clean, body_clean, extracted = extract_complaint_details(subject, body)
                store_complaint(subject_clean, body_clean, extracted)

    mail.logout()

    # After storing, re-load complaints and check threshold
    complaints = get_all_complaints()
    constituency_map = defaultdict(list)
    for c in complaints:
        if c.get("status") == "unresolved":
            constituency_map[c.get("constituency", "Unknown")].append(c)

    for constituency, items in constituency_map.items():
        if len(items) >= THRESHOLD:
            send_constituency_alert(constituency, items)

if __name__ == "__main__":
    fetch_unread_emails()
