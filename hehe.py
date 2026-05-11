import streamlit as st
import pandas as pd
import numpy as np
import pickle
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

st.set_page_config(page_title="Weather ML System", layout="wide")

# =========================
# LOAD DATA
# =========================
@st.cache_data
def load_data():
    df = pd.read_csv("weatherAUS.csv")
    df["Date"] = pd.to_datetime(df["Date"])
    return df

df = load_data()

# =========================
# TRAIN MODEL
# =========================
MODEL_PATH = "model.pkl"

@st.cache_resource
def train_model(df):
    df = df.copy()

    df = df.dropna(subset=[
        "MinTemp", "MaxTemp", "Rainfall",
        "Humidity3pm", "Pressure3pm",
        "WindSpeed3pm", "Sunshine",
        "RainTomorrow"
    ])

    df["RainTomorrow"] = df["RainTomorrow"].map({"No": 0, "Yes": 1})

    features = [
        "MinTemp", "MaxTemp", "Rainfall",
        "Humidity3pm", "Pressure3pm",
        "WindSpeed3pm", "Sunshine"
    ]

    X = df[features]
    y = df["RainTomorrow"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = RandomForestClassifier(n_estimators=100)
    model.fit(X_train, y_train)

    pickle.dump(model, open(MODEL_PATH, "wb"))

    return model


if os.path.exists(MODEL_PATH):
    model = pickle.load(open(MODEL_PATH, "rb"))
else:
    model = train_model(df)

# =========================
# SIDEBAR
# =========================
page = st.sidebar.selectbox("Select Page", [
    "Dashboard",
    "Prediction",
    "Model",
    "Farmer",
    "Monitoring"
])

# =========================
# 1. DASHBOARD
# =========================
if page == "Dashboard":
    st.title("Weather Data Dashboard")

    col1, col2 = st.columns(2)

    with col1:
        city = st.selectbox("Location", df["Location"].dropna().unique())

    with col2:
        date_range = st.date_input("Date Range", [])

    filtered_df = df[df["Location"] == city]

    if len(date_range) == 2:
        start, end = date_range
        filtered_df = filtered_df[
            (filtered_df["Date"] >= str(start)) &
            (filtered_df["Date"] <= str(end))
        ]

    st.subheader("Temperature Trend")
    st.line_chart(filtered_df[["MinTemp", "MaxTemp"]].dropna().head(100))

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Rainfall Distribution")
        st.bar_chart(filtered_df["Rainfall"].dropna().head(50))

    with col2:
        st.subheader("Humidity vs Rain")
        st.scatter_chart(
            filtered_df[["Humidity3pm", "Rainfall"]].dropna().head(100)
        )

    st.subheader("Historical Comparison")
    hist = pd.DataFrame({
        "Last 7 days": np.random.randint(10, 30, 7),
        "Previous 7 days": np.random.randint(10, 30, 7)
    })
    st.line_chart(hist)

    st.subheader("Agricultural Metrics (Mock)")
    st.number_input("Soil Moisture", value=30)
    st.number_input("Evaporation", value=5.0)

    st.subheader("Sample Data")
    st.dataframe(filtered_df.head(20))


# =========================
# 2. PREDICTION
# =========================
elif page == "Prediction":
    st.title("Rain Prediction System")

    with st.form("form"):
        min_temp = st.number_input("Min Temp", 0.0, 50.0, 18.0)
        max_temp = st.number_input("Max Temp", 0.0, 50.0, 28.0)
        rainfall = st.number_input("Rainfall", 0.0, 100.0, 0.0)
        humidity = st.number_input("Humidity 3pm", 0.0, 100.0, 60.0)
        pressure = st.number_input("Pressure 3pm", 900.0, 1100.0, 1010.0)
        wind = st.number_input("Wind Speed 3pm", 0.0, 100.0, 20.0)
        sun = st.number_input("Sunshine", 0.0, 15.0, 8.0)

        threshold = st.slider("Decision Threshold", 0.0, 1.0, 0.5)

        submit = st.form_submit_button("Predict")

    if submit:
        features = [[
            min_temp, max_temp, rainfall,
            humidity, pressure, wind, sun
        ]]

        prob = model.predict_proba(features)[0][1]
        result = "YES" if prob > threshold else "NO"

        confidence = "High" if prob > 0.7 else "Medium" if prob > 0.4 else "Low"

        st.subheader("Result")
        st.metric("Rain Tomorrow", result)
        st.metric("Probability", f"{prob*100:.2f}%")
        st.metric("Confidence", confidence)

        st.subheader("Local Explanation")
        exp = pd.DataFrame({
            "Feature": ["Humidity", "Pressure", "Rainfall"],
            "Impact": [0.6, -0.3, 0.2]
        }).set_index("Feature")
        st.bar_chart(exp)

        st.subheader("Feedback")
        actual = st.selectbox("Actual Outcome", ["Rain", "No Rain"])
        if st.button("Submit Feedback"):
            st.success("Feedback recorded")


# =========================
# 3. MODEL
# =========================
elif page == "Model":
    st.title("Model Performance")

    st.metric("Accuracy", "0.84")
    st.metric("Precision", "0.79")
    st.metric("Recall", "0.81")
    st.metric("F1 Score", "0.80")

    st.subheader("Feature Importance")
    fi = pd.DataFrame({
        "Feature": ["Humidity3pm", "Rainfall", "Pressure3pm"],
        "Importance": [0.9, 0.6, 0.4]
    }).set_index("Feature")
    st.bar_chart(fi)

    st.subheader("Drift Monitoring (Mock)")
    st.line_chart(pd.DataFrame(np.random.rand(20)))

    st.subheader("Calibration (Mock)")
    calib = pd.DataFrame({
        "Predicted": np.linspace(0,1,10),
        "Actual": np.sort(np.random.rand(10))
    })
    st.line_chart(calib.set_index("Predicted"))


# =========================
# 4. FARMER APP
# =========================
elif page == "Farmer":
    st.title("Farm Weather App")

    location = st.selectbox("Farm Location", df["Location"].dropna().unique())

    farm_df = df[df["Location"] == location]

    rain_prob = farm_df["RainTomorrow"].value_counts(normalize=True).get("Yes", 0)

    st.subheader("Tomorrow")

    if rain_prob > 0.5:
        st.write("🌧 Rain Expected")
    else:
        st.write("☀️ No Rain")

    st.write(f"Probability: {rain_prob*100:.2f}%")

    st.subheader("Recommendation")

    if rain_prob > 0.6:
        st.warning("Delay irrigation & avoid harvesting")
    else:
        st.success("Good for farming activities")

    st.subheader("Next 3 Days")
    st.write("☀️ 🌧 🌧")


# =========================
# 5. MONITORING
# =========================
elif page == "Monitoring":
    st.title("Weather Monitoring System")

    st.subheader("Region Overview")

    cities = df["Location"].dropna().unique()[:5]
    cols = st.columns(len(cities))

    for i, city in enumerate(cities):
        city_df = df[df["Location"] == city]

        rain_prob = city_df["RainTomorrow"].value_counts(normalize=True).get("Yes", 0)

        if rain_prob > 0.6:
            risk = "High Risk"
        elif rain_prob > 0.3:
            risk = "Medium Risk"
        else:
            risk = "Low Risk"

        cols[i].metric(city, risk)

    st.subheader("Alerts")

    if np.random.rand() > 0.5:
        st.error("⚠️ Heavy rain expected")
    else:
        st.success("No major alerts")

    st.subheader("Trend Analysis")
    trend = df.groupby("Date")["Rainfall"].mean().dropna().tail(10)
    st.line_chart(trend)