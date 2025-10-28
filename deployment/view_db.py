"""
view_db.py
-----------
Utility script to view stored temperature readings from the local SQLite database.

Usage:
    python deployment/view_db.py

It fetches all rows from the 'readings' table and prints them in a formatted table.
"""

import sqlite3
import pandas as pd
from tabulate import tabulate

# === Database path ===
DB_PATH = "deployment/temperature_data.db"


def view_latest_readings(limit=20):
    """Fetch and display the most recent readings."""
    try:
        conn = sqlite3.connect(DB_PATH)

        query = f"""
        SELECT id, timestamp, temperature, hybrid_alert
        FROM readings
        ORDER BY id DESC
        LIMIT {limit}
        """

        df = pd.read_sql(query, conn)
        conn.close()

        if df.empty:
            print("⚠️ No data found. Run simulate_stream.py first.")
        else:
            print(f"\n📊 Showing the latest {len(df)} readings from the database:\n")
            print(tabulate(df, headers="keys", tablefmt="fancy_grid", showindex=False))
    except Exception as e:
        print(f"❌ Error reading database: {e}")


if __name__ == "__main__":
    view_latest_readings()
