import pandas as pd
import streamlit as st

from components.charts import (
    temperature_trend_chart,
    rainfall_bar_chart,
    humidity_scatter_chart,
    wind_rose_chart,
)
from services.weather_service import (
    get_locations,
    get_weather_data,
    get_wind_direction_data,
)


def show_dashboard():
    st.title("Weather Data Dashboard")

    # ── filters ──────────────────────────────────────────────────
    c1, c2, c3 = st.columns(3)
    with c1:
        locations = get_locations()
        location = st.selectbox("Location", locations or ["Sydney"])
    with c2:
        date_range = st.date_input("Date Range", [])
    with c3:
        granularity = st.selectbox("Granularity", ["Daily", "Hourly (Mock)"])

    start, end = None, None
    if isinstance(date_range, (list, tuple)) and len(date_range) == 2:
        start, end = date_range

    df = get_weather_data(location, start_date=start, end_date=end)

    # ── top KPI metrics ──────────────────────────────────────────
    if not df.empty:
        latest = df.iloc[-1]
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Min Temp", f"{latest.get('MinTemp', '–')} °C")
        m2.metric("Max Temp", f"{latest.get('MaxTemp', '–')} °C")
        m3.metric("Humidity 3pm", f"{latest.get('Humidity3pm', '–')}%")
        m4.metric("Pressure 3pm", f"{latest.get('Pressure3pm', '–')} hPa")

    # ── temperature trend ────────────────────────────────────────
    st.subheader("Temperature Trend (Min / Max)")
    st.plotly_chart(temperature_trend_chart(df), use_container_width=True)

    # ── rainfall + scatter ───────────────────────────────────────
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Rainfall Distribution")
        st.plotly_chart(rainfall_bar_chart(df), use_container_width=True)
    with col2:
        st.subheader("Humidity vs Rain (Scatter)")
        st.plotly_chart(humidity_scatter_chart(df), use_container_width=True)

    # ── wind direction ───────────────────────────────────────────
    st.subheader("Wind Direction Analysis")
    wind_df = get_wind_direction_data(location)
    col_w1, col_w2 = st.columns([1, 2])
    with col_w1:
        st.write("Frequency by direction:")
        st.dataframe(wind_df, use_container_width=True)
    with col_w2:
        st.plotly_chart(wind_rose_chart(wind_df), use_container_width=True)

    # ── historical comparison ────────────────────────────────────
    st.subheader("Rainfall: Current vs Previous Period")
    if not df.empty and "Rainfall" in df.columns:
        recent = df[["Date", "Rainfall"]].dropna().tail(14)
        if len(recent) >= 7:
            comp = pd.DataFrame({
                "Current Period": recent["Rainfall"].iloc[7:].values,
                "Previous Period": recent["Rainfall"].iloc[:7].values,
            })
            st.line_chart(comp)

    # ── agricultural parameters ──────────────────────────────────
    with st.expander("Agricultural Parameters", expanded=False):
        ic1, ic2 = st.columns(2)
        soil = ic1.slider("Soil Moisture (%)", 0, 100, 35)
        evap = ic2.slider("Evaporation Rate (mm/day)", 0.0, 20.0, 4.2, step=0.1)

        mc1, mc2, mc3 = st.columns(3)
        mc1.metric("Soil Moisture", f"{soil}%",
                   delta="Optimal" if 30 <= soil <= 60 else "Check Level",
                   delta_color="normal" if 30 <= soil <= 60 else "inverse")
        mc2.metric("Evaporation", f"{evap} mm/d", delta="-0.2 vs Yesterday")
        mc3.metric("Sensor Status", "Active" if soil > 20 else "Irrigation Req.", delta="Online")

    # ── raw data ─────────────────────────────────────────────────
    if not df.empty:
        with st.expander("Raw Data Sample"):
            st.dataframe(df.tail(20), use_container_width=True)
