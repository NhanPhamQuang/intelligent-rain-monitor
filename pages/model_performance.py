import streamlit as st
import pandas as pd
import numpy as np

def show_model_performance():
    st.title("Model Performance Dashboard")

    st.metric("Accuracy", "0.84")
    st.metric("Precision", "0.79")
    st.metric("Recall", "0.81")
    st.metric("F1 Score", "0.80")

    cm = pd.DataFrame([[1200,150],[180,980]],
        columns=["Pred: No","Pred: Yes"],
        index=["Actual: No","Actual: Yes"]
    )
    st.dataframe(cm, width="stretch")

    roc = pd.DataFrame({
        "x": np.linspace(0,1,50),
        "y": np.sort(np.random.rand(50))
    })
    st.line_chart(roc.set_index("x"))