import streamlit as st
import numpy as np
import pandas as pd
import time
from datetime import datetime

# Cấu hình trang với giao diện rộng và tiêu đề chuyên nghiệp
st.set_page_config(
    page_title="WeatherAI - Predictive Intelligence",
    page_icon="⛈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------
# CUSTOM CSS & STYLING
# -----------------------------
st.markdown("""
<style>
    /* Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Gradient Background cho Sidebar */
    [data-testid="stSidebar"] {
        background-image: linear-gradient(#0e1117, #1a1c24);
        border-right: 1px solid rgba(255,255,255,0.1);
    }

    /* Tùy chỉnh Metrics */
    [data-testid="stMetricValue"] {
        font-size: 28px;
        font-weight: 700;
        color: #00d4ff;
    }

    /* Thẻ Card tùy chỉnh */
    .weather-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 20px;
        transition: transform 0.2s ease;
    }
    .weather-card:hover {
        border: 1px solid #00d4ff;
        background: rgba(255, 255, 255, 0.08);
    }

    /* Hiệu ứng Glassmorphism cho header */
    .main-header {
        background: linear-gradient(90deg, #00d4ff 0%, #004e92 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 2.5rem;
        margin-bottom: 1rem;
    }

    /* Tùy chỉnh Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 40px;
        white-space: pre-wrap;
        background-color: rgba(255,255,255,0.05);
        border-radius: 5px;
        padding: 10px 20px;
    }

    /* Footer */
    .footer {
        text-align: center;
        padding: 20px;
        opacity: 0.5;
        font-size: 0.8rem;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# SIDEBAR NAVIGATION
# -----------------------------
with st.sidebar:
    st.markdown("<h2 style='color:#00d4ff;'>🌤️ WeatherAI</h2>", unsafe_allow_html=True)
    st.markdown("---")
    page = st.selectbox("Navigation", [
        "🌐 Dashboard",
        "🧠 Rain Prediction",
        "📊 Model Insights",
        "👨‍🌾 Farmer Portal",
        "🚨 Alerts & Monitor"
    ])

    st.markdown("---")
    st.caption("System Status: **Operational**")
    st.caption(f"Last sync: {datetime.now().strftime('%H:%M:%S')}")


# -----------------------------
# HELPER FUNCTIONS
# -----------------------------
def get_mock_data(n):
    return pd.DataFrame({
        "Min Temp": np.random.normal(15, 3, n),
        "Max Temp": np.random.normal(25, 5, n),
        "Humidity": np.random.randint(40, 90, n)
    })


# -----------------------------
# 1. WEATHER DASHBOARD
# -----------------------------
if "Dashboard" in page:
    st.markdown("<h1 class='main-header'>Weather Intelligence Dashboard</h1>", unsafe_allow_html=True)

    # Top Filters Row
    col_a, col_b, col_c = st.columns([2, 2, 1])
    with col_a:
        locations = ['Sydney', 'Melbourne', 'Brisbane', 'Perth', 'Adelaide', 'Cairns', 'Darwin', 'Hobart']
        location = st.selectbox("📍 Select Location", locations)
    with col_b:
        date_range = st.date_input("📅 Observation Period", [datetime.now(), datetime.now()])
    with col_c:
        realtime = st.toggle("⚡ Live Mode", help="Simulate real-time data stream")

    # Metrics Row
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Current Temp", "24.5°C", "1.2°C")
    m2.metric("Humidity", "62%", "-5%")
    m3.metric("Wind Speed", "18 km/h", "2 km/h")
    m4.metric("UV Index", "8.2", "High", delta_color="inverse")

    # Main Visuals
    t1, t2 = st.tabs(["📈 Temperature Trends", "☁️ Rainfall Analysis"])

    with t1:
        st.subheader("Historical & Forecasted Temperature")
        data = get_mock_data(30)
        st.area_chart(data[["Min Temp", "Max Temp"]], color=["#00d4ff", "#ff4b4b"])

    with t2:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("#### Precipitation Distribution")
            st.bar_chart(np.random.gamma(2, 2, 15), color="#3366ff")
        with c2:
            st.markdown("#### Humidity Correlation")
            scatter_data = pd.DataFrame({
                "Pressure": np.random.normal(1013, 5, 100),
                "Rain": np.random.normal(5, 2, 100)
            })
            st.scatter_chart(scatter_data, x="Pressure", y="Rain", color="#00d4ff")

    # Bottom Grid
    st.markdown("---")
    col_bot1, col_bot2 = st.columns([1, 2])
    with col_bot1:
        st.markdown("##### Wind Direction (Octant)")
        wind_data = pd.DataFrame(np.random.randint(10, 50, (1, 8)),
                                 columns=["N", "NE", "E", "SE", "S", "SW", "W", "NW"])
        st.dataframe(wind_data, use_container_width=True)
    with col_bot2:
        st.markdown("##### Environmental Metrics")
        st.info("Soil moisture and evaporation rates are within optimal agricultural ranges.")
        sc1, sc2 = st.columns(2)
        sc1.slider("Soil Moisture (%)", 0, 100, 45)
        sc2.slider("Evaporation (mm)", 0.0, 15.0, 4.2)

# -----------------------------
# 2. RAIN PREDICTION
# -----------------------------
elif "Prediction" in page:
    st.markdown("<h1 class='main-header'>Predictive Rain Analytics</h1>", unsafe_allow_html=True)

    with st.expander("ℹ️ Model Information", expanded=False):
        st.write("Current model: **XGBoost Classifier v2.4**. Accuracy: 86.4% on validation set.")

    col_input, col_res = st.columns([1, 1])

    with col_input:
        st.markdown("### 📝 Input Features")
        with st.container(border=True):
            f1, f2 = st.columns(2)
            temp_min = f1.number_input("Min Temp (°C)", value=15.0)
            temp_max = f2.number_input("Max Temp (°C)", value=28.0)
            rain_today = f1.number_input("Rainfall Today (mm)", value=0.0)
            sunshine = f2.number_input("Sunshine (hr)", value=8.5)
            hum_3pm = st.slider("Humidity at 3pm (%)", 0, 100, 55)
            threshold = st.select_slider("Sensitivity Threshold", options=[0.3, 0.4, 0.5, 0.6, 0.7], value=0.5)

            predict_btn = st.button("Generate Prediction", use_container_width=True, type="primary")

    with col_res:
        if predict_btn:
            with st.spinner("Analyzing atmospheric patterns..."):
                time.sleep(1)
                prob = np.random.uniform(0, 1)
                will_rain = prob > threshold

                st.markdown("### 🎯 Result")
                status_color = "#ff4b4b" if will_rain else "#00c853"
                st.markdown(f"""
                    <div style="background:{status_color}22; border: 2px solid {status_color}; border-radius:15px; padding:30px; text-align:center;">
                        <h2 style="color:{status_color}; margin:0;">RAIN TOMORROW: {"YES" if will_rain else "NO"}</h2>
                        <h1 style="font-size:4rem; margin:10px 0;">{prob:.1%}</h1>
                        <p style="opacity:0.8;">Probability Score</p>
                    </div>
                """, unsafe_allow_html=True)

                st.markdown("#### Feature Importance (SHAP)")
                imp_data = pd.DataFrame({
                    "Feature": ["Humidity", "Sunshine", "Pressure", "Temp"],
                    "Impact": [0.45, -0.32, 0.15, 0.08]
                })
                st.bar_chart(imp_data.set_index("Feature"), horizontal=True, color="#00d4ff")

# -----------------------------
# 3. MODEL PERFORMANCE
# -----------------------------
elif "Insights" in page:
    st.markdown("<h1 class='main-header'>Model Diagnostics</h1>", unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("AUC-ROC", "0.91", "Good")
    c2.metric("F1-Score", "0.82", "+0.02")
    c3.metric("Log Loss", "0.24", "-0.01")
    c4.metric("Latency", "14ms", "Fast")

    col_l, col_r = st.columns(2)
    with col_l:
        st.markdown("##### Confusion Matrix")
        cm = [[850, 45], [92, 413]]
        st.table(pd.DataFrame(cm, columns=["Pred: No", "Pred: Yes"], index=["Actual: No", "Actual: Yes"]))

    with col_r:
        st.markdown("##### Learning Curve")
        lc_data = pd.DataFrame({"Train": np.sort(np.random.rand(20)), "Val": np.sort(np.random.rand(20)) * 0.9})
        st.line_chart(lc_data)

# -----------------------------
# 4. FARMER PORTAL
# -----------------------------
elif "Farmer" in page:
    st.markdown("<h1 class='main-header'>Smart Farming Assistant</h1>", unsafe_allow_html=True)

    col_farm, col_rec = st.columns([1, 1.5])

    with col_farm:
        st.markdown("""
        <div class="weather-card">
            <h3>📅 Forecast: Mixed Rain</h3>
            <p>Next 24 hours: 5.2mm expected</p>
            <hr>
            <p><b>Soil Condition:</b> Moderate</p>
            <p><b>Pest Risk:</b> Low</p>
        </div>
        """, unsafe_allow_html=True)

    with col_rec:
        st.subheader("Smart Recommendations")
        st.success("✅ **Irrigation:** Skip today. Rain expected at 4:00 PM.")
        st.warning("⚠️ **Fertilizing:** Not recommended before heavy rain.")
        st.info("ℹ️ **Harvesting:** Window of opportunity between 8 AM - 12 PM.")

# -----------------------------
# 5. ALERTS & MONITOR
# -----------------------------
else:
    st.markdown("<h1 class='main-header'>Real-time Monitoring</h1>", unsafe_allow_html=True)

    st.error("🚨 **High Alert:** Severe thunderstorm warning for South-East regions.")

    grid = st.columns(3)
    regions = [("Sydney", "Active", "75%"), ("Melbourne", "Stable", "12%"), ("Brisbane", "Warning", "45%")]

    for i, (name, status, risk) in enumerate(regions):
        with grid[i]:
            st.markdown(f"""
            <div class="weather-card">
                <h4>{name}</h4>
                <p>Status: <b>{status}</b></p>
                <h2 style="color:#00d4ff">{risk}</h2>
                <small>Risk Level</small>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("### Anomaly Detection Log")
    st.code("""
    [2023-10-27 10:15] INFO: Pressure drop detected in Sector 7G
    [2023-10-27 10:22] WARN: Unexpected temperature spike +4.5°C
    [2023-10-27 10:45] ALERT: Rain probability exceeded threshold (92%)
    """, language="bash")

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("---")
st.markdown("<div class='footer'>WeatherAI Predictive Engine © 2023 | Powered by Streamlit & Machine Learning</div>",
            unsafe_allow_html=True)