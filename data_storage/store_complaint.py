import json
import os
from datetime import datetime

COMPLAINTS_FILE = os.path.join(os.path.dirname(__file__), 'complaints.json')

def store_complaint(subject, body, result):
    """
    Stores the processed complaint as a new entry in complaints.json
    """
    entry = {
        "timestamp": datetime.now().isoformat(),
        "subject": subject,
        "body": body,
        "category": result.get("category", "Unknown"),
        "constituency": result.get("constituency", "Unknown"),
        "department": result.get("department", "Unassigned"),
        "confidence": result.get("confidence", 0.0),
        "status": "unresolved"
    }

    if os.path.exists(COMPLAINTS_FILE):
        with open(COMPLAINTS_FILE, "r") as f:
            data = json.load(f)
    else:
        data = []

    data.append(entry)

    with open(COMPLAINTS_FILE, "w") as f:
        json.dump(data, f, indent=4)

    print("✅ Complaint stored successfully.")

def get_all_complaints():
    """
    Loads and returns all complaints from complaints.json
    """
    if not os.path.exists(COMPLAINTS_FILE):
        return []

    with open(COMPLAINTS_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []
