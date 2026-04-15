import streamlit as st
import numpy as np
import pandas as pd

def show_prediction():
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

        threshold = st.slider("Decision Threshold", 0.0, 1.0, 0.5)

        submit = st.form_submit_button("Predict")

    if submit:
        prob = float(np.random.rand())
        result = "YES" if prob > threshold else "NO"

        st.metric("Rain Tomorrow", result)
        st.metric("Probability", f"{round(prob*100,2)}%")