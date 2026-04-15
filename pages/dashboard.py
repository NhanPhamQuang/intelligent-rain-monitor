import streamlit as st
import time
import pandas as pd
import numpy as np
from utils.data_generator import gen_temp, gen_rain, gen_scatter

def show_dashboard():
    st.title("Weather Data Dashboard")

    c1, c2, c3 = st.columns(3)
    with c1:
        location = st.selectbox("Location", ["Sydney", "Melbourne"])
    with c2:
        date = st.date_input("Date Range")
    with c3:
        granularity = st.selectbox("Granularity", ["Daily", "Hourly (Mock)"])

    realtime = st.toggle("Simulate Real-time Streaming (mock)")

    n = 24 if granularity.startswith("Hourly") else 10

    st.subheader("Temperature Trend (Min/Max)")
    temp_data = gen_temp(n)
    chart = st.line_chart(temp_data)

    if realtime:
        for _ in range(10):
            time.sleep(0.3)
            chart.add_rows(gen_temp(n).tail(1))

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Rainfall Distribution")
        st.bar_chart(gen_rain())

    with col2:
        st.subheader("Humidity vs Rain")
        st.scatter_chart(gen_scatter())

    st.subheader("Wind Direction Heatmap")
    wind = pd.DataFrame(np.random.rand(1, 8),
                        columns=["N","NE","E","SE","S","SW","W","NW"])
    st.dataframe(wind, width="stretch")