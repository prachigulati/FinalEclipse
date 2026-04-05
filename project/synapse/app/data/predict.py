import numpy as np
import joblib
import os
from .extract_features import extract_features
from django.conf import settings

# Load model correctly using BASE_DIR
MODEL_PATH = os.path.join(settings.BASE_DIR, "synapse/app/models/dementia_model.pkl")
SCALER_PATH = os.path.join(settings.BASE_DIR, "synapse/app/models/scaler.pkl")

model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)


def predict_audio(audio_path):
    features = extract_features(audio_path)

    if features is None:
        return None, None

    features = features.reshape(1, -1)
    features = scaler.transform(features)

    pred = model.predict(features)[0]
    prob = model.predict_proba(features)[0]

    label = "Dementia" if pred == 1 else "✅ No Dementia"
    confidence = float(np.max(prob))

    return label, confidence