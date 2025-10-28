"""
deployment/app.py
-----------------
FastAPI application exposing a REST endpoint for real-time anomaly detection.

Endpoint:
    POST /predict
Example request:
    {
        "temperature": -22.5
    }
"""

from fastapi import FastAPI
from pydantic import BaseModel
from .inference import detect_anomaly


# Initialize the FastAPI application
app = FastAPI(title="Cold Storage Anomaly Detection API", version="1.0.0")


class Reading(BaseModel):
    """Defines the input schema for temperature readings."""
    temperature: float


@app.post("/predict")
def predict(reading: Reading):
    """
    Perform anomaly detection on a single temperature reading.

    Returns:
        JSON response with hybrid detection details.
    """
    result = detect_anomaly(reading.temperature)
    return result
