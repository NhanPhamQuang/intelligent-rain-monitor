import os
import joblib
import streamlit as st
from config import MODEL_PATH, WEATHER_FEATURES


@st.cache_resource(show_spinner=False)
def get_model():
    """Load the LightGBM bundle. Falls back to root-level file if models/ copy is missing."""
    candidates = [
        MODEL_PATH,
        os.path.join(os.path.dirname(os.path.dirname(__file__)), "lightgbm_rain_tomorrow_bundle.joblib"),
    ]
    for path in candidates:
        if os.path.exists(path):
            bundle = joblib.load(path)
            if isinstance(bundle, dict):
                return bundle.get("model") or bundle.get("pipeline")
            if isinstance(bundle, (list, tuple)):
                return bundle[0]
            return bundle
    return None


def get_feature_importance() -> dict:
    model = get_model()
    if model is None:
        return {}
    try:
        importances = model.feature_importances_
        return dict(zip(WEATHER_FEATURES, importances.tolist()))
    except Exception:
        return {}
