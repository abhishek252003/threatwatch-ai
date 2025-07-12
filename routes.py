from flask import request
from app import app
import json

@app.route('/api/collect', methods=['POST'])
def collect_traffic():
    data = request.get_json()
    print("Received traffic data:", data)
    # TODO: Preprocess and run through model
    return {"status": "received"}, 200
