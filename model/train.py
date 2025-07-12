from anomaly_model import AnomalyDetector
import time
import random
import os

# 1. Generate realistic training data
training_data = []

base_time = time.time()

for i in range(200):
    training_data.append({
        "packet_size": random.randint(480, 550),
        "timestamp": base_time + i * random.uniform(4, 7),
        "protocol": "TCP"  # ✅ Added required field for new model
    })

# 2. Initialize and train model
detector = AnomalyDetector()
detector.fit(training_data)

# 3. Save the model safely
os.makedirs("model", exist_ok=True)
save_path = "model.pkl"

try:
    detector.save_model(save_path)
    print(f"✅ Model retrained and saved at {save_path}")
except Exception as e:
    print("❌ Failed to save model:", e)

# 4. Show a sample of the training data
print("\n🔍 Sample training data (first 5 rows):")
for row in training_data[:5]:
    print(row)
