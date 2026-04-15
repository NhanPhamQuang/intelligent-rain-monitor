import streamlit as st

def load_styles():
    st.markdown("""
    <style>
    .block-container {padding-top: 1rem;}
    .card {
        background:#0e1117;
        border-radius:16px;
        padding:16px;
        box-shadow:0 6px 20px rgba(0,0,0,.25);
    } 
    .small {opacity:.7;font-size:12px}
    </style>
    """, unsafe_allow_html=True)