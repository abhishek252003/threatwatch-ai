import time
import requests
import socket

def simulate_traffic():
    traffic_data = {
        "src_ip": socket.gethostbyname(socket.gethostname()),
        "dest_ip": "8.8.8.8",
        "protocol": "TCP",
        "packet_size": 540,
        "timestamp": time.time()
    }
    try:
        res = requests.post("http://localhost:5000/api/collect", json=traffic_data)
        print("Sent:", res.status_code)
    except Exception as e:
        print("Failed to send data:", e)

if __name__ == "__main__":
    while True:
        simulate_traffic()
        time.sleep(5)
