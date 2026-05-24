from datetime import datetime
import streamlit as st

from components.charts import (
    confusion_matrix_chart,
    drift_chart,
    feature_importance_chart,
    roc_curve_chart,
)
from components.metrics import show_model_metrics
from models.loader import get_feature_importance
from services.weather_service import get_db


_DEFAULT_METRICS = {
    "model_name": "LightGBM",
    "accuracy": 0.842, "precision": 0.795, "recall": 0.810, "f1": 0.802, "auc": 0.891,
    "confusion_matrix": [[1200, 150], [180, 980]],
    "feature_importance": {
        "Humidity3pm": 0.35, "Rainfall": 0.25, "Pressure3pm": 0.15,
        "Sunshine": 0.12, "WindSpeed3pm": 0.08, "MaxTemp": 0.03, "MinTemp": 0.02,
    },
    "last_trained": datetime(2026, 3, 15),
    "dataset_size": 145460,
}


def _ensure_metrics():
    db = get_db()
    if db is None:
        return
    if db["model_metrics"].count_documents({}) == 0:
        record = dict(_DEFAULT_METRICS)
        record["last_trained"] = datetime.utcnow()
        db["model_metrics"].insert_one(record)


def _load_all_metrics() -> dict:
    """Return {model_name: doc} for every entry in the collection."""
    db = get_db()
    result = {}
    if db is not None:
        for doc in db["model_metrics"].find():
            doc.pop("_id", None)
            result[doc.get("model_name", "Unknown")] = doc
    if not result:
        result[_DEFAULT_METRICS["model_name"]] = dict(_DEFAULT_METRICS)
    return result


def show_model_performance():
    st.title("Model Performance Dashboard")
    _ensure_metrics()

    all_metrics = _load_all_metrics()
    model_names = list(all_metrics.keys())

    # ── header ───────────────────────────────────────────────────
    hc1, hc2 = st.columns([2, 1])
    with hc1:
        selected = st.selectbox("Model", model_names)
    m = all_metrics[selected]

    last_trained = m.get("last_trained")
    trained_str = last_trained.strftime("%Y-%m-%d") if isinstance(last_trained, datetime) else "N/A"
    with hc2:
        st.info(f"**Status:** Production  \n**Last Trained:** {trained_str}  \n**Dataset:** {m.get('dataset_size', 0):,} rows")

    # ── core metrics ─────────────────────────────────────────────
    st.subheader("Core Metrics")
    show_model_metrics(m["accuracy"], m["precision"], m["recall"], m["f1"], m.get("auc"))

    st.divider()

    # ── confusion matrix + ROC ───────────────────────────────────
    cl, cr = st.columns(2)
    with cl:
        st.subheader("Confusion Matrix")
        st.plotly_chart(confusion_matrix_chart(m["confusion_matrix"]), use_container_width=True)
    with cr:
        st.subheader("ROC Curve")
        st.plotly_chart(roc_curve_chart(m.get("auc", 0.89)), use_container_width=True)

    st.divider()

    # ── feature importance + drift ───────────────────────────────
    tab_fi, tab_drift = st.tabs(["Feature Importance", "Drift Monitoring"])

    with tab_fi:
        importance = get_feature_importance() or m.get("feature_importance", {})
        st.plotly_chart(feature_importance_chart(importance), use_container_width=True)

    with tab_drift:
        st.write("Population Stability Index (PSI) over the last 30 days.")
        st.plotly_chart(drift_chart(), use_container_width=True)
        st.caption("Values above 0.20 trigger automatic model retraining.")
