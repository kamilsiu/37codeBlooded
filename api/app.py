from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

COMPLAINTS_FILE = os.path.join(os.path.dirname(__file__), '..', 'data_storage', 'complaints.json')

# Utility function to load complaints
def load_complaints():
    if os.path.exists(COMPLAINTS_FILE):
        with open(COMPLAINTS_FILE, 'r') as f:
            return json.load(f)
    return []

# Route to get complaints for a constituency
@app.route("/api/complaints", methods=["GET"])
def get_complaints():
    constituency = request.args.get("constituency", "").lower()
    all_complaints = load_complaints()

    filtered = [
        c for c in all_complaints
        if c["constituency"].lower() == constituency
    ]

    return jsonify(filtered)

# Route to get stats for a constituency
@app.route("/api/stats", methods=["GET"])
def get_stats():
    constituency = request.args.get("constituency", "").lower()
    all_complaints = load_complaints()

    filtered = [
        c for c in all_complaints
        if c["constituency"].lower() == constituency
    ]

    resolved = sum(1 for c in filtered if c["status"] == "resolved")
    unresolved = len(filtered) - resolved

    return jsonify({
        "total": len(filtered),
        "resolved": resolved,
        "unresolved": unresolved
    })

if __name__ == "__main__":
    app.run(debug=True)
