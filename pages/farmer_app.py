import streamlit as st

def show_farmer_app():
    st.title("Farm Weather App")

    st.markdown("### 🌧 Tomorrow: RAIN")
    st.write("Probability: 78%")

    st.success("Delay irrigation")
    st.warning("Avoid harvesting")