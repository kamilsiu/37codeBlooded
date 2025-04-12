from flask import Flask, render_template, send_from_directory, jsonify
import os
import json
app = Flask(__name__, static_folder="frontend", template_folder="frontend")

COMPLAINTS_FILE = os.path.join(os.path.dirname(__file__), 'data_storage', 'complaints.json')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/resolved')
def resolved():
    return render_template('resolved.html')

@app.route('/emails')
def emails():
    return render_template('emails.html')

@app.route('/api/complaints')
def get_complaints():
    if os.path.exists(COMPLAINTS_FILE):
        with open(COMPLAINTS_FILE, 'r') as f:
            data = json.load(f)
    else:
        data = []
    return jsonify(data)

# Optional: Route to trigger backend fetching
@app.route('/fetch')
def trigger_fetch():
    from email_reader import fetch_emails
    fetch_emails.fetch_unread_emails()
    return "✅ Emails fetched and complaints stored!"

if __name__ == '__main__':
    app.run(debug=True, port=8000)