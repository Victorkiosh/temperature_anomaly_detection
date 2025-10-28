"""
deployment/database.py
----------------------
Handles SQLite database connection and table creation
for storing temperature readings and anomaly results.
"""

import sqlite3
from contextlib import contextmanager

DB_PATH = "deployment/temperature_data.db"


@contextmanager
def get_connection():
    """Provides a database connection context."""
    conn = sqlite3.connect(DB_PATH)
    try:
        yield conn
    finally:
        conn.close()


def init_db():
    """Creates the temperature readings table if it doesn’t exist."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS temperature_readings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                temperature REAL NOT NULL,
                reconstruction_error REAL,
                raw_anomaly BOOLEAN,
                persistence_alert BOOLEAN,
                bounds_breach BOOLEAN,
                hybrid_alert BOOLEAN
            )
        """)
        conn.commit()


def insert_reading(reading: dict):
    """Inserts a new reading + anomaly results into the database."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO temperature_readings
            (temperature, reconstruction_error, raw_anomaly, persistence_alert, bounds_breach, hybrid_alert)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            reading["temperature"],
            reading["reconstruction_error"],
            reading["raw_anomaly"],
            reading["persistence_alert"],
            reading["bounds_breach"],
            reading["hybrid_alert"]
        ))
        conn.commit()
