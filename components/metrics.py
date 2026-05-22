import os
import streamlit as st


def load_css():
    css_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "styles.css")
    if os.path.exists(css_path):
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def show_model_metrics(accuracy: float, precision: float, recall: float, f1: float, auc: float = None):
    n = 5 if auc is not None else 4
    cols = st.columns(n)
    cols[0].metric("Accuracy", f"{accuracy:.3f}", delta="+0.01")
    cols[1].metric("Precision", f"{precision:.3f}", delta="-0.02")
    cols[2].metric("Recall", f"{recall:.3f}", delta="+0.05")
    cols[3].metric("F1 Score", f"{f1:.3f}", delta="+0.02")
    if auc is not None:
        cols[4].metric("AUC-ROC", f"{auc:.3f}")


def show_connection_status(connected: bool):
    if connected:
        st.sidebar.success("MongoDB: Connected", icon="🟢")
    else:
        st.sidebar.error("MongoDB: Offline — CSV fallback active", icon="🔴")
