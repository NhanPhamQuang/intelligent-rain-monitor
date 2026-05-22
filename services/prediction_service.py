from datetime import datetime
import streamlit as st
from pymongo.errors import PyMongoError

from services.weather_service import get_db
from models.loader import get_model
from config import WEATHER_FEATURES


def predict(features: dict) -> dict:
    """Run the LightGBM model. Falls back to a humidity/rainfall heuristic if model unavailable."""
    model = get_model()
    if model is None:
        humidity = features.get("Humidity3pm", 50)
        rainfall = features.get("Rainfall", 0)
        prob = min(0.95, (humidity / 100) * 0.6 + (min(rainfall, 20) / 20) * 0.4)
        return {"probability": float(prob), "model": "heuristic"}

    feature_vector = [[features.get(f, 0.0) for f in WEATHER_FEATURES]]
    try:
        prob = float(model.predict_proba(feature_vector)[0][1])
    except Exception:
        try:
            prob = float(model.predict(feature_vector)[0])
        except Exception:
            prob = 0.5
    return {"probability": prob, "model": "lightgbm"}


def save_prediction(location: str, features: dict, probability: float, threshold: float):
    """Persist prediction to MongoDB. Returns str id or None."""
    db = get_db()
    if db is None:
        return None
    try:
        doc = {
            "timestamp": datetime.utcnow(),
            "location": location,
            "input_features": {k: float(v) for k, v in features.items()},
            "probability": float(probability),
            "prediction": bool(probability > threshold),
            "threshold": float(threshold),
            "actual_outcome": None,
        }
        result = db["predictions"].insert_one(doc)
        return str(result.inserted_id)
    except PyMongoError:
        return None


def save_feedback(prediction_id: str, actual_outcome: str) -> bool:
    db = get_db()
    if db is None:
        return False
    try:
        from bson import ObjectId
        db["predictions"].update_one(
            {"_id": ObjectId(prediction_id)},
            {"$set": {"actual_outcome": actual_outcome}},
        )
        return True
    except PyMongoError:
        return False


@st.cache_data(ttl=60)
def get_recent_predictions(limit: int = 20) -> list:
    db = get_db()
    if db is None:
        return []
    docs = (
        db["predictions"]
        .find(
            {},
            {"_id": 1, "timestamp": 1, "location": 1, "probability": 1, "prediction": 1, "actual_outcome": 1},
        )
        .sort("timestamp", -1)
        .limit(limit)
    )
    records = []
    for doc in docs:
        doc["_id"] = str(doc["_id"])
        records.append(doc)
    return records
