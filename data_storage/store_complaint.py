import json
import os
from datetime import datetime

COMPLAINTS_FILE = os.path.join(os.path.dirname(__file__), 'complaints.json')

def store_complaint(subject, body, extracted):
    # Load existing complaints
    complaints = get_all_complaints()
    
    # Create new complaint
    complaint = {
        'subject': subject,
        'body': body,
        'category': extracted.get('category', 'Unknown'),
        'constituency': extracted.get('constituency', 'Unknown'),
        'department': extracted.get('department', 'Unassigned'),
        'confidence': extracted.get('confidence', 0.9),
        'status': 'unresolved',
        'filed_date': datetime.utcnow().isoformat() + 'Z',
        'resolved_date': None
    }
    
    complaints.append(complaint)
    
    # Save to file
    with open(COMPLAINTS_FILE, 'w') as f:
        json.dump(complaints, f, indent=2)

def get_all_complaints():
    if not os.path.exists(COMPLAINTS_FILE):
        return []
    
    with open(COMPLAINTS_FILE, 'r') as f:
        return json.load(f)