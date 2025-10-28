"""
simulate_stream.py
------------------
Simulates a real-time stream of temperature readings.

How it works:
1. Randomly generates or reads temperature values.
2. Sends each reading to the FastAPI `/predict` endpoint.
3. Logs the API’s response into the local SQLite database.

Run:
    uvicorn deployment.app:app --reload
    python deployment/simulate_stream.py
"""

import time
import random
import requests
import sqlite3
from datetime import datetime
import os


# === API endpoint (FastAPI must be running) ===
API_URL = "http://127.0.0.1:8000/predict"

# === Database path ===
DB_PATH = "deployment/temperature_data.db"

# Debugging: confirm setup
print("Current working directory:", os.getcwd())
print("API URL:", API_URL)
print("Database path:", DB_PATH)
# === Simulation parameters ===
INTERVAL = 5  # seconds between readings
N_SAMPLES = 20  # total number of readings to simulate


def insert_to_db(timestamp, temperature, hybrid_alert):
    """Insert prediction results into SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create table if not exists
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            temperature REAL,
            hybrid_alert INTEGER
        )
    """)

    # Insert record
    cursor.execute("""
        INSERT INTO readings (timestamp, temperature, hybrid_alert)
        VALUES (?, ?, ?)
    """, (timestamp, temperature, int(hybrid_alert)))

    conn.commit()
    conn.close()


def simulate_stream():
    """Main simulation loop."""
    print("🌡️ Starting temperature stream simulation...\n")

    for i in range(N_SAMPLES):
        print(f"Sending reading {i+1}/{N_SAMPLES}...")
        # Random temperature near normal range (-25°C to -15°C)
        temperature = round(random.uniform(-28, -10), 2)

        # Send reading to API
        response = requests.post(API_URL, json={"temperature": temperature})

        if response.status_code == 200:
            result = response.json()
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Log to database
            insert_to_db(timestamp, result["temperature"], result["hybrid_alert"])

            print(f"[{timestamp}] Temp: {temperature}°C → Hybrid Alert: {result['hybrid_alert']}")
        else:
            print(f"❌ API error: {response.status_code}")

        time.sleep(INTERVAL)

    print("\n✅ Simulation complete! Check your database for stored readings.")


if __name__ == "__main__":
    simulate_stream()
