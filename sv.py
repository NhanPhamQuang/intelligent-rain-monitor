import streamlit as st
import numpy as np
import pandas as pd
import time

st.set_page_config(page_title="Weather ML App (Full)", layout="wide")

# -----------------------------
# GLOBAL STYLE (dark-ish)
# -----------------------------
st.markdown("""
<style>
.block-container {padding-top: 1rem;}
.card {background:#0e1117;border-radius:16px;padding:16px;box-shadow:0 6px 20px rgba(0,0,0,.25);} 
.small {opacity:.7;font-size:12px}
</style>
""", unsafe_allow_html=True)

# Sidebar Navigation
page = st.sidebar.selectbox("Select Page", [
    "Weather Dashboard",
    "Rain Prediction",
    "Model Performance",
    "Farmer App",
    "Weather Monitoring"
])

# -----------------------------
# 1. WEATHER DASHBOARD
# -----------------------------
if page == "Weather Dashboard":
    st.title("Weather Data Dashboard")

    c1, c2, c3 = st.columns(3)
    with c1:
        location = st.selectbox("Location", ["Sydney", "Melbourne"])
    with c2:
        date = st.date_input("Date Range")
    with c3:
        granularity = st.selectbox("Granularity", ["Daily", "Hourly (Mock)"])

    # Simulate real-time toggle
    realtime = st.toggle("Simulate Real-time Streaming (mock)")

    def gen_temp(n):
        return pd.DataFrame({
            "Min": np.random.randint(10, 20, n),
            "Max": np.random.randint(20, 35, n)
        })

    n = 24 if granularity.startswith("Hourly") else 10
    st.subheader("Temperature Trend (Min/Max)")
    temp_data = gen_temp(n)
    temp_chart = st.line_chart(temp_data)

    if realtime:
        for _ in range(10):
            time.sleep(0.3)
            temp_data = gen_temp(n)
            temp_chart.add_rows(temp_data.tail(1))

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Rainfall Distribution")
        rain = np.random.randint(0, 100, 10)
        st.bar_chart(rain)

    with col2:
        st.subheader("Humidity vs Rain (Scatter)")
        scatter = pd.DataFrame({
            "Humidity": np.random.randint(40, 100, 50),
            "Rain": np.random.randint(0, 10, 50)
        })
        st.scatter_chart(scatter)

    st.subheader("Wind Direction Heatmap")
    wind = pd.DataFrame(np.random.rand(1, 8), columns=["N","NE","E","SE","S","SW","W","NW"])
    # st.dataframe(wind, use_container_width=True)
    st.dataframe(wind, width="stretch")

    st.subheader("Historical Comparison (Last 7 days vs Current)")
    hist = pd.DataFrame({
        "Last_7_Days": np.random.randint(10, 30, 7),
        "Current_Period": np.random.randint(10, 30, 7)
    })
    st.line_chart(hist)

    st.info("Agricultural metrics (soil moisture, evaporation) are included below as mock inputs for UI completeness.")

    m1, m2 = st.columns(2)
    with m1:
        soil = st.number_input("Soil Moisture (mock)", value=30)
    with m2:
        evap = st.number_input("Evaporation (mock)", value=5.0)

# -----------------------------
# 2. RAIN PREDICTION
# -----------------------------
elif page == "Rain Prediction":
    st.title("Rain Prediction System")

    with st.form("prediction_form"):
        location = st.selectbox("Location", ["Sydney"])
        min_temp = st.number_input("Min Temp", value=18.5)
        max_temp = st.number_input("Max Temp", value=27.3)
        rainfall = st.number_input("Rainfall", value=0.0)
        humidity = st.number_input("Humidity 3pm", value=65)
        pressure = st.number_input("Pressure 3pm", value=1012)
        wind = st.number_input("Wind Speed 3pm", value=20)
        sun = st.number_input("Sunshine", value=8.5)
        soil = st.number_input("Soil Moisture (mock)", value=30)
        evap = st.number_input("Evaporation (mock)", value=5.0)

        threshold = st.slider("Decision Threshold", 0.0, 1.0, 0.5)

        submit = st.form_submit_button("Predict")

    if submit:
        prob = float(np.random.rand())
        result = "YES" if prob > threshold else "NO"
        confidence = "High" if prob > 0.7 else "Medium" if prob > 0.4 else "Low"

        st.subheader("Result")
        colA, colB, colC = st.columns(3)
        colA.metric("Rain Tomorrow", result)
        colB.metric("Probability", f"{round(prob*100,2)}%")
        colC.metric("Confidence", confidence)

        # Local explainability (visual + text)
        st.subheader("Local Explanation (per prediction)")
        exp = pd.DataFrame({
            "Feature": ["Humidity3pm", "Pressure3pm", "Rainfall"],
            "Impact": [0.6, -0.3, 0.2]
        }).set_index("Feature")
        st.bar_chart(exp)
        st.caption("Higher humidity increases rain probability; lower pressure increases likelihood of rain.")

        # Feedback loop
        st.subheader("Ground Truth Feedback")
        actual = st.selectbox("Actual Outcome", ["Rain", "No Rain"])
        if st.button("Submit Feedback"):
            st.success("Feedback recorded (mock) for future model tuning.")

# -----------------------------
# 3. MODEL PERFORMANCE
# -----------------------------
elif page == "Model Performance":
    st.title("Model Performance Dashboard")

    model = st.selectbox("Model", ["Random Forest", "XGBoost"])

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Accuracy", "0.84")
    c2.metric("Precision", "0.79")
    c3.metric("Recall", "0.81")
    c4.metric("F1 Score", "0.80")

    st.subheader("Confusion Matrix (Actual vs Predicted)")
    cm = pd.DataFrame([[1200,150],[180,980]], columns=["Pred: No","Pred: Yes"], index=["Actual: No","Actual: Yes"])
    # st.dataframe(cm, use_container_width=True)
    st.dataframe(cm, width="stretch")

    st.subheader("ROC Curve (0–1)")
    roc = pd.DataFrame({"x": np.linspace(0,1,50), "y": np.sort(np.random.rand(50))})
    st.line_chart(roc.set_index("x"))

    st.subheader("Feature Importance")
    fi = pd.DataFrame({
        "Feature": ["Humidity3pm","Rainfall","Pressure3pm"],
        "Importance": [0.9,0.6,0.4]
    }).set_index("Feature")
    st.bar_chart(fi)

    # Drift monitoring (mock)
    st.subheader("Model & Data Drift Monitoring (mock)")
    drift = pd.DataFrame({"Feature Drift": np.random.rand(30)})
    st.line_chart(drift)
    st.caption("Tracks distribution shift over time to trigger retraining.")

    # Calibration (mock but structured)
    st.subheader("Probability Calibration Curve (Predicted vs Actual)")
    bins = np.linspace(0,1,10)
    calib = pd.DataFrame({
        "Predicted": bins,
        "Actual": np.clip(bins + np.random.normal(0,0.05,len(bins)), 0, 1)
    })
    st.line_chart(calib.set_index("Predicted"))

# -----------------------------
# 4. FARMER APP (light/simple)
# -----------------------------
elif page == "Farmer App":
    st.title("Farm Weather App")

    location = st.selectbox("Farm Location", ["Farm 1"])

    card = st.container()
    with card:
        st.markdown("### 🌧 Tomorrow: RAIN")
        st.write("Probability: 78%")

    st.subheader("Recommendation")
    st.success("Delay irrigation")
    st.warning("Avoid harvesting")

    st.subheader("Next 3 Days")
    st.write("☀️ 🌧 🌧")

# -----------------------------
# 5. WEATHER MONITORING
# -----------------------------
elif page == "Weather Monitoring":
    st.title("Weather Monitoring System")

    st.subheader("Region Overview")
    r1, r2 = st.columns(2)
    r1.metric("Sydney", "High Risk")
    r2.metric("Melbourne", "Low Risk")

    st.subheader("Alerts")
    st.error("⚠️ Heavy rain expected in NSW")

    st.subheader("Trend Analysis (Historical)")
    trend = pd.DataFrame({
        "Last 7 days": np.random.randint(0,100,7),
        "Previous 7 days": np.random.randint(0,100,7)
    })
    st.line_chart(trend)

    st.caption("Supports anomaly detection and long-term climate monitoring (mock).")
