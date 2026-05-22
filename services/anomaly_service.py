import numpy as np
import pandas as pd
from datetime import datetime
import streamlit as st

from services.weather_service import get_db, get_multi_location_risk
from utils.helpers import get_risk_level

_SEVERITY_MAP = {"critical": "error", "warning": "warning", "info": "info"}


def detect_anomalies(df: pd.DataFrame, column: str = "Pressure3pm", threshold: float = 2.5) -> pd.DataFrame:
    """Z-score anomaly detection. Adds is_anomaly bool column."""
    if df.empty or column not in df.columns:
        return df
    series = df[column].dropna()
    if len(series) < 3:
        return df
    z = (series - series.mean()) / series.std()
    df = df.copy()
    df["is_anomaly"] = False
    df.loc[z[z.abs() > threshold].index, "is_anomaly"] = True
    return df


@st.cache_data(ttl=300)
def get_alerts(location: str = None) -> list:
    db = get_db()
    if db is None:
        return _mock_alerts()

    query = {"is_active": True}
    if location:
        query["region"] = location
    alerts = list(db["alerts"].find(query, {"_id": 0}))
    return alerts if alerts else _mock_alerts()


def upsert_alert(region: str, severity: str, message: str):
    db = get_db()
    if db is None:
        return
    db["alerts"].update_one(
        {"region": region, "is_active": True},
        {"$set": {"region": region, "severity": severity, "message": message,
                  "timestamp": datetime.utcnow(), "is_active": True}},
        upsert=True,
    )


@st.cache_data(ttl=600)
def get_regional_risk_data() -> list:
    raw = get_multi_location_risk()
    return [
        {
            "location": item["location"],
            "rain_prob": item["rain_prob"],
            "risk_level": get_risk_level(item["rain_prob"]),
        }
        for item in raw
    ]


def _mock_alerts() -> list:
    return [
        {"region": "NSW", "severity": "critical",
         "message": "Heavy rain and potential flash flooding expected in NSW (next 24 h)."},
        {"region": "Queensland", "severity": "warning",
         "message": "High UV index in Queensland. Heat exhaustion risk."},
        {"region": "Melbourne", "severity": "info",
         "message": "Sensor maintenance scheduled for Melbourne Station at 02:00 AM."},
    ]
