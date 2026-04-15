import os
from pathlib import Path

BASE_DIR = "."

structure = {
    "app.py": """import streamlit as st

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
""",

    "config.py": """# Global config
APP_NAME = "Weather ML App"
VERSION = "1.0.0"
""",

    "requirements.txt": """streamlit
pandas
numpy
""",

    "pages/dashboard.py": """import streamlit as st
import time
import pandas as pd
import numpy as np
from utils.data_generator import gen_temp, gen_rain, gen_scatter

def show_dashboard():
    st.title("Weather Data Dashboard")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.selectbox("Location", ["Sydney", "Melbourne"])
    with c2:
        st.date_input("Date Range")
    with c3:
        granularity = st.selectbox("Granularity", ["Daily", "Hourly"])

    realtime = st.toggle("Realtime (mock)")

    n = 24 if granularity == "Hourly" else 10

    st.subheader("Temperature Trend")
    data = gen_temp(n)
    chart = st.line_chart(data)

    if realtime:
        for _ in range(5):
            time.sleep(0.3)
            chart.add_rows(gen_temp(n).tail(1))

    col1, col2 = st.columns(2)

    with col1:
        st.bar_chart(gen_rain())

    with col2:
        st.scatter_chart(gen_scatter())

    wind = pd.DataFrame(np.random.rand(1, 8),
        columns=["N","NE","E","SE","S","SW","W","NW"])
    st.dataframe(wind, width="stretch")
""",

    "pages/prediction.py": """import streamlit as st
import numpy as np

def show_prediction():
    st.title("Rain Prediction")

    with st.form("form"):
        temp = st.number_input("Temperature", value=25.0)
        humidity = st.number_input("Humidity", value=60)
        threshold = st.slider("Threshold", 0.0, 1.0, 0.5)

        submit = st.form_submit_button("Predict")

    if submit:
        prob = float(np.random.rand())
        result = "YES" if prob > threshold else "NO"

        st.metric("Result", result)
        st.metric("Probability", f"{prob:.2f}")
""",

    "pages/model_performance.py": """import streamlit as st
import pandas as pd
import numpy as np

def show_model_performance():
    st.title("Model Performance")

    st.metric("Accuracy", "0.84")
    st.metric("Precision", "0.79")

    cm = pd.DataFrame([[100,10],[20,80]])
    st.dataframe(cm)

    roc = pd.DataFrame({
        "x": np.linspace(0,1,50),
        "y": np.sort(np.random.rand(50))
    })
    st.line_chart(roc.set_index("x"))
""",

    "pages/farmer_app.py": """import streamlit as st

def show_farmer_app():
    st.title("Farmer App")

    st.success("Delay irrigation")
    st.warning("Avoid harvesting")
""",

    "pages/monitoring.py": """import streamlit as st
import pandas as pd
import numpy as np

def show_monitoring():
    st.title("Monitoring")

    st.metric("Sydney", "High Risk")

    trend = pd.DataFrame({
        "Last 7 days": np.random.randint(0,100,7)
    })
    st.line_chart(trend)
""",

    "components/styles.py": """import streamlit as st

def load_styles():
    st.markdown(\"\"\"
    <style>
    .block-container {padding-top: 1rem;}
    .card {
        background:#0e1117;
        border-radius:16px;
        padding:16px;
    }
    </style>
    \"\"\", unsafe_allow_html=True)
""",

    "utils/data_generator.py": """import numpy as np
import pandas as pd

def gen_temp(n):
    return pd.DataFrame({
        "Min": np.random.randint(10, 20, n),
        "Max": np.random.randint(20, 35, n)
    })

def gen_rain():
    return np.random.randint(0, 100, 10)

def gen_scatter():
    return pd.DataFrame({
        "Humidity": np.random.randint(40, 100, 50),
        "Rain": np.random.randint(0, 10, 50)
    })
"""
}

folders = ["pages", "components", "utils"]

def create_project():
    Path(BASE_DIR).mkdir(exist_ok=True)

    for folder in folders:
        Path(f"{BASE_DIR}/{folder}").mkdir(parents=True, exist_ok=True)

    for path, content in structure.items():
        file_path = Path(BASE_DIR) / path
        file_path.parent.mkdir(parents=True, exist_ok=True)

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

    print("✅ Project created successfully!")

if __name__ == "__main__":
    create_project()