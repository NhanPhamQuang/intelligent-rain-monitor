import os
import pandas as pd
import streamlit as st
from pymongo import MongoClient, ASCENDING, DESCENDING
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError

from config import MONGO_URI, MONGO_DB, CSV_DATA_PATH


@st.cache_resource(show_spinner="Connecting to database...")
def _get_client():
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        client.admin.command("ping")
        return client
    except (ConnectionFailure, ServerSelectionTimeoutError):
        return None


def get_db():
    client = _get_client()
    return client[MONGO_DB] if client is not None else None


def is_connected() -> bool:
    return get_db() is not None


def is_data_seeded() -> bool:
    db = get_db()
    if db is None:
        return False
    return db["weather_records"].count_documents({}) > 0


def seed_from_csv(progress_callback=None) -> tuple:
    """Seed weather_records from CSV. Returns (success: bool, message: str)."""
    db = get_db()
    if db is None:
        return False, "MongoDB connection failed."
    if not os.path.exists(CSV_DATA_PATH):
        return False, f"CSV not found: {CSV_DATA_PATH}"

    try:
        df = pd.read_csv(CSV_DATA_PATH)
        df["Date"] = pd.to_datetime(df["Date"]).dt.strftime("%Y-%m-%d")
        records = df.where(pd.notnull(df), None).to_dict(orient="records")

        collection = db["weather_records"]
        collection.drop()

        batch_size = 2000
        total = len(records)
        for i in range(0, total, batch_size):
            collection.insert_many(records[i : i + batch_size])
            if progress_callback:
                progress_callback(
                    min((i + batch_size) / total, 1.0),
                    f"Seeding... {min(i + batch_size, total)}/{total} records",
                )

        collection.create_index([("Location", ASCENDING), ("Date", DESCENDING)])
        collection.create_index([("Date", DESCENDING)])
        return True, f"Seeded {total} records successfully."
    except Exception as exc:
        return False, f"Seeding failed: {exc}"


def _csv_fallback(location: str, limit: int) -> pd.DataFrame:
    if not os.path.exists(CSV_DATA_PATH):
        return pd.DataFrame()
    df = pd.read_csv(CSV_DATA_PATH)
    df["Date"] = pd.to_datetime(df["Date"])
    return df[df["Location"] == location].sort_values("Date").tail(limit)


@st.cache_data(ttl=300)
def get_locations() -> list:
    db = get_db()
    if db is None:
        if os.path.exists(CSV_DATA_PATH):
            df = pd.read_csv(CSV_DATA_PATH, usecols=["Location"])
            return sorted(df["Location"].dropna().unique().tolist())
        return []
    return sorted(db["weather_records"].distinct("Location"))


@st.cache_data(ttl=300)
def get_weather_data(location: str, start_date=None, end_date=None, limit: int = 200) -> pd.DataFrame:
    db = get_db()
    if db is None:
        return _csv_fallback(location, limit)

    query = {"Location": location}
    if start_date and end_date:
        query["Date"] = {"$gte": str(start_date), "$lte": str(end_date)}

    records = list(
        db["weather_records"]
        .find(query, {"_id": 0})
        .sort("Date", DESCENDING)
        .limit(limit)
    )
    if not records:
        return pd.DataFrame()

    df = pd.DataFrame(records)
    df["Date"] = pd.to_datetime(df["Date"])
    return df.sort_values("Date")


@st.cache_data(ttl=600)
def get_location_rain_probability(location: str) -> float:
    db = get_db()
    if db is None:
        if os.path.exists(CSV_DATA_PATH):
            df = pd.read_csv(CSV_DATA_PATH, usecols=["Location", "RainTomorrow"])
            loc = df[df["Location"] == location]["RainTomorrow"].dropna()
            return float((loc == "Yes").mean()) if len(loc) > 0 else 0.0
        return 0.0

    pipeline = [
        {"$match": {"Location": location, "RainTomorrow": {"$in": ["Yes", "No"]}}},
        {"$group": {"_id": "$RainTomorrow", "count": {"$sum": 1}}},
    ]
    counts = {r["_id"]: r["count"] for r in db["weather_records"].aggregate(pipeline)}
    total = sum(counts.values())
    return counts.get("Yes", 0) / total if total > 0 else 0.0


@st.cache_data(ttl=300)
def get_wind_direction_data(location: str) -> pd.DataFrame:
    db = get_db()
    if db is None:
        return pd.DataFrame()

    pipeline = [
        {"$match": {"Location": location, "WindDir3pm": {"$ne": None}}},
        {"$group": {"_id": "$WindDir3pm", "count": {"$sum": 1}}},
    ]
    freq = {r["_id"]: r["count"] for r in db["weather_records"].aggregate(pipeline)}
    direction_order = [
        "N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
        "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW",
    ]
    return pd.DataFrame([{"Direction": d, "Frequency": freq.get(d, 0)} for d in direction_order])


@st.cache_data(ttl=600)
def get_multi_location_risk() -> list:
    db = get_db()
    if db is None:
        return []

    pipeline = [
        {"$match": {"RainTomorrow": {"$in": ["Yes", "No"]}}},
        {
            "$group": {
                "_id": "$Location",
                "rain_yes": {"$sum": {"$cond": [{"$eq": ["$RainTomorrow", "Yes"]}, 1, 0]}},
                "total": {"$sum": 1},
            }
        },
        {"$project": {"location": "$_id", "rain_prob": {"$divide": ["$rain_yes", "$total"]}, "_id": 0}},
        {"$sort": {"rain_prob": -1}},
        {"$limit": 8},
    ]
    return list(db["weather_records"].aggregate(pipeline))
