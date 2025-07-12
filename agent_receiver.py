# agent_receiver.py

from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Main backend API URL (change this to your backend address if remote)
MAIN_API_URL = "http://localhost:5000/api/collect"

@app.route("/")
def health_check():
    return {"status": "Agent Receiver is running"}, 200

@app.route("/receive", methods=["POST"])
def receive_traffic():
    try:
        data = request.get_json()
        print("📥 Received traffic from agent:", data)

        # Forward to main backend for processing
        res = requests.post(MAIN_API_URL, json=data)
        print("➡️ Forwarded to main API. Status:", res.status_code)

        return res.json(), res.status_code

    except Exception as e:
        print("❌ Error while forwarding:", str(e))
        return jsonify({"error": "Failed to forward data"}), 500

if __name__ == "__main__":
    app.run(port=6000, debug=True)
