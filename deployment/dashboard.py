"""
deployment/dashboard.py
-----------------------
Streamlit dashboard for live monitoring of temperature anomalies.

Run:
    streamlit run deployment/dashboard.py

This app:
    - Connects to the same SQLite database used by the simulator.
    - Automatically refreshes every few seconds to show the latest data.
    - Displays KPIs (current temp, alert count, averages).
    - Visualizes real-time temperature trends using Plotly.
"""

import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
from streamlit_autorefresh import st_autorefresh
from datetime import datetime

# === CONFIG ===
DB_PATH = "deployment/temperature_data.db"
REFRESH_INTERVAL_MS = 5000  # Auto-refresh every 5 seconds
MAX_RECORDS = 200  # How many recent records to display


# === FUNCTIONS ===
def load_data(n_latest=MAX_RECORDS):
    """Fetch the most recent readings from the SQLite database."""
    try:
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query(
            f"SELECT * FROM readings ORDER BY id DESC LIMIT {n_latest}", conn
        )
        conn.close()
        if not df.empty:
            df = df[::-1]  # chronological order
        return df
    except Exception as e:
        st.error(f"Database error: {e}")
        return pd.DataFrame()


def compute_metrics(df):
    """Compute key indicators for quick insights."""
    latest_temp = df["temperature"].iloc[-1]
    alert_status = df["hybrid_alert"].iloc[-1]
    avg_temp = df["temperature"].tail(10).mean()
    recent_alerts = df["hybrid_alert"].tail(20).sum()
    return latest_temp, alert_status, avg_temp, recent_alerts


def plot_temperature(df):
    """Create an interactive temperature trend chart with color-coded alerts."""
    fig = px.scatter(
        df,
        x="timestamp",
        y="temperature",
        color=df["hybrid_alert"].map({0: "Normal", 1: "Alert"}),
        color_discrete_map={"Normal": "green", "Alert": "red"},
        title="Temperature Trend Over Time",
    )
    fig.add_traces(
        px.line(df, x="timestamp", y="temperature").data
    )  # keep line continuity

    fig.add_hrect(y0=-25, y1=-15, fillcolor="green", opacity=0.15, line_width=0)
    fig.update_layout(
        xaxis_title="Timestamp",
        yaxis_title="Temperature (°C)",
        title_x=0.3,
        template="plotly_white",
        legend_title_text="Status",
    )
    return fig



# === STREAMLIT UI ===
st.set_page_config(
    page_title="Cold Storage Dashboard",
    page_icon="🌡️",
    layout="wide",
)

# Auto-refresh
st_autorefresh(interval=REFRESH_INTERVAL_MS, key="refresh_data")

st.title("🌡️ Cold Storage Temperature Monitoring Dashboard")

# Load data
df = load_data()

if df.empty:
    st.warning("No data available yet. Start the simulation to see live updates.")
else:
    # Compute KPIs
    latest_temp, alert_status, avg_temp, alert_count = compute_metrics(df)

    # KPI section
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Current Temperature", f"{latest_temp:.2f} °C")
    col2.metric("Status", "⚠️ ALERT" if alert_status else "✅ Normal")
    col3.metric("Avg (Last 10)", f"{avg_temp:.2f} °C")
    col4.metric("Alerts (Last 20)", int(alert_count))

    st.markdown("---")

    # Temperature chart
    st.subheader("📈 Live Temperature Trend")
    fig = plot_temperature(df)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # Recent readings table
    st.subheader("🕒 Recent Readings")
    st.dataframe(
        df[["timestamp", "temperature", "hybrid_alert"]].tail(10).reset_index(drop=True),
        use_container_width=True,
    )

    # Timestamp footer
    st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

