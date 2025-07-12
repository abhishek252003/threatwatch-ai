from scapy.all import sniff, IP, TCP, UDP, ICMP
import requests
import time

API_URL = "http://localhost:5000/api/collect"

def send_to_api(packet):
    if IP in packet:
        proto = ""
        if TCP in packet:
            proto = "TCP"
        elif UDP in packet:
            proto = "UDP"
        elif ICMP in packet:
            proto = "ICMP"
        else:
            return  # skip unsupported protocols

        data = {
            "src_ip": packet[IP].src,
            "dest_ip": packet[IP].dst,
            "protocol": proto,
            "packet_size": len(packet),
            "timestamp": time.time()
        }

        try:
            res = requests.post(API_URL, json=data)
            print(f"Sent packet: {data} | Response: {res.status_code}")
        except requests.exceptions.RequestException as e:
            print("❌ Failed to send:", e)

print("📡 Starting live traffic capture...")
sniff(prn=send_to_api, store=False, filter="ip", count=0)
