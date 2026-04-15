import streamlit as st

from pages.dashboard import show_dashboard
from pages.prediction import show_prediction
from pages.model_performance import show_model_performance
from pages.farmer_app import show_farmer_app
from pages.monitoring import show_monitoring

from components.styles import load_styles

st.set_page_config(page_title="Weather ML App", layout="wide")

load_styles()

page = st.sidebar.selectbox("Select Page", [
    "Weather Dashboard",
    "Rain Prediction",
    "Model Performance",
    "Farmer App",
    "Weather Monitoring"
])

if page == "Weather Dashboard":
    show_dashboard()
elif page == "Rain Prediction":
    show_prediction()
elif page == "Model Performance":
    show_model_performance()
elif page == "Farmer App":
    show_farmer_app()
elif page == "Weather Monitoring":
    show_monitoring()