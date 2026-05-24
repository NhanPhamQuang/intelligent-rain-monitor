# Intelligent Rain Monitor

An end-to-end Machine Learning system for rainfall prediction and weather monitoring, powered by **LightGBM**, **Streamlit**, and **MongoDB Atlas**.

---

## Features

- **Weather Dashboard** — Real-time temperature, rainfall, humidity, and wind direction charts pulled from MongoDB
- **Rain Prediction** — LightGBM model inference with feature importance (SHAP-style) and confidence scoring
- **Model Performance** — Confusion matrix, ROC curve, feature importance, and drift monitoring
- **Farmer App** — Location-aware farm advice, 7-day forecast, and field-worker alerts
- **Weather Monitoring** — Regional risk assessment, active alerts, and Z-score anomaly detection
- **Full-stack persistence** — All predictions + feedback stored in MongoDB; CSV fallback when offline

---

## Project Structure

```
intelligent-rain-monitor/
│
├── app.py                          # Entry point
├── config.py                       # MongoDB URI, model path, feature list
│
├── pages/
│   ├── dashboard.py                # Weather Dashboard page
│   ├── rain_prediction.py          # Rain Prediction page
│   ├── model_performance.py        # Model Performance page
│   ├── farmer_app.py               # Farmer App page
│   └── monitoring.py               # Weather Monitoring page
│
├── services/
│   ├── weather_service.py          # MongoDB queries & CSV seeding
│   ├── prediction_service.py       # Model inference + prediction history
│   └── anomaly_service.py          # Alerts & Z-score anomaly detection
│
├── models/
│   ├── lightgbm_rain_tomorrow_bundle.joblib   # Trained LightGBM model
│   └── loader.py                   # Model loading helper
│
├── components/
│   ├── charts.py                   # Reusable Plotly chart builders
│   └── metrics.py                  # Metric cards + CSS loader
│
├── utils/
│   └── helpers.py                  # Formatting and utility functions
│
├── assets/
│   └── styles.css                  # Global dark-theme CSS
│
├── weatherAUS.csv                  # Source dataset (seed MongoDB once)
├── requirements.txt
└── README.md
```

---

## MongoDB Schema

Database: `weather_monitor`

| Collection        | Purpose                                        |
|-------------------|------------------------------------------------|
| `weather_records` | Historical weather observations (from CSV)     |
| `predictions`     | Stored predictions + user feedback             |
| `model_metrics`   | Model performance snapshots                    |
| `alerts`          | Active regional weather alerts                 |

---

## Quick Start

### 1. Clone & create virtual environment

```bash
git clone https://github.com/your-username/intelligent-rain-monitor.git
cd intelligent-rain-monitor
python -m venv .venv
```

Activate:

```bash
# Windows
.venv\Scripts\activate

# Mac / Linux
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment (optional)

Create a `.env` file in the project root to override defaults:

```
MONGO_URI=mongodb+srv://<user>:<password>@<cluster>.mongodb.net/?appName=<App>
MONGO_DB=weather_monitor
```

If no `.env` is present, the default Atlas URI from `config.py` is used.

### 4. Run the app

```bash
streamlit run app.py
```

App opens at **http://localhost:8501**

### 5. Seed the database (first run)

On first launch, the sidebar will show a **"Seed Database from CSV"** button if `weather_records` is empty. Click it to load all 145 000+ records from `weatherAUS.csv` into MongoDB. This takes about 1–2 minutes and runs only once.

---

## Model Details

| Property     | Value                                                |
|--------------|------------------------------------------------------|
| Algorithm    | LightGBM (pre-trained bundle)                        |
| Task         | Binary classification — Rain Tomorrow (Yes / No)     |
| Features     | MinTemp, MaxTemp, Rainfall, Humidity3pm, Pressure3pm, WindSpeed3pm, Sunshine |
| Fallback     | Humidity + Rainfall heuristic if model file missing  |

---

## Tech Stack

| Layer       | Technology                              |
|-------------|-----------------------------------------|
| UI          | Streamlit 1.56                          |
| ML Model    | LightGBM (joblib bundle)                |
| Database    | MongoDB Atlas (pymongo 4.x)             |
| Charts      | Plotly                                  |
| Data        | Pandas, NumPy, Scikit-learn             |
| Config      | python-dotenv                           |

---

## Author

Built by Lê Phước Gia Lộc and Phạm Quang Nhân — practical full-stack ML system, not just a notebook.
