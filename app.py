from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from model.anomaly_model import AnomalyDetector

app = Flask(__name__)

# Allow only requests from frontend
CORS(app, origins=["http://localhost:3000"])

# Rate limiter (global default and per route example)
limiter = Limiter(
    key_func=get_remote_address,
    app=app,
    default_limits=["100 per minute"]
)

# Load ML anomaly model
detector = AnomalyDetector()
detector.load_model("model/model.pkl")


# In-memory log store
log_store = []

# Payload validation
def is_valid_payload(data):
    required_keys = {"src_ip", "dest_ip", "protocol", "packet_size", "timestamp"}
    return (
        isinstance(data, dict) and
        required_keys.issubset(data) and
        isinstance(data["packet_size"], (int, float)) and
        isinstance(data["src_ip"], str) and
        isinstance(data["dest_ip"], str) and
        isinstance(data["protocol"], str)
    )

@app.route('/')
def home():
    return jsonify({"status": "ThreatWatch AI API is running"})

@app.route('/api/collect', methods=['POST'])
@limiter.limit("20 per minute")  # Optional fine-tuned limit for this route
def collect_traffic():
    data = request.get_json()

    if not is_valid_payload(data):
        return jsonify({"error": "Invalid traffic data format"}), 400

    result = detector.predict(data)
    is_anomaly = result == -1

    print("Received:", data)
    print("⚠️ Anomaly detected!" if is_anomaly else "✅ Normal traffic.")

    log_store.append({
        **data,
        "anomaly": str(is_anomaly)
    })

    # Keep last 100 entries
    if len(log_store) > 100:
        log_store.pop(0)

    return jsonify({
        "status": "received",
        "anomaly": str(is_anomaly)
    }), 200

@app.route('/api/logs', methods=['GET'])
def get_logs():
    return jsonify({"logs": log_store})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
