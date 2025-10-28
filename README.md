# 🧊 Cold Storage Temperature Anomaly Detection System

This project demonstrates a **complete end-to-end Machine Learning deployment pipeline** for real-time temperature anomaly detection in a cold storage environment.  
It combines **deep learning (LSTM)**, **statistical monitoring**, **operational rules**, and **real-time visualization** to simulate an intelligent cold storage monitoring system.

---

## 🚀 Project Overview

### 🎯 Objective
To detect abnormal temperature patterns in cold storage facilities and alert operators before a safety threshold is breached — ensuring **operational efficiency**, **food safety**, and **energy savings**.

### 🧩 System Components

| Module | Description |
|--------|--------------|
| **1. Data Simulation & Preprocessing** | Simulated realistic cold storage temperature data and structured it into a database. |
| **2. LSTM Model Training** | Built an LSTM Autoencoder to learn normal temperature behavior and detect deviations. |
| **3. Hybrid Detection Rule** | Combined AI-based anomaly prediction with operational threshold rules for robust alerts. |
| **4. FastAPI Backend** | Exposed the trained model as a real-time REST API (`/predict`) for live inference. |
| **5. SQLite Database** | Logged all readings and anomaly predictions for audit and visualization. |
| **6. Stream Simulation** | Emulated a live data feed from IoT sensors using Python’s request loop. |
| **7. Streamlit Dashboard** | Provided a real-time dashboard to visualize temperature fluctuations and alerts. |
| **8. Docker Containerization** | (Optional) Bundled the app for portable and consistent deployment. |

---

## 🧠 Model Architecture

The system uses an **LSTM Autoencoder** trained on historical temperature data to reconstruct normal behavior.  
A high reconstruction error indicates an **anomaly**, which is further validated through a **hybrid operational rule**.

Normal → Model reconstructs well → Low error
Anomaly → Model fails to reconstruct → High error → Alert triggered


---

## 🧩 Hybrid Rule Logic

| Rule | Description |
|------|--------------|
| **LSTM anomaly** | Model detects unusual pattern based on reconstruction error. |
| **Persistence** | Confirms if anomaly persists for `N` consecutive readings. |
| **Bounds breach** | Checks if temperature is outside allowed range (e.g., -25°C to -18°C). |
| **Hybrid alert** | Triggers alert if either persistence or bounds rule is True. |

---

## 🗂️ Folder Structure

