import streamlit as st
import pandas as pd
import numpy as np

def show_monitoring():
    st.title("Weather Monitoring System")

    st.metric("Sydney", "High Risk")
    st.metric("Melbourne", "Low Risk")

    st.error("⚠️ Heavy rain expected")

    trend = pd.DataFrame({
        "Last 7 days": np.random.randint(0,100,7),
        "Previous 7 days": np.random.randint(0,100,7)
    })

    st.line_chart(trend)