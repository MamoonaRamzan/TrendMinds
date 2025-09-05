from flask import Flask, request, jsonify
from flask_cors import CORS
import requests, os

app = Flask(__name__)
CORS(app)   # ✅ allow frontend requests

# Load from env
GITHUB_PAT = os.getenv("GITHUB_PAT")
OWNER = "MamoonaRamzan"
REPO = "AI-Newsletter"
WORKFLOW_FILE = "subscribe.yml"   # must exist in .github/workflows/

@app.route("/subscribe", methods=["POST"])
def subscribe():
    data = request.json
    email = data.get("email")
    niche = data.get("niche")

    if not email or not niche:
        return jsonify({"error": "Email and niche are required"}), 400

    url = f"https://api.github.com/repos/{OWNER}/{REPO}/actions/workflows/{WORKFLOW_FILE}/dispatches"
    headers = {
        "Authorization": f"token {GITHUB_PAT}",
        "Accept": "application/vnd.github+json"
    }
    payload = {"ref": "main", "inputs": {"email": email, "niche": niche}}

    r = requests.post(url, headers=headers, json=payload)
    if r.status_code == 204:
        return jsonify({"message": f"✅ Subscribed {email} to {niche}"}), 200
    else:
        return jsonify({"error": "GitHub API failed", "details": r.text}), 500

if __name__ == "__main__":
    app.run(port=5000, debug=True)
