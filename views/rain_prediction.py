import numpy as np
import pandas as pd
import streamlit as st

from components.charts import feature_importance_chart
from models.loader import get_feature_importance
from services.prediction_service import (
    get_recent_predictions,
    predict,
    save_feedback,
    save_prediction,
)
from services.weather_service import get_locations
from utils.helpers import format_probability, get_confidence_level


def show_prediction():
    st.title("Rain Prediction System")
    st.markdown("Enter meteorological parameters to estimate the probability of rain tomorrow.")

    # ── input form ────────────────────────────────────────────────
    with st.form("prediction_form", border=True):
        st.subheader("Input Parameters")
        c1, c2, c3 = st.columns(3)
        with c1:
            locations = get_locations()
            location = st.selectbox("Location", locations or ["Sydney", "Melbourne", "Brisbane"])
            min_temp = st.number_input("Min Temp (°C)", value=18.5)
            max_temp = st.number_input("Max Temp (°C)", value=27.3)
        with c2:
            rainfall = st.number_input("Rainfall (mm)", value=0.0, min_value=0.0)
            humidity = st.slider("Humidity 3pm (%)", 0, 100, 65)
            sunshine = st.slider("Sunshine (hr)", 0.0, 16.0, 8.5)
        with c3:
            pressure = st.number_input("Pressure 3pm (hPa)", value=1012.0)
            wind = st.number_input("Wind Speed 3pm (km/h)", value=20.0, min_value=0.0)
            evap = st.number_input("Evaporation (mm)", value=5.0, min_value=0.0)

        with st.expander("Advanced Settings"):
            threshold = st.select_slider(
                "Decision Threshold",
                options=[round(x, 1) for x in np.arange(0.1, 1.0, 0.1)],
                value=0.5,
            )
            st.caption("Lower threshold = more sensitive to rain detection.")

        submitted = st.form_submit_button("Run Prediction", use_container_width=True, type="primary")

    if not submitted:
        return

    # ── run model ────────────────────────────────────────────────
    features = {
        "MinTemp": min_temp, "MaxTemp": max_temp, "Rainfall": rainfall,
        "Humidity3pm": float(humidity), "Pressure3pm": pressure,
        "WindSpeed3pm": wind, "Sunshine": float(sunshine),
    }

    with st.spinner("Analyzing atmospheric patterns..."):
        result = predict(features)

    prob = result["probability"]
    is_rain = prob > threshold
    pred_id = save_prediction(location, features, prob, threshold)

    st.divider()

    # ── result tabs ───────────────────────────────────────────────
    tab1, tab2, tab3 = st.tabs(["Prediction Result", "Model Explainability", "Prediction History"])

    with tab1:
        cA, cB, cC = st.columns(3)
        cA.metric("Rain Tomorrow", "YES" if is_rain else "NO",
                  delta="Likely" if is_rain else "Unlikely",
                  delta_color="inverse" if is_rain else "normal")
        cB.metric("Probability", format_probability(prob))
        cC.metric("Confidence", get_confidence_level(prob))

        if is_rain:
            st.error(f"Rain probability: {format_probability(prob)}. Consider rescheduling outdoor activities.")
        else:
            st.success(f"Rain probability: {format_probability(prob)}. Conditions look clear!")

        st.progress(prob, text=f"Probability scale: {format_probability(prob)}")
        st.caption(f"Model used: **{result['model'].upper()}**")

    with tab2:
        importance = get_feature_importance() or {
            "Humidity3pm": 0.45, "Pressure3pm": -0.32,
            "Sunshine": -0.25, "WindSpeed3pm": 0.15, "Rainfall": 0.10,
        }
        st.plotly_chart(feature_importance_chart(importance), use_container_width=True)
        st.info("Higher humidity and recent rainfall push the model toward YES; "
                "high pressure and sunshine push toward NO.")

    with tab3:
        preds = get_recent_predictions()
        if preds:
            pdf = pd.DataFrame(preds)
            pdf["timestamp"] = pd.to_datetime(pdf["timestamp"]).dt.strftime("%Y-%m-%d %H:%M")
            pdf["probability"] = pdf["probability"].map(lambda x: f"{x * 100:.1f}%")
            st.dataframe(
                pdf[["timestamp", "location", "probability", "prediction", "actual_outcome"]],
                use_container_width=True,
            )
        else:
            st.info("No prediction history yet.")

    # ── feedback ─────────────────────────────────────────────────
    st.divider()
    st.subheader("Ground Truth Feedback")
    f1, f2 = st.columns([2, 1])
    with f1:
        actual = st.radio("Actual outcome?", ["Rain", "No Rain"], horizontal=True)
    with f2:
        if st.button("Submit Feedback", use_container_width=True):
            if pred_id:
                save_feedback(pred_id, actual)
            st.toast("Feedback saved for retraining.", icon="✅")
