"""
1_data_simulation.py
--------------------
This script generates synthetic temperature and humidity readings 
for a cold storage facility. The data simulates 8 rooms across 
different temperature zones (frozen, chilled, ambient) with 
measurements recorded every 15 minutes for one week.

Output:
    - A CSV file named 'simulated_sensor_data.csv' containing:
        timestamp, room_name, temperature, humidity
"""

import pandas as pd
import numpy as np
from datetime import datetime

# Step 1: Define rooms with realistic temperature ranges (°C)
# Each room simulates an independent cold storage zone
rooms = {
    "Frozen_Storage_A": (-25, -18),
    "Frozen_Storage_B": (-25, -18),
    "Chilled_Storage_A": (0, 5),
    "Chilled_Storage_B": (0, 5),
    "Dispatch_Bay": (5, 10),
    "Receiving_Zone": (5, 10),
    "Packaging_Section": (15, 25),
    "Maintenance_Room": (15, 25)
}

# Step 2: Generate timestamps at 15-minute intervals for 7 full days
# Frequency '15min' = every 15 minutes
start_time = datetime(2025, 10, 1, 0, 0, 0)
end_time = datetime(2025, 10, 7, 23, 45, 0)
timestamps = pd.date_range(start=start_time, end=end_time, freq="15min")

# Step 3: Simulate readings for each room and timestamp
# Temperature and humidity values are drawn from random distributions
data = []
for ts in timestamps:
    for room, (low, high) in rooms.items():
        temp = np.random.normal((low + high) / 2, 1.5)  # Gaussian noise for realism
        humidity = np.random.uniform(40, 80)            # Uniform range for humidity
        data.append([ts, room, round(temp, 2), round(humidity, 2)])

# Step 4: Create DataFrame
df = pd.DataFrame(data, columns=["timestamp", "room_name", "temperature", "humidity"])

# Step 5: Export simulated data to CSV
output_path = output_path = "data/simulated_sensor_data.csv"

df.to_csv(output_path, index=False)

# Step 6: Display summary info
print(f"✅ Data simulation complete.")
print(f"✅ Records generated: {len(df):,}")
print(f"✅ Unique timestamps: {df['timestamp'].nunique():,}")
print(f"✅ Unique rooms: {df['room_name'].nunique()}")
print(f"💾 Data saved to: {output_path}")
