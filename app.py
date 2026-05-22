from datetime import datetime
import streamlit as st

from components.metrics import load_css, show_connection_status
from services.auth_service import ensure_admin, get_allowed_pages
from services.weather_service import is_connected, is_data_seeded, seed_from_csv
from views.login import show_login
from views.register import show_register
from views.dashboard import show_dashboard
from views.farmer_app import show_farmer_app
from views.model_performance import show_model_performance
from views.monitoring import show_monitoring
from views.rain_prediction import show_prediction

st.set_page_config(
    page_title="Intelligent Rain Monitor",
    page_icon="🌧️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── one-time startup tasks ────────────────────────────────────────
ensure_admin()

# ── auth gate ─────────────────────────────────────────────────────
if not st.session_state.get("authenticated"):
    auth_page = st.session_state.get("auth_page", "login")
    if auth_page == "register":
        show_register()
    else:
        show_login()
    st.stop()

# ── authenticated app ─────────────────────────────────────────────
load_css()

user        = st.session_state.user
role        = user["role"]
allowed     = get_allowed_pages(role)

_PAGE_FN = {
    "Weather Dashboard":  show_dashboard,
    "Rain Prediction":    show_prediction,
    "Model Performance":  show_model_performance,
    "Farmer App":         show_farmer_app,
    "Weather Monitoring": show_monitoring,
}

_ROLE_BADGE = {
    "admin":          ("Admin",          "#7c3aed"),
    "data_scientist": ("Data Scientist", "#0284c7"),
    "farmer":         ("Farmer",         "#16a34a"),
    "weather_agency": ("Weather Agency", "#b45309"),
}

badge_label, badge_color = _ROLE_BADGE.get(role, (role.title(), "#6b7280"))

# ── sidebar ───────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("<h2 style='color:#00d4ff;'>🌧️ Rain Monitor</h2>", unsafe_allow_html=True)
    st.markdown("---")

    # user info
    st.markdown(
        f"<div style='margin-bottom:4px;'>"
        f"<b style='font-size:15px;'>👤 {user['username']}</b></div>"
        f"<span style='background:{badge_color};color:white;border-radius:6px;"
        f"padding:2px 10px;font-size:11px;font-weight:600;'>{badge_label}</span>",
        unsafe_allow_html=True,
    )
    st.markdown("---")

    page = st.selectbox("Navigation", allowed)

    st.markdown("---")
    connected = is_connected()
    show_connection_status(connected)

    if connected and not is_data_seeded():
        st.warning("Database is empty.")
        if st.button("Seed Database from CSV", use_container_width=True):
            bar = st.progress(0, text="Starting...")
            def _cb(pct, text):
                bar.progress(pct, text=text)
            ok, msg = seed_from_csv(progress_callback=_cb)
            bar.empty()
            if ok:
                st.success(msg)
                st.cache_data.clear()
                st.rerun()
            else:
                st.error(msg)

    st.caption(f"Last sync: {datetime.now().strftime('%H:%M:%S')}")
    st.caption("System Status: **Operational**")
    st.markdown("---")

    if st.button("Logout", use_container_width=True):
        st.session_state.clear()
        st.rerun()

# ── page routing ──────────────────────────────────────────────────
_PAGE_FN[page]()

st.markdown("---")
st.markdown(
    "<div class='footer'>Intelligent Rain Monitor v2.0 | Powered by Streamlit, LightGBM & MongoDB</div>",
    unsafe_allow_html=True,
)
