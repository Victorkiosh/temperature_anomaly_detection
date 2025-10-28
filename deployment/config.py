"""
deployment/config.py
--------------------
Holds configuration constants used across the deployment phase.
"""

import os

# === PATH CONFIGURATION ===
# Locate model and scaler relative to this file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "..", "models", "lstm_model.keras")
SCALER_PATH = os.path.join(BASE_DIR, "..", "models", "scaler.pkl")

# === OPERATIONAL BOUNDS ===
# Example for frozen storage room (temperatures in °C)
MIN_TEMP = -25.0
MAX_TEMP = -18.0

# === ANOMALY LOGIC CONFIG ===
# Persistence rule: an alert is only raised if an anomaly persists N consecutive times
PERSISTENCE_N = 2
