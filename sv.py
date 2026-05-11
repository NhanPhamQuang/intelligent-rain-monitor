import streamlit as st
import numpy as np
import pandas as pd
import time
import plotly.express as px
import plotly.graph_objects as go

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

# st.markdown("""
# <style>
#     /* 1. Ẩn hoàn toàn Sidebar mặc định của Streamlit */
#     [data-testid="stSidebar"] {
#         display: none;
#     }
#     [data-testid="stSidebarCollapsedControl"] {
#         display: none;
#     }
#
#     /* 2. Tối ưu không gian nội dung chính */
#     .block-container {
#         padding-top: 2rem;    /* Khoảng cách trên cùng */
#         padding-bottom: 2rem;
#         max-width: 95%;      /* Mở rộng chiều ngang để Dashboard thoáng hơn */
#     }
#
#     /* 3. Style cho các Card (Nền tối, bo góc, bóng đổ) */
#     .card {
#         background: #0e1117;
#         border: 1px solid #30363d; /* Thêm viền nhẹ cho giống Dashboard cao cấp */
#         border-radius: 16px;
#         padding: 20px;
#         box-shadow: 0 6px 20px rgba(0,0,0,.25);
#         margin-bottom: 15px;
#     }
#
#     /* 4. Text nhỏ cho các ghi chú */
#     .small {
#         opacity: .7;
#         font-size: 13px;
#     }
# </style>
# """, unsafe_allow_html=True)

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
        # location = st.selectbox("Location", ["Sydney", "Melbourne"])
        locations = [
            'Albury', 'BadgerysCreek', 'Cobar', 'CoffsHarbour', 'Moree',
            'Newcastle', 'NorahHead', 'NorfolkIsland', 'Penrith', 'Richmond',
            'Sydney', 'SydneyAirport', 'WaggaWagga', 'Williamtown',
            'Wollongong', 'Canberra', 'Tuggeranong', 'MountGinini', 'Ballarat',
            'Bendigo', 'Sale', 'MelbourneAirport', 'Melbourne', 'Mildura',
            'Nhil', 'Portland', 'Watsonia', 'Dartmoor', 'Brisbane', 'Cairns',
            'GoldCoast', 'Townsville', 'Adelaide', 'MountGambier', 'Nuriootpa',
            'Woomera', 'Albany', 'Witchcliffe', 'PearceRAAF', 'PerthAirport',
            'Perth', 'SalmonGums', 'Walpole', 'Hobart', 'Launceston',
            'AliceSprings', 'Darwin', 'Katherine', 'Uluru'
        ]

        # Tạo selectbox với danh sách đầy đủ
        location = st.selectbox("Location", locations)
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

    # st.subheader("Wind Direction Heatmap")
    # wind = pd.DataFrame(np.random.rand(1, 8), columns=["N","NE","E","SE","S","SW","W","NW"])
    # # st.dataframe(wind, use_container_width=True)
    # st.dataframe(wind, width="stretch")

    st.subheader("Wind Direction Analysis")

    # 1. Chuẩn bị dữ liệu có cấu trúc hơn
    directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
    # Giả lập giá trị (ví dụ: tần suất gió thổi theo các hướng tính bằng %)
    values = np.random.randint(5, 30, size=8)

    df_wind = pd.DataFrame({
        "Direction": directions,
        "Frequency": values
    })

    # 2. Tạo biểu đồ Radar (Wind Rose đơn giản) bằng Plotly
    fig = px.line_polar(
        df_wind,
        r="Frequency",
        theta="Direction",
        line_close=True,
        template="plotly_white",
        color_discrete_sequence=["#00CC96"]
    )

    fig.update_traces(fill='toself')  # Tô màu vùng bên trong biểu đồ

    # 3. Hiển thị lên Streamlit
    col1, col2 = st.columns([1, 2])

    with col1:
        st.write("Dữ liệu chi tiết:")
        st.dataframe(df_wind, width="stretch")

    with col2:
        st.plotly_chart(fig, width="stretch")

    st.subheader("Historical Comparison (Last 7 days vs Current)")
    hist = pd.DataFrame({
        "Last_7_Days": np.random.randint(10, 30, 7),
        "Current_Period": np.random.randint(10, 30, 7)
    })
    st.line_chart(hist)

    # st.info("Agricultural metrics (soil moisture, evaporation) are included below as mock inputs for UI completeness.")
    #
    # m1, m2 = st.columns(2)
    # with m1:
    #     soil = st.number_input("Soil Moisture (mock)", value=30)
    # with m2:
    #     evap = st.number_input("Evaporation (mock)", value=5.0)

    # --- Agricultural Metrics Section ---
    with st.expander("🌱 Agricultural Parameters Configuration", expanded=True):
        st.info("Adjust the sliders to simulate real-time soil and atmospheric conditions.")

        # Chia layout thành 2 cột cho phần nhập liệu
        input_col1, input_col2 = st.columns(2)

        with input_col1:
            soil_value = st.slider(
                "Soil Moisture (%)",
                min_value=0,
                max_value=100,
                value=35,
                help="Current water content in the soil."
            )

        with input_col2:
            evap_value = st.slider(
                "Evaporation Rate (mm/day)",
                min_value=0.0,
                max_value=20.0,
                value=4.2,
                step=0.1,
                help="Rate of water evaporation from the land surface."
            )

        st.markdown("---")  # Đường kẻ phân cách

        # Hiển thị kết quả dưới dạng Metric (thường thấy trong các Dashboard giám sát)
        metric_col1, metric_col2, metric_col3 = st.columns(3)

        # Cột 1: Hiển thị độ ẩm
        metric_col1.metric(
            label="Soil Moisture",
            value=f"{soil_value}%",
            delta="Optimal" if 30 <= soil_value <= 60 else "Check Level",
            delta_color="normal" if 30 <= soil_value <= 60 else "inverse"
        )

        # Cột 2: Hiển thị bay hơi
        metric_col2.metric(
            label="Evaporation",
            value=f"{evap_value} mm/d",
            delta="-0.2 vs Yesterday"
        )

        # Cột 3: Trạng thái hệ thống (Thêm vào để UI đầy đủ hơn)
        status = "Active" if soil_value > 20 else "Irrigation Req."
        metric_col3.metric(
            label="Sensor Status",
            value=status,
            delta="Online",
            delta_color="normal"
        )

# # -----------------------------
# # 2. RAIN PREDICTION
# # -----------------------------
# elif page == "Rain Prediction":
#     st.title("Rain Prediction System")
#
#     with st.form("prediction_form"):
#         location = st.selectbox("Location", ["Sydney"])
#         min_temp = st.number_input("Min Temp", value=18.5)
#         max_temp = st.number_input("Max Temp", value=27.3)
#         rainfall = st.number_input("Rainfall", value=0.0)
#         humidity = st.number_input("Humidity 3pm", value=65)
#         pressure = st.number_input("Pressure 3pm", value=1012)
#         wind = st.number_input("Wind Speed 3pm", value=20)
#         sun = st.number_input("Sunshine", value=8.5)
#         soil = st.number_input("Soil Moisture (mock)", value=30)
#         evap = st.number_input("Evaporation (mock)", value=5.0)
#
#         threshold = st.slider("Decision Threshold", 0.0, 1.0, 0.5)
#
#         submit = st.form_submit_button("Predict")
#
#     if submit:
#         prob = float(np.random.rand())
#         result = "YES" if prob > threshold else "NO"
#         confidence = "High" if prob > 0.7 else "Medium" if prob > 0.4 else "Low"
#
#         st.subheader("Result")
#         colA, colB, colC = st.columns(3)
#         colA.metric("Rain Tomorrow", result)
#         colB.metric("Probability", f"{round(prob*100,2)}%")
#         colC.metric("Confidence", confidence)
#
#         # Local explainability (visual + text)
#         st.subheader("Local Explanation (per prediction)")
#         exp = pd.DataFrame({
#             "Feature": ["Humidity3pm", "Pressure3pm", "Rainfall"],
#             "Impact": [0.6, -0.3, 0.2]
#         }).set_index("Feature")
#         st.bar_chart(exp)
#         st.caption("Higher humidity increases rain probability; lower pressure increases likelihood of rain.")
#
#         # Feedback loop
#         st.subheader("Ground Truth Feedback")
#         actual = st.selectbox("Actual Outcome", ["Rain", "No Rain"])
#         if st.button("Submit Feedback"):
#             st.success("Feedback recorded (mock) for future model tuning.")

# -----------------------------
# 2. RAIN PREDICTION (ENHANCED)
# -----------------------------
elif page == "Rain Prediction":
    st.title("🌧️ Rain Prediction System")
    st.markdown("Enter meteorological parameters to estimate the probability of rain for tomorrow.")

    # Sử dụng expander để ẩn bớt các thông số phụ, tập trung vào form chính
    with st.form("prediction_form", border=True):
        st.subheader("Input Parameters")

        # Chia làm 3 cột để tối ưu không gian
        c1, c2, c3 = st.columns(3)
        with c1:
            location = st.selectbox("📍 Location", ["Sydney", "Melbourne", "Brisbane"])
            min_temp = st.number_input("🌡️ Min Temp (°C)", value=18.5)
            max_temp = st.number_input("🌡️ Max Temp (°C)", value=27.3)
        with c2:
            rainfall = st.number_input("💧 Rainfall (mm)", value=0.0)
            humidity = st.slider("🌫️ Humidity 3pm (%)", 0, 100, 65)
            sun = st.slider("☀️ Sunshine (hr)", 0.0, 16.0, 8.5)
        with c3:
            pressure = st.number_input("⏲️ Pressure 3pm (hPa)", value=1012)
            wind = st.number_input("💨 Wind Speed (km/h)", value=20)
            evap = st.number_input("☁️ Evaporation (mm)", value=5.0)

        with st.expander("Advanced Settings"):
            threshold = st.select_slider("Decision Threshold", options=[round(x, 1) for x in np.arange(0.1, 1.0, 0.1)],
                                         value=0.5)
            st.caption("Lowering threshold increases sensitivity to rain detection.")

        submit = st.form_submit_button("Run Model Prediction", use_container_width=True, type="primary")

    if submit:
        # Mocking Prediction Logic
        prob = float(np.random.rand())
        is_rain = prob > threshold
        result = "YES" if is_rain else "NO"

        # Color coding based on result
        status_color = "red" if is_rain else "green"

        st.divider()

        # Tạo các Tab để xem kết quả và giải thích riêng biệt
        tab1, tab2 = st.tabs(["🎯 Prediction Result", "🧠 Model Explainability"])

        with tab1:
            colA, colB, colC = st.columns(3)
            colA.metric("Rain Tomorrow", result, delta="Likely" if is_rain else "Unlikely",
                        delta_color="inverse" if is_rain else "normal")
            colB.metric("Probability", f"{round(prob * 100, 2)}%")

            conf_level = "High" if prob > 0.8 or prob < 0.2 else "Medium"
            colC.metric("Confidence", conf_level)

            if is_rain:
                st.error(f"High probability of rain detected ({round(prob * 100, 1)}%). Consider carrying an umbrella!")
            else:
                st.success(f"Low probability of rain ({round(prob * 100, 1)}%). Enjoy your day!")

            # Progress bar for visual probability
            st.progress(prob, text=f"Probability scale: {round(prob * 100, 1)}%")

        with tab2:
            st.subheader("Feature Impact (SHAP values)")
            # Tạo dữ liệu giải thích trực quan hơn
            exp_data = pd.DataFrame({
                "Feature": ["Humidity", "Pressure", "Sunshine", "Wind Speed", "Rainfall"],
                "Contribution": [0.45, -0.32, -0.25, 0.15, 0.1]
            }).sort_values(by="Contribution")

            # Sử dụng bar_chart với màu sắc tùy biến nếu dùng thư viện ngoài,
            # hoặc đơn giản là dùng biểu đồ ngang của streamlit
            st.bar_chart(exp_data.set_index("Feature"))
            st.info(
                "**Insight:** Higher humidity and recent rainfall are pushing the model towards a 'YES' prediction, while high pressure is pulling it back.")

        # Feedback loop nằm dưới cùng
        st.divider()
        st.subheader("📝 Ground Truth Feedback")
        f1, f2 = st.columns([2, 1])
        with f1:
            actual = st.radio("What was the actual outcome?", ["Rain", "No Rain"], horizontal=True)
        with f2:
            if st.button("Submit Feedback", use_container_width=True):
                st.toast("Thank you! Feedback saved for retraining.", icon="✅")

# -----------------------------
# 3. MODEL PERFORMANCE
# -----------------------------
# elif page == "Model Performance":
#     st.title("Model Performance Dashboard")
#
#     model = st.selectbox("Model", ["Random Forest", "XGBoost"])
#
#     c1, c2, c3, c4 = st.columns(4)
#     c1.metric("Accuracy", "0.84")
#     c2.metric("Precision", "0.79")
#     c3.metric("Recall", "0.81")
#     c4.metric("F1 Score", "0.80")
#
#     st.subheader("Confusion Matrix (Actual vs Predicted)")
#     cm = pd.DataFrame([[1200,150],[180,980]], columns=["Pred: No","Pred: Yes"], index=["Actual: No","Actual: Yes"])
#     # st.dataframe(cm, use_container_width=True)
#     st.dataframe(cm, width="stretch")
#
#     st.subheader("ROC Curve (0–1)")
#     roc = pd.DataFrame({"x": np.linspace(0,1,50), "y": np.sort(np.random.rand(50))})
#     st.line_chart(roc.set_index("x"))
#
#     st.subheader("Feature Importance")
#     fi = pd.DataFrame({
#         "Feature": ["Humidity3pm","Rainfall","Pressure3pm"],
#         "Importance": [0.9,0.6,0.4]
#     }).set_index("Feature")
#     st.bar_chart(fi)
#
#     # Drift monitoring (mock)
#     st.subheader("Model & Data Drift Monitoring (mock)")
#     drift = pd.DataFrame({"Feature Drift": np.random.rand(30)})
#     st.line_chart(drift)
#     st.caption("Tracks distribution shift over time to trigger retraining.")
#
#     # Calibration (mock but structured)
#     st.subheader("Probability Calibration Curve (Predicted vs Actual)")
#     bins = np.linspace(0,1,10)
#     calib = pd.DataFrame({
#         "Predicted": bins,
#         "Actual": np.clip(bins + np.random.normal(0,0.05,len(bins)), 0, 1)
#     })
#     st.line_chart(calib.set_index("Predicted"))

# -----------------------------
# 3. MODEL PERFORMANCE (ENHANCED)
# -----------------------------
elif page == "Model Performance":
    st.title("📊 Model Performance Dashboard")

    # Header với lựa chọn Model và Version
    top_c1, top_c2 = st.columns([2, 1])
    with top_c1:
        model_name = st.selectbox("Select Model Architecture", ["Random Forest", "XGBoost", "LightGBM"])
    with top_c2:
        st.info(f"**Status:** Production\n\n**Last Retrained:** 2026-03-15")

    # 1. Key Metrics Highlighting
    st.subheader("Core Metrics")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Accuracy", "0.842", delta="0.01")
    m2.metric("Precision", "0.795", delta="-0.02")
    m3.metric("Recall", "0.810", delta="0.05")
    m4.metric("F1 Score", "0.802", delta="0.02")

    st.divider()

    # 2. Confusion Matrix & ROC Curve (Bố cục ngang)
    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("Confusion Matrix")
        cm_data = [[1200, 150], [180, 980]]
        labels = ["No Rain", "Rain"]

        # Sử dụng Plotly Heatmap cho Confusion Matrix nhìn chuyên nghiệp hơn
        fig_cm = px.imshow(
            cm_data,
            x=labels, y=labels,
            labels=dict(x="Predicted", y="Actual", color="Count"),
            text_auto=True,
            color_continuous_scale='Blues'
        )
        st.plotly_chart(fig_cm, use_container_width=True)

    with col_right:
        st.subheader("ROC Curve")
        # Giả lập đường cong ROC mượt mà hơn
        fpr = np.linspace(0, 1, 100)
        tpr = np.sqrt(fpr)  # Giả lập đường cong tốt

        fig_roc = go.Figure()
        fig_roc.add_trace(
            go.Scatter(x=fpr, y=tpr, mode='lines', name='Model (AUC = 0.89)', line=dict(color='firebrick', width=3)))
        fig_roc.add_trace(go.Scatter(x=[0, 1], y=[0, 1], mode='lines', name='Random', line=dict(dash='dash')))
        fig_roc.update_layout(xaxis_title='False Positive Rate', yaxis_title='True Positive Rate', height=400)
        st.plotly_chart(fig_roc, use_container_width=True)

    # 3. Feature Importance & Drift (Tabs cho gọn)
    st.divider()
    tab_fi, tab_drift, tab_calib = st.tabs(["🔥 Feature Importance", "📉 Drift Monitoring", "🎯 Calibration"])

    with tab_fi:
        fi_data = pd.DataFrame({
            "Feature": ["Humidity3pm", "Rainfall", "Pressure3pm", "Sunshine", "WindSpeed3pm", "Temp3pm"],
            "Importance": [0.35, 0.25, 0.15, 0.12, 0.08, 0.05]
        }).sort_values(by="Importance", ascending=True)

        fig_fi = px.bar(fi_data, x='Importance', y='Feature', orientation='h', title="Gini Importance")
        st.plotly_chart(fig_fi, use_container_width=True)

    with tab_drift:
        st.write("Tracking Population Stability Index (PSI) over last 30 days.")
        drift_data = pd.DataFrame({
            "Day": range(1, 31),
            "Drift Score": np.random.normal(0.1, 0.02, 30)
        })
        # Highlight vùng nguy hiểm
        fig_drift = px.area(drift_data, x="Day", y="Drift Score", title="Feature Drift (PSI)")
        fig_drift.add_hline(y=0.2, line_dash="dot", line_color="red", annotation_text="Retrain Trigger")
        st.plotly_chart(fig_drift, use_container_width=True)

    with tab_calib:
        bins = np.linspace(0, 1, 10)
        calib_data = pd.DataFrame({
            "Mean Predicted Value": bins,
            "Fraction of Positives": np.clip(bins + np.random.normal(0, 0.03, 10), 0, 1)
        })
        fig_cal = go.Figure()
        fig_cal.add_trace(
            go.Scatter(x=calib_data["Mean Predicted Value"], y=calib_data["Fraction of Positives"], name="Model"))
        fig_cal.add_trace(
            go.Scatter(x=[0, 1], y=[0, 1], mode='lines', name='Perfectly Calibrated', line=dict(dash='dash')))
        fig_cal.update_layout(title="Reliability Curve", xaxis_title="Predicted Probability",
                              yaxis_title="Actual Fraction")
        st.plotly_chart(fig_cal, use_container_width=True)

# # -----------------------------
# # 4. FARMER APP (light/simple)
# # -----------------------------
# elif page == "Farmer App":
#     st.title("Farm Weather App")
#
#     location = st.selectbox("Farm Location", ["Farm 1"])
#
#     card = st.container()
#     with card:
#         st.markdown("### 🌧 Tomorrow: RAIN")
#         st.write("Probability: 78%")
#
#     st.subheader("Recommendation")
#     st.success("Delay irrigation")
#     st.warning("Avoid harvesting")
#
#     st.subheader("Next 3 Days")
#     st.write("☀️ 🌧 🌧")

# -----------------------------
# 4. FARMER APP (ENHANCED)
# -----------------------------
elif page == "Farmer App":
    st.title("👨‍🌾 Smart Farm Assistant")

    # Lựa chọn nông trại với giao diện gọn
    col_header, col_loc = st.columns([2, 1])
    with col_header:
        st.markdown(f"### Welcome back, Gia Lộc :))")
    with col_loc:
        location = st.selectbox("Select Farm", ["East Field", "West Orchard"], label_visibility="collapsed")

    st.divider()

    # 1. Main Weather Card (Sử dụng container và màu sắc để nhấn mạnh)
    rain_prob = 78

    # Tạo một "Card" giả lập bằng st.container và st.markdown
    with st.container(border=True):
        c1, c2 = st.columns([1, 2])
        with c1:
            # Icon thời tiết lớn
            st.markdown("<h1 style='text-align: center; font-size: 80px; margin: 0;'>🌧️</h1>", unsafe_allow_html=True)
        with c2:
            st.markdown("### Tomorrow's Outlook")
            st.markdown(f"<h2 style='color: #1f77b4; margin: 0;'>Heavy Rain Expected</h2>", unsafe_allow_html=True)
            st.write(f"Probability: **{rain_prob}%** | Expected: **12mm**")

    # 2. Recommendations (Biến thành danh sách việc cần làm)
    st.subheader("📋 Farm Management Advice")

    # Hiển thị các khuyến nghị dưới dạng Alert levels
    reco1, reco2 = st.columns(2)
    with reco1:
        st.error("**Delay Irrigation**\n\nRain will provide sufficient moisture. Save water and energy.")
    with reco2:
        st.warning("**Protect Seedlings**\n\nStrong winds and rain may damage young plants in the West Field.")

    st.info("💡 **Tip:** Apply fertilizer *after* the rain to ensure deep soil penetration.")

    # 3. Next 7 Days Forecast (Dạng bảng ngang trực quan)
    st.subheader("📅 7-Day Forecast")

    forecast_data = {
        "Day": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        "Icon": ["☀️", "🌧️", "🌧️", "☁️", "⛅", "☀️", "☀️"],
        "Temp": ["31°C", "24°C", "23°C", "27°C", "29°C", "30°C", "32°C"]
    }

    # Hiển thị forecast theo hàng ngang
    cols = st.columns(7)
    for i in range(7):
        with cols[i]:
            st.markdown(f"**{forecast_data['Day'][i]}**")
            st.markdown(f"### {forecast_data['Icon'][i]}")
            st.caption(forecast_data['Temp'][i])

    # 4. Quick Actions
    st.divider()
    if st.button("📲 Send Alert to Field Workers", use_container_width=True):
        st.toast("Alert sent to all registered workers via SMS!", icon="📡")

# -----------------------------
# 5. WEATHER MONITORING
# -----------------------------
# elif page == "Weather Monitoring":
#     st.title("Weather Monitoring System")
#
#     st.subheader("Region Overview")
#     r1, r2 = st.columns(2)
#     r1.metric("Sydney", "High Risk")
#     r2.metric("Melbourne", "Low Risk")
#
#     st.subheader("Alerts")
#     st.error("⚠️ Heavy rain expected in NSW")
#
#     st.subheader("Trend Analysis (Historical)")
#     trend = pd.DataFrame({
#         "Last 7 days": np.random.randint(0,100,7),
#         "Previous 7 days": np.random.randint(0,100,7)
#     })
#     st.line_chart(trend)
#
#     st.caption("Supports anomaly detection and long-term climate monitoring (mock).")

# -----------------------------
# 5. WEATHER MONITORING (ENHANCED)
# -----------------------------
elif page == "Weather Monitoring":
    st.title("🛡️ Weather Monitoring & Risk Assessment")
    st.markdown("Real-time monitoring of regional climate anomalies and risk distribution.")

    # 1. Regional Risk Overview (Dạng Dashboard hiện đại)
    st.subheader("Regional Risk Status")

    # Tạo layout 4 cột cho các khu vực chính
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Sydney", "High Risk", delta="Increasing", delta_color="inverse")
    m2.metric("Melbourne", "Low Risk", delta="Stable")
    m3.metric("Brisbane", "Moderate", delta="-5%", delta_color="normal")
    m4.metric("Perth", "Safe", delta="Stable")

    # 2. Active Alerts & Critical Notifications
    st.subheader("Active Alerts")
    with st.container():
        st.error("🔴 **Critical:** Heavy rain and potential flash flooding expected in NSW (Next 24h).")
        st.warning("🟡 **Advisory:** High UV index reported in Queensland. Heat exhaustion risk.")
        st.info("🔵 **Notice:** Sensor maintenance scheduled for Melbourne Station at 02:00 AM.")

    st.divider()

    # 3. Trend Analysis (Nâng cấp biểu đồ Historical)
    st.subheader("Historical Trend Analysis")

    # Tạo dữ liệu giả lập có ý nghĩa hơn (ví dụ: Lượng mưa trung bình)
    dates = pd.date_range(end=pd.Timestamp.now(), periods=14)
    trend_data = pd.DataFrame({
        "Date": dates,
        "Current Period": np.random.randint(10, 50, 14),
        "Historical Avg": np.random.randint(15, 45, 14)
    }).set_index("Date")

    # Sử dụng line_chart của Streamlit nhưng có thêm chú thích rõ ràng
    st.line_chart(trend_data, color=["#FF4B4B", "#0083B0"])

    st.caption(
        "🔍 **Trend Insight:** Current rainfall levels are 12% higher than the 10-year historical average for April.")

    # 4. Anomaly Detection (Tính năng nâng cao cho Research Intern)
    st.divider()
    st.subheader("Anomaly Detection (AI-Powered)")

    col_chart, col_info = st.columns([2, 1])

    with col_chart:
        # Giả lập biểu đồ phát hiện điểm bất thường (Anomaly)
        anomaly_data = pd.DataFrame({
            "Time": range(50),
            "Signal": np.sin(np.linspace(0, 10, 50)) + np.random.normal(0, 0.1, 50)
        })
        # Tạo một điểm bất thường giả
        anomaly_data.loc[35, "Signal"] = 2.5

        fig_anomaly = px.line(anomaly_data, x="Time", y="Signal", title="Real-time Sensor Signal")
        fig_anomaly.add_scatter(x=[35], y=[2.5], mode='markers', name='Anomaly',
                                marker=dict(color='red', size=12, symbol='x'))
        st.plotly_chart(fig_anomaly, use_container_width=True)

    with col_info:
        st.write("**Detection Summary**")
        st.success("✅ System Health: Good")
        st.error("🚨 Anomalies Detected: 1")
        st.markdown("""
        **Root Cause Analysis:**
        Sensor S-104 (Sydney) reported a sudden pressure drop. 
        Possible sensor malfunction or rapid storm front entry.
        """)
        if st.button("Generate Technical Report", use_container_width=True):
            st.toast("Generating PDF report... Please wait.")

    # st.divider()
    # st.caption("Data sources: Bureau of Meteorology (BOM) & IoT Sensor Network. Powered by Digital Twin Architecture.")
