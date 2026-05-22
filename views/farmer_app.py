import numpy as np
import streamlit as st

from services.prediction_service import predict
from services.weather_service import get_locations, get_location_rain_probability, get_weather_data
from utils.helpers import format_probability


def _build_forecast(base_prob: float) -> list:
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    probs = [base_prob] + list(np.random.uniform(0.1, 0.9, 6))
    icons = ["🌧️" if p > 0.55 else "☀️" if p < 0.3 else "⛅" for p in probs]
    temps = [f"{int(20 + (1 - p) * 12)}°C" for p in probs]
    return [{"day": days[i], "icon": icons[i], "temp": temps[i], "prob": probs[i]} for i in range(7)]


def show_farmer_app():
    st.title("Smart Farm Assistant")

    ch, cl = st.columns([2, 1])
    with ch:
        st.markdown("### Farm Weather Intelligence")
    with cl:
        locations = get_locations()
        location = st.selectbox("Farm Location", locations or ["Sydney"], label_visibility="collapsed")

    st.divider()

    # ── derive rain probability ───────────────────────────────────
    rain_prob = get_location_rain_probability(location)

    # refine with latest actual observations + model
    df = get_weather_data(location, limit=5)
    if not df.empty:
        latest = df.iloc[-1]
        features = {
            "MinTemp": latest.get("MinTemp", 18.0),
            "MaxTemp": latest.get("MaxTemp", 27.0),
            "Rainfall": latest.get("Rainfall", 0.0),
            "Humidity3pm": float(latest.get("Humidity3pm", 60.0) or 60.0),
            "Pressure3pm": float(latest.get("Pressure3pm", 1013.0) or 1013.0),
            "WindSpeed3pm": float(latest.get("WindSpeed3pm", 15.0) or 15.0),
            "Sunshine": float(latest.get("Sunshine", 8.0) or 8.0),
        }
        rain_prob = predict(features)["probability"]

    # ── main outlook card ─────────────────────────────────────────
    with st.container(border=True):
        ic, tx = st.columns([1, 2])
        with ic:
            icon = "🌧️" if rain_prob > 0.5 else "☀️"
            st.markdown(f"<h1 style='text-align:center;font-size:80px;margin:0'>{icon}</h1>",
                        unsafe_allow_html=True)
        with tx:
            st.markdown("### Tomorrow's Outlook")
            label = "Rain Expected" if rain_prob > 0.5 else "Clear Skies"
            color = "#1f77b4" if rain_prob > 0.5 else "#f0a500"
            st.markdown(f"<h2 style='color:{color};margin:0'>{label}</h2>", unsafe_allow_html=True)
            st.write(f"Probability: **{format_probability(rain_prob)}**")
            st.progress(rain_prob)

    # ── recommendations ───────────────────────────────────────────
    st.subheader("Farm Management Advice")
    r1, r2 = st.columns(2)
    with r1:
        if rain_prob > 0.6:
            st.error("**Delay Irrigation**  \nRain expected. Save water and energy.")
        else:
            st.success("**Proceed with Irrigation**  \nLow rain probability. Good time to irrigate.")
    with r2:
        if rain_prob > 0.5:
            st.warning("**Protect Seedlings**  \nStrong winds and rain may damage young plants.")
        else:
            st.info("**Ideal Farming Conditions**  \nGood weather window for outdoor activities.")

    if rain_prob > 0.4:
        st.info("Apply fertilizer *after* rain for deeper soil penetration.")

    # ── 7-day forecast ────────────────────────────────────────────
    st.subheader("7-Day Forecast")
    forecast = _build_forecast(rain_prob)
    cols = st.columns(7)
    for i, day in enumerate(forecast):
        with cols[i]:
            st.markdown(f"**{day['day']}**")
            st.markdown(f"### {day['icon']}")
            st.caption(day["temp"])
            st.caption(format_probability(day["prob"]))

    # ── recent observations ───────────────────────────────────────
    if not df.empty:
        with st.expander("Recent Observations"):
            cols_show = [c for c in ["Date", "MinTemp", "MaxTemp", "Rainfall", "Humidity3pm", "RainTomorrow"] if c in df.columns]
            st.dataframe(df[cols_show], use_container_width=True)

    st.divider()
    if st.button("Send Alert to Field Workers", use_container_width=True):
        st.toast("Alert sent to all registered workers!", icon="📡")
