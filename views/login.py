import streamlit as st
from services.auth_service import login_user

_SVG = """
<svg viewBox="0 0 420 560" xmlns="http://www.w3.org/2000/svg" style="display:block;width:100%;height:100%;">
  <defs>
    <linearGradient id="lsky" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%"   stop-color="#8fbdd3"/>
      <stop offset="55%"  stop-color="#6aa5c2"/>
      <stop offset="100%" stop-color="#4a8aad"/>
    </linearGradient>
    <linearGradient id="lsea" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%"   stop-color="#2a6e9e"/>
      <stop offset="100%" stop-color="#1a4f72"/>
    </linearGradient>
    <linearGradient id="lwave2" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%"   stop-color="#1d5980"/>
      <stop offset="100%" stop-color="#123d5a"/>
    </linearGradient>
  </defs>
  <rect width="420" height="560" fill="url(#lsky)"/>
  <g opacity="0.28">
    <ellipse cx="205" cy="52" rx="75" ry="30" fill="#4a6a7a"/>
    <ellipse cx="250" cy="40" rx="88" ry="34" fill="#5a7a8a"/>
    <ellipse cx="290" cy="52" rx="62" ry="26" fill="#4a6a7a"/>
  </g>
  <g opacity="0.55">
    <ellipse cx="70"  cy="82"  rx="55" ry="26" fill="white"/>
    <ellipse cx="102" cy="68"  rx="68" ry="31" fill="white"/>
    <ellipse cx="138" cy="78"  rx="46" ry="22" fill="white"/>
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
    <line x1="152" y1="158" x2="144" y2="176"/>
    <line x1="208" y1="172" x2="200" y2="190"/>
    <line x1="238" y1="152" x2="230" y2="170"/>
    <line x1="282" y1="162" x2="274" y2="180"/>
    <line x1="310" y1="142" x2="302" y2="160"/>
    <line x1="340" y1="170" x2="332" y2="188"/>
    <line x1="368" y1="152" x2="360" y2="170"/>
    <line x1="392" y1="178" x2="384" y2="196"/>
  </g>
  <path d="M0,308 C55,280 115,320 175,294 C235,268 295,308 355,282 C380,270 405,278 420,268 L420,560 L0,560 Z" fill="url(#lsea)"/>
  <path d="M0,348 C72,318 155,360 225,330 C285,306 345,342 420,318 L420,560 L0,560 Z" fill="url(#lwave2)" opacity="0.9"/>
  <path d="M0,348 C28,338 58,350 88,340 C108,333 128,345 148,337" stroke="rgba(255,255,255,0.55)" stroke-width="3.5" fill="none" stroke-linecap="round"/>
  <path d="M224,330 C244,320 264,333 284,325 C304,317 320,328 338,320" stroke="rgba(255,255,255,0.45)" stroke-width="2.5" fill="none" stroke-linecap="round"/>
  <path d="M0,392 C82,364 172,398 252,372 C314,354 378,382 420,365 L420,560 L0,560 Z" fill="#165070" opacity="0.88"/>
  <g transform="translate(188,304) rotate(-12)">
    <ellipse cx="0" cy="0" rx="66" ry="13" fill="#c05810"/>
    <ellipse cx="0" cy="-2" rx="60" ry="9"  fill="#e07825" opacity="0.65"/>
    <ellipse cx="0" cy="0"  rx="26" ry="6"  fill="#f09030" opacity="0.45"/>
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
  <path d="M128,318 Q142,303 152,316" stroke="rgba(255,255,255,0.55)" stroke-width="2.5" fill="none"/>
  <path d="M258,308 Q268,293 278,306" stroke="rgba(255,255,255,0.45)" stroke-width="2"   fill="none"/>
  <text x="210" y="488" text-anchor="middle" font-size="17" font-weight="700"
        fill="white" font-family="Arial,sans-serif">Intelligent Rain Monitor</text>
  <text x="210" y="510" text-anchor="middle" font-size="11"
        fill="rgba(255,255,255,0.72)" font-family="Arial,sans-serif">AI-powered weather prediction</text>
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

/* ── outer card ── */
div[data-testid="stHorizontalBlock"].auth-cols {
    background: white;
    border-radius: 24px;
    overflow: hidden;
    box-shadow: 0 24px 64px rgba(0,0,0,0.18);
    gap: 0 !important;
    align-items: stretch !important;
}

/* illustration column */
div[data-testid="stHorizontalBlock"].auth-cols
  > div[data-testid="stColumn"]:first-child {
    padding: 0 !important;
    min-height: 520px;
}
div[data-testid="stHorizontalBlock"].auth-cols
  > div[data-testid="stColumn"]:first-child > div {
    padding: 0 !important;
    height: 100%;
}

/* form column */
div[data-testid="stHorizontalBlock"].auth-cols
  > div[data-testid="stColumn"]:last-child {
    background: white;
    padding: 48px 44px 36px 44px !important;
}

/* inputs */
div[data-testid="stHorizontalBlock"].auth-cols .stTextInput input {
    border: 1px solid #d1d5db !important;
    border-radius: 8px !important;
    padding: 10px 14px !important;
    font-size: 14px !important;
    color: #1f2937 !important;
    background: #f9fafb !important;
}
div[data-testid="stHorizontalBlock"].auth-cols .stTextInput input:focus {
    border-color: #6bacd4 !important;
    box-shadow: 0 0 0 3px rgba(107,172,212,0.2) !important;
}
div[data-testid="stHorizontalBlock"].auth-cols .stTextInput label {
    color: #374151 !important;
    font-size: 13px !important;
}

/* login button */
div[data-testid="stHorizontalBlock"].auth-cols
  > div[data-testid="stColumn"]:last-child > div > div[data-testid="stButton"]:nth-of-type(1) button {
    background: #6bacd4 !important;
    border: none !important;
    border-radius: 8px !important;
    color: white !important;
    font-size: 14px !important;
    font-weight: 600 !important;
    padding: 12px !important;
    letter-spacing: 0.5px;
    width: 100%;
    margin-top: 4px;
}
div[data-testid="stHorizontalBlock"].auth-cols
  > div[data-testid="stColumn"]:last-child > div > div[data-testid="stButton"]:nth-of-type(1) button:hover {
    background: #5499c2 !important;
}

/* sign up button */
div[data-testid="stHorizontalBlock"].auth-cols .stButton button {
    border-radius: 8px !important;
    font-size: 13px !important;
}

/* checkbox */
div[data-testid="stHorizontalBlock"].auth-cols .stCheckbox label {
    color: #6b7280 !important;
    font-size: 13px !important;
}

/* nested columns (remember-me row) — reset card styles */
div[data-testid="stHorizontalBlock"].auth-cols
  div[data-testid="stHorizontalBlock"] {
    background: transparent !important;
    border-radius: 0 !important;
    box-shadow: none !important;
    overflow: visible !important;
}
</style>
"""


def show_login():
    st.markdown(_CSS, unsafe_allow_html=True)

    # Inject a class onto the next stHorizontalBlock via a preceding marker div
    st.markdown(
        '<div style="display:none" class="auth-marker"></div>', unsafe_allow_html=True
    )

    col_left, col_right = st.columns(2, gap="small")

    with col_left:
        st.markdown(
            f'<div style="height:520px;overflow:hidden;line-height:0;">{_SVG}</div>',
            unsafe_allow_html=True,
        )

    with col_right:
        st.markdown(
            "<h2 style='text-align:center;letter-spacing:4px;color:#1f2937;"
            "font-size:22px;font-weight:700;margin-bottom:24px;'>LOGIN</h2>",
            unsafe_allow_html=True,
        )

        username = st.text_input("Email", placeholder="Username or email", key="login_user")
        password = st.text_input("Password", type="password", placeholder="Password", key="login_pass")

        c1, c2 = st.columns([1, 1])
        with c1:
            st.checkbox("Remember me", key="remember_me")
        with c2:
            st.markdown(
                "<div style='text-align:right;padding-top:6px;'>"
                "<a href='#' style='color:#6bacd4;font-size:12px;text-decoration:none;'>Forgot Password?</a>"
                "</div>",
                unsafe_allow_html=True,
            )

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

        if st.button("Login", use_container_width=True, key="login_btn"):
            if not username or not password:
                st.warning("Please enter your username and password.")
            else:
                user = login_user(username.strip(), password)
                if user:
                    st.session_state.authenticated = True
                    st.session_state.user = user
                    st.rerun()
                else:
                    st.error("Invalid username or password.")

        st.markdown(
            "<p style='text-align:center;color:#9ca3af;font-size:13px;margin-top:12px;'>"
            "Don't have an account?</p>",
            unsafe_allow_html=True,
        )
        if st.button("Sign Up", use_container_width=True, key="goto_register"):
            st.session_state.auth_page = "register"
            st.rerun()
