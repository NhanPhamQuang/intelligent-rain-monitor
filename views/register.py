import streamlit as st
from services.auth_service import register_user, ROLE_LABELS

_SVG = """
<svg viewBox="0 0 420 560" xmlns="http://www.w3.org/2000/svg" style="display:block;width:100%;height:100%;">
  <defs>
    <linearGradient id="rsky" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%"   stop-color="#8fbdd3"/>
      <stop offset="55%"  stop-color="#6aa5c2"/>
      <stop offset="100%" stop-color="#4a8aad"/>
    </linearGradient>
    <linearGradient id="rsea" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%"   stop-color="#2a6e9e"/>
      <stop offset="100%" stop-color="#1a4f72"/>
    </linearGradient>
    <linearGradient id="rwave2" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%"   stop-color="#1d5980"/>
      <stop offset="100%" stop-color="#123d5a"/>
    </linearGradient>
  </defs>
  <rect width="420" height="560" fill="url(#rsky)"/>
  <g opacity="0.28">
    <ellipse cx="205" cy="52" rx="75" ry="30" fill="#4a6a7a"/>
    <ellipse cx="250" cy="40" rx="88" ry="34" fill="#5a7a8a"/>
    <ellipse cx="290" cy="52" rx="62" ry="26" fill="#4a6a7a"/>
  </g>
  <g opacity="0.55">
    <ellipse cx="70"  cy="82" rx="55" ry="26" fill="white"/>
    <ellipse cx="102" cy="68" rx="68" ry="31" fill="white"/>
    <ellipse cx="138" cy="78" rx="46" ry="22" fill="white"/>
  </g>
  <g opacity="0.40">
    <ellipse cx="305" cy="100" rx="46" ry="22" fill="white"/>
    <ellipse cx="340" cy="88"  rx="58" ry="26" fill="white"/>
    <ellipse cx="372" cy="98"  rx="38" ry="18" fill="white"/>
  </g>
  <g stroke="rgba(255,255,255,0.42)" stroke-width="1.8" stroke-linecap="round">
    <line x1="38"  y1="148" x2="30"  y2="166"/>
    <line x1="66"  y1="170" x2="58"  y2="188"/>
    <line x1="94"  y1="150" x2="86"  y2="168"/>
    <line x1="122" y1="178" x2="114" y2="196"/>
    <line x1="208" y1="172" x2="200" y2="190"/>
    <line x1="310" y1="142" x2="302" y2="160"/>
    <line x1="368" y1="152" x2="360" y2="170"/>
  </g>
  <path d="M0,308 C55,280 115,320 175,294 C235,268 295,308 355,282 C380,270 405,278 420,268 L420,560 L0,560 Z" fill="url(#rsea)"/>
  <path d="M0,348 C72,318 155,360 225,330 C285,306 345,342 420,318 L420,560 L0,560 Z" fill="url(#rwave2)" opacity="0.9"/>
  <path d="M0,392 C82,364 172,398 252,372 C314,354 378,382 420,365 L420,560 L0,560 Z" fill="#165070" opacity="0.88"/>
  <g transform="translate(188,304) rotate(-12)">
    <ellipse cx="0" cy="0"  rx="66" ry="13" fill="#c05810"/>
    <ellipse cx="0" cy="-2" rx="60" ry="9"  fill="#e07825" opacity="0.65"/>
  </g>
  <g transform="translate(198,270)">
    <circle cx="0" cy="-40" r="17" fill="#c87941"/>
    <path d="M-10,-52 Q0,-60 10,-52 Q8,-40 0,-37 Q-8,-40 -10,-52" fill="#2a1505"/>
    <path d="M-13,-24 Q0,-10 13,-24 L17,10 Q0,17 -17,10 Z" fill="#d4a020"/>
    <path d="M-13,-14 Q-30,-32 -40,-50" stroke="#c87941" stroke-width="9" stroke-linecap="round" fill="none"/>
    <path d="M13,-14 Q34,-30 46,-46"   stroke="#c87941" stroke-width="9" stroke-linecap="round" fill="none"/>
    <path d="M-6,10 L-13,30" stroke="#d4a020" stroke-width="8" stroke-linecap="round"/>
    <path d="M6,10  L15,28"  stroke="#d4a020" stroke-width="8" stroke-linecap="round"/>
  </g>
  <text x="210" y="488" text-anchor="middle" font-size="17" font-weight="700"
        fill="white" font-family="Arial,sans-serif">Create Your Account</text>
  <text x="210" y="510" text-anchor="middle" font-size="11"
        fill="rgba(255,255,255,0.72)" font-family="Arial,sans-serif">Join the Rain Monitor network</text>
  <path d="M0,530 C70,520 140,536 210,524 C280,512 350,530 420,518 L420,560 L0,560 Z"
        fill="rgba(255,255,255,0.07)"/>
</svg>
"""

_CSS = """
<style>
[data-testid="stSidebar"]   { display: none !important; }
[data-testid="stHeader"]    { display: none !important; }
#MainMenu                   { display: none !important; }
footer                      { display: none !important; }

.block-container {
    padding: 2rem 1rem 1rem 1rem !important;
    max-width: 860px !important;
    margin: 0 auto !important;
}
.stApp { background: #c3d8e5 !important; }

div[data-testid="stHorizontalBlock"] {
    background: white;
    border-radius: 24px;
    overflow: hidden;
    box-shadow: 0 24px 64px rgba(0,0,0,0.18);
    gap: 0 !important;
    align-items: stretch !important;
}

div[data-testid="stHorizontalBlock"]
  > div[data-testid="stColumn"]:first-child {
    padding: 0 !important;
    min-height: 560px;
}
div[data-testid="stHorizontalBlock"]
  > div[data-testid="stColumn"]:first-child > div {
    padding: 0 !important;
    height: 100%;
}

div[data-testid="stHorizontalBlock"]
  > div[data-testid="stColumn"]:last-child {
    background: white;
    padding: 40px 44px 32px 44px !important;
}

div[data-testid="stHorizontalBlock"] .stTextInput input,
div[data-testid="stHorizontalBlock"] .stSelectbox > div > div {
    border: 1px solid #d1d5db !important;
    border-radius: 8px !important;
    font-size: 14px !important;
    color: #1f2937 !important;
    background: #f9fafb !important;
}
div[data-testid="stHorizontalBlock"] .stTextInput input:focus {
    border-color: #6bacd4 !important;
    box-shadow: 0 0 0 3px rgba(107,172,212,0.2) !important;
}
div[data-testid="stHorizontalBlock"] .stTextInput label,
div[data-testid="stHorizontalBlock"] .stSelectbox label {
    color: #374151 !important;
    font-size: 13px !important;
}
div[data-testid="stHorizontalBlock"] .stButton button {
    border-radius: 8px !important;
    font-size: 14px !important;
}
div[data-testid="stHorizontalBlock"] p,
div[data-testid="stHorizontalBlock"] label {
    color: #374151 !important;
}
</style>
"""

_ROLE_OPTIONS = {v: k for k, v in ROLE_LABELS.items()}


def show_register():
    st.markdown(_CSS, unsafe_allow_html=True)

    col_left, col_right = st.columns(2, gap="small")

    with col_left:
        st.markdown(
            f'<div style="height:560px;overflow:hidden;line-height:0;">{_SVG}</div>',
            unsafe_allow_html=True,
        )

    with col_right:
        st.markdown(
            "<h2 style='text-align:center;letter-spacing:4px;color:#1f2937;"
            "font-size:22px;font-weight:700;margin-bottom:16px;'>SIGN UP</h2>",
            unsafe_allow_html=True,
        )

        username   = st.text_input("Username",         placeholder="Choose a username",   key="reg_user")
        email      = st.text_input("Email",            placeholder="Your email address",   key="reg_email")
        password   = st.text_input("Password",         placeholder="Create a password",    key="reg_pass",  type="password")
        confirm    = st.text_input("Confirm Password", placeholder="Repeat your password", key="reg_confirm", type="password")
        role_label = st.selectbox(
            "Role",
            list(_ROLE_OPTIONS.keys()),
            key="reg_role",
            help="Data Scientist: analytics pages  |  Farmer: farm assistant  |  Weather Agency: monitoring",
        )

        st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

        if st.button("Create Account", use_container_width=True, key="reg_btn"):
            if not all([username, email, password, confirm]):
                st.warning("Please fill in all fields.")
            elif password != confirm:
                st.error("Passwords do not match.")
            elif len(password) < 4:
                st.error("Password must be at least 4 characters.")
            else:
                role = _ROLE_OPTIONS[role_label]
                ok, msg = register_user(username.strip(), email.strip(), password, role)
                if ok:
                    st.success(f"{msg} You can now log in.")
                    st.session_state.auth_page = "login"
                    st.rerun()
                else:
                    st.error(msg)

        st.markdown(
            "<p style='text-align:center;color:#9ca3af;font-size:13px;margin-top:12px;'>"
            "Already have an account?</p>",
            unsafe_allow_html=True,
        )
        if st.button("Login", use_container_width=True, key="goto_login"):
            st.session_state.auth_page = "login"
            st.rerun()
