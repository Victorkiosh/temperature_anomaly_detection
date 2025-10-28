"""
4_data_verification.py
-----------------------

Verifies that the simulated sensor data has been successfully inserted into
the SQLite database.

Performs:
    1. Record count checks for each table.
    2. Sampling a few entries from sensor_readings.
    3. Viewing the most recent system log messages.

This script is purely for validation and quality assurance.

Author: Victor Kioko
Date:9th October 2025
"""

import sqlite3
import pandas as pd

# Step 1: Define database path
db_path = "database/cold_storage.db"

# Step 2: Connect to the database
conn = sqlite3.connect(db_path)

try:
    print("\n🔍 Running data verification checks...\n")

    # Step 3: Check record count in each table
    tables = ["rooms", "sensor_readings", "anomaly_predictions", "system_logs"]
    for table in tables:
        count = pd.read_sql_query(f"SELECT COUNT(*) AS total FROM {table}", conn)["total"][0]
        print(f"📊 {table}: {count:,} records")

    # Step 4: Preview a few rows from sensor_readings
    print("\n🧾 Sample data from sensor_readings:")
    sample_data = pd.read_sql_query("""
        SELECT * FROM sensor_readings
        ORDER BY timestamp DESC
        LIMIT 5;
    """, conn)
    print(sample_data)

    # Step 5: Display recent system logs
    print("\n🪵 Recent system logs:")
    logs = pd.read_sql_query("""
        SELECT log_timestamp, log_level, message, source
        FROM system_logs
        ORDER BY log_timestamp DESC
        LIMIT 5;
    """, conn)
    print(logs)

except Exception as e:
    print(f"❌ Verification failed: {e}")

finally:
    conn.close()
    print("\n✅ Verification complete. Database connection closed.")
