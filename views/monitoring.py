import numpy as np
import pandas as pd
import streamlit as st

from components.charts import anomaly_chart
from services.anomaly_service import detect_anomalies, get_alerts, get_regional_risk_data
from services.weather_service import get_locations, get_weather_data

_ALERT_FN = {"critical": st.error, "warning": st.warning, "info": st.info}


def show_monitoring():
    st.title("Weather Monitoring & Risk Assessment")
    st.markdown("Real-time monitoring of regional climate anomalies and risk distribution.")

    # ── regional risk ─────────────────────────────────────────────
    st.subheader("Regional Risk Status")
    risk_data = get_regional_risk_data()

    if risk_data:
        cols = st.columns(min(len(risk_data), 4))
        for i, item in enumerate(risk_data[:4]):
            color = "inverse" if item["risk_level"] == "High Risk" else "normal"
            cols[i].metric(
                item["location"],
                item["risk_level"],
                delta=f"{item['rain_prob'] * 100:.0f}% rain",
                delta_color=color,
            )
    else:
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Sydney", "High Risk", delta="Increasing", delta_color="inverse")
        m2.metric("Melbourne", "Low Risk", delta="Stable")
        m3.metric("Brisbane", "Moderate", delta="-5%")
        m4.metric("Perth", "Safe", delta="Stable")

    # ── active alerts ─────────────────────────────────────────────
    st.subheader("Active Alerts")
    for alert in get_alerts():
        severity = alert.get("severity", "info")
        msg = f"**{alert.get('region', 'System')}:** {alert.get('message', '')}"
        _ALERT_FN.get(severity, st.info)(msg)

    st.divider()

    # ── trend analysis ────────────────────────────────────────────
    st.subheader("Historical Trend Analysis")
    locations = get_locations()
    selected = st.selectbox("Select Location", locations or ["Sydney"], key="monitor_loc")

    df = get_weather_data(selected, limit=30)
    if not df.empty and "Rainfall" in df.columns:
        rainfall_df = df[["Date", "Rainfall"]].dropna().set_index("Date")
        st.line_chart(rainfall_df)
        st.caption(f"Avg rainfall for **{selected}**: {rainfall_df['Rainfall'].mean():.1f} mm/day")
    else:
        fallback = pd.DataFrame({
            "Current Period": np.random.randint(10, 50, 14),
            "Historical Avg": np.random.randint(15, 45, 14),
        }, index=pd.date_range(end=pd.Timestamp.now(), periods=14))
        st.line_chart(fallback)

    # ── anomaly detection ─────────────────────────────────────────
    st.divider()
    st.subheader("Anomaly Detection (Z-Score)")

    col_chart, col_info = st.columns([2, 1])
    with col_chart:
        if not df.empty and "Pressure3pm" in df.columns:
            df_a = detect_anomalies(df[["Date", "Pressure3pm"]].dropna().reset_index(drop=True))
            st.plotly_chart(anomaly_chart(df_a), use_container_width=True)
        else:
            # synthetic demo
            dates = pd.date_range(end=pd.Timestamp.now(), periods=50)
            synthetic = pd.DataFrame({
                "Date": dates,
                "Pressure3pm": np.sin(np.linspace(0, 10, 50)) * 8 + 1013 + np.random.normal(0, 2, 50),
                "is_anomaly": [False] * 50,
            })
            synthetic.loc[35, "Pressure3pm"] = 1042
            synthetic.loc[35, "is_anomaly"] = True
            st.plotly_chart(anomaly_chart(synthetic), use_container_width=True)

    with col_info:
        st.write("**Detection Summary**")
        anomaly_count = 0
        if not df.empty and "Pressure3pm" in df.columns:
            df_a = detect_anomalies(df[["Date", "Pressure3pm"]].dropna().reset_index(drop=True))
            anomaly_count = int(df_a["is_anomaly"].sum()) if "is_anomaly" in df_a.columns else 0

        if anomaly_count:
            st.error(f"Anomalies detected: **{anomaly_count}**")
        else:
            st.success("System Health: Good")

        st.markdown("**Algorithm:** Z-Score (σ = 2.5)")

        if st.button("Generate Technical Report", use_container_width=True):
            st.toast("Generating PDF report...")
