"""
3_data_insertion.py
-------------------

Loads the simulated temperature and humidity readings
from the CSV file into the SQLite database.

Tables affected:
    - sensor_readings  (data inserted)
    - system_logs      (logs insert status)

Assumptions:
    - Database setup script has already been run.
    - The CSV file exists at: data/simulated_sensor_data.csv

Author: Victor Kioko
Date: 9th October 2025
"""

import sqlite3
import pandas as pd
from datetime import datetime

# Step 1: Define paths
db_path = "database/cold_storage.db"
csv_path = "data/simulated_sensor_data.csv"

# Step 2: Connect to database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    # Step 3: Read simulated data
    df = pd.read_csv(csv_path)

    # Step 4: Insert data into sensor_readings table
    df.to_sql("sensor_readings", conn, if_exists="append", index=False)

    # Step 5: Log success in system_logs
    cursor.execute("""
        INSERT INTO system_logs (log_level, message, source)
        VALUES (?, ?, ?)
    """, (
        "INFO",
        f"Inserted {len(df):,} sensor readings from CSV successfully.",
        "data_insertion"
    ))

    conn.commit()
    print(f"✅ Data insertion successful — {len(df):,} records added to sensor_readings.")

except Exception as e:
    # Step 6: Log errors if any
    error_message = f"❌ Data insertion failed: {str(e)}"
    print(error_message)
    cursor.execute("""
        INSERT INTO system_logs (log_level, message, source)
        VALUES (?, ?, ?)
    """, (
        "ERROR",
        error_message,
        "data_insertion"
    ))
    conn.commit()

finally:
    # Step 7: Close database connection
    conn.close()
    print("🔒 Database connection closed.")
