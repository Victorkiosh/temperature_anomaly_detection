"""
deployment/inference.py
-----------------------
Contains the anomaly detection logic and integrates:
1. Model inference (LSTM reconstruction)
2. Statistical error-based detection
3. Persistence rule (consecutive anomalies)
4. Operational bound check
5. Hybrid decision rule
"""

import numpy as np
import joblib
import tensorflow as tf
from deployment.config import MODEL_PATH, SCALER_PATH, MIN_TEMP, MAX_TEMP, PERSISTENCE_N

# === MODEL AND SCALER LOADING ===
# These are loaded once when the API starts
model = tf.keras.models.load_model(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)

# Track recent anomalies for persistence rule
recent_anomalies = []


def detect_anomaly(data_point: float):
    """
    Runs hybrid anomaly detection on a single temperature reading.

    Steps:
    1. Scale input using the same scaler from training.
    2. Use the LSTM model to reconstruct the reading.
    3. Compute reconstruction error (difference between actual and predicted).
    4. Compare error to a statistical threshold.
    5. Apply persistence filter: require N consecutive anomalies.
    6. Apply absolute temperature bounds.
    7. Combine both (hybrid) to decide whether to raise an alert.

    Args:
        data_point (float): Temperature reading in °C.

    Returns:
        dict: Detection results including reconstruction error, raw anomaly flag,
              persistence alert, bounds breach, and final hybrid decision.
    """

    # --- Preprocessing ---
    scaled = scaler.transform(np.array([[data_point]]))

    # --- Model reconstruction ---
    recon = model.predict(scaled.reshape(1, 1, 1), verbose=0)
    error = abs(scaled - recon[0][0])

    # --- Basic statistical threshold ---
    threshold = 0.2  # This can be tuned empirically

    # --- Raw anomaly flag ---
    is_anom_raw = error > threshold

    # --- Persistence rule: track consecutive anomalies ---
    recent_anomalies.append(bool(is_anom_raw))
    if len(recent_anomalies) > PERSISTENCE_N:
        recent_anomalies.pop(0)

    persistence_alert = all(recent_anomalies[-PERSISTENCE_N:])

    # --- Absolute bounds check ---
    bounds_breach = (data_point < MIN_TEMP) or (data_point > MAX_TEMP)

    # --- Final hybrid alert ---
    hybrid_alert = bool(persistence_alert or bounds_breach)

    return {
        "temperature": data_point,
        "reconstruction_error": float(error),
        "raw_anomaly": bool(is_anom_raw),
        "persistence_alert": bool(persistence_alert),
        "bounds_breach": bool(bounds_breach),
        "hybrid_alert": hybrid_alert
    }
