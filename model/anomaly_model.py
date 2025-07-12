from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import numpy as np
import pickle

class AnomalyDetector:
    def __init__(self):
        self.model = IsolationForest(n_estimators=100, contamination=0.1)
        self.scaler = StandardScaler()

    def extract_features(self, data):
        """
        Extract numeric features for anomaly detection:
        - packet_size
        - normalized_time (seconds within current hour)
        - protocol (TCP=0, UDP=1, ICMP=2, other=3)
        """
        normalized_time = data['timestamp'] % 3600  # normalize timestamp to 0–3600
        protocol_map = {"TCP": 0, "UDP": 1, "ICMP": 2}
        protocol_num = protocol_map.get(data.get("protocol", "").upper(), 3)

        return np.array([[data['packet_size'], normalized_time, protocol_num]])

    def fit(self, training_data):
        """
        Train the model using a list of traffic dicts
        """
        features = [self.extract_features(d)[0] for d in training_data]
        self.scaler.fit(features)
        scaled_features = self.scaler.transform(features)
        self.model.fit(scaled_features)

    def predict(self, data):
        """
        Predict anomaly for a single data point
        """
        feature = self.extract_features(data)
        scaled = self.scaler.transform(feature)
        return self.model.predict(scaled)[0]  # -1 means anomaly, 1 means normal

    def save_model(self, path="model.pkl"):
        """
        Save model and scaler
        """
        with open(path, "wb") as f:
            pickle.dump((self.model, self.scaler), f)

    def load_model(self, path="model/model.pkl"):
        """
        Load model and scaler
        """
        with open(path, "rb") as f:
            self.model, self.scaler = pickle.load(f)
