"""
data_setup.py

Initializes the database for the Temperature Monitoring & Anomaly Detection System.

Creates the following tables:
    1. rooms               - metadata for each monitored room (name, type, safe ranges, etc.)
    2. sensor_readings     - logs temperature & humidity readings at 15-min intervals.
    3. anomaly_predictions - stores detected anomalies (temperature or humidity breaches).
    4. system_logs         - captures system-level events, warnings, or errors.

Author: Victor Kioko
Date:9th October 2025
"""

import sqlite3
import os

# Step 1: Ensure the database directory exists
os.makedirs("database", exist_ok=True)

# Step 2: Define database path
db_path = "database/cold_storage.db"

# Step 3: Connect to the SQLite database (auto-creates file if not existing)
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Step 4: Create 'rooms' table — must match rooms in data_simulation.py
cursor.execute("""
CREATE TABLE IF NOT EXISTS rooms (
    room_id INTEGER PRIMARY KEY AUTOINCREMENT,
    room_name TEXT UNIQUE NOT NULL,
    room_type TEXT,              -- e.g., 'Frozen', 'Chilled', 'Ambient'
    min_temp REAL,               -- lower safe temperature bound
    max_temp REAL,               -- upper safe temperature bound
    min_humidity REAL,           -- lower safe humidity bound
    max_humidity REAL            -- upper safe humidity bound
);
""")

# Step 5: Create 'sensor_readings' table
cursor.execute("""
CREATE TABLE IF NOT EXISTS sensor_readings (
    reading_id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME NOT NULL,
    room_name TEXT NOT NULL,
    temperature REAL,
    humidity REAL,
    FOREIGN KEY (room_name) REFERENCES rooms (room_name)
);
""")

# Step 6: Create 'anomaly_predictions' table
cursor.execute("""
CREATE TABLE IF NOT EXISTS anomaly_predictions (
    anomaly_id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME NOT NULL,
    room_name TEXT NOT NULL,
    temperature REAL,
    humidity REAL,
    anomaly_type TEXT,  -- e.g., 'TEMP_HIGH', 'TEMP_LOW', 'HUMIDITY_HIGH'
    detected_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (room_name) REFERENCES rooms (room_name)
);
""")

# Step 7: Create 'system_logs' table
cursor.execute("""
CREATE TABLE IF NOT EXISTS system_logs (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    log_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    log_level TEXT,      -- e.g., 'INFO', 'WARNING', 'ERROR'
    message TEXT,
    source TEXT          -- e.g., 'data_insertion', 'anomaly_detection', 'api_handler'
);
""")

# Step 8: Populate 'rooms' table with consistent data
rooms_data = [
    ("Frozen_Storage_A", "Frozen", -25, -18, 40, 80),
    ("Frozen_Storage_B", "Frozen", -25, -18, 40, 80),
    ("Chilled_Storage_A", "Chilled", 0, 5, 40, 80),
    ("Chilled_Storage_B", "Chilled", 0, 5, 40, 80),
    ("Dispatch_Bay", "Chilled", 5, 10, 40, 80),
    ("Receiving_Zone", "Chilled", 5, 10, 40, 80),
    ("Packaging_Section", "Ambient", 15, 25, 40, 80),
    ("Maintenance_Room", "Ambient", 15, 25, 40, 80),
]

cursor.executemany("""
INSERT OR IGNORE INTO rooms (room_name, room_type, min_temp, max_temp, min_humidity, max_humidity)
VALUES (?, ?, ?, ?, ?, ?);
""", rooms_data)

# Step 9: Commit and close connection
conn.commit()
conn.close()

print("✅ Database setup complete! All tables and room metadata are ready.")
print(f"📁 Database location: {db_path}")
