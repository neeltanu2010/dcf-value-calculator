import math
from datetime import datetime
from urllib.parse import quote_plus

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# =====================================================
# FINANCIFY - FREE DCF VALUE CALCULATOR
# Premium tool for Financify blog
# =====================================================

st.set_page_config(
    page_title="Financify DCF Value Calculator",
    page_icon="🐝",
    layout="wide",
    initial_sidebar_state="auto",
)

SURECART_CHECKOUT_URL = "https://financify.blog/buy/financify-tools"
TOOLS_PAGE_URL = "https://financify.blog/tools"
BLOG_URL = "https://financify.blog"

# Mobile-friendly Plotly config
PLOTLY_MOBILE_CONFIG = {"responsive": True, "displayModeBar": False}

# =====================================================
# CSS - Premium Financify Honeycomb Theme
# =====================================================
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif !important;
    }

    .stApp {
        background:
            radial-gradient(circle at 12% 10%, rgba(255, 210, 31, 0.24), transparent 28%),
            radial-gradient(circle at 85% 4%, rgba(255, 184, 0, 0.15), transparent 25%),
            radial-gradient(circle at 88% 82%, rgba(255, 210, 31, 0.18), transparent 28%),
            linear-gradient(135deg, #fffaf0 0%, #fff6d6 45%, #fffdf6 100%);
    }

    .stApp::before {
        content: "";
        position: fixed;
        inset: 0;
        pointer-events: none;
        opacity: 0.12;
        background-image:
          linear-gradient(30deg, #111 12%, transparent 12.5%, transparent 87%, #111 87.5%, #111),
          linear-gradient(150deg, #111 12%, transparent 12.5%, transparent 87%, #111 87.5%, #111),
          linear-gradient(30deg, #111 12%, transparent 12.5%, transparent 87%, #111 87.5%, #111),
          linear-gradient(150deg, #111 12%, transparent 12.5%, transparent 87%, #111 87.5%, #111),
          linear-gradient(60deg, rgba(0,0,0,0.17) 25%, transparent 25.5%, transparent 75%, rgba(0,0,0,0.17) 75%, rgba(0,0,0,0.17));
        background-size: 62px 108px;
        background-position: 0 0, 0 0, 31px 54px, 31px 54px, 0 0;
        z-index: -1;
    }

    .block-container {
        padding-top: 1.3rem;
        padding-bottom: 3rem;
        max-width: 1260px;
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #050505 0%, #181200 62%, #302400 100%);
        border-right: 1px solid rgba(255, 210, 31, 0.30);
    }

    section[data-testid="stSidebar"] * {
        color: #fff6c7 !important;
    }

    section[data-testid="stSidebar"] input,
    section[data-testid="stSidebar"] textarea,
    section[data-testid="stSidebar"] select,
    section[data-testid="stSidebar"] [data-baseweb="select"] * {
        color: #111 !important;
    }

    .hero-card {
        background: linear-gradient(135deg, #050505 0%, #120d00 46%, #3b2d00 100%);
        border: 1px solid rgba(255, 210, 31, 0.60);
        border-radius: 30px;
        padding: 36px 36px 32px 36px;
        box-shadow: 0 26px 90px rgba(0,0,0,0.24);
        position: relative;
        overflow: hidden;
        margin-bottom: 22px;
    }

    .hero-card:before {
        content: "";
        position: absolute;
        inset: -1px;
        background:
            radial-gradient(circle at 86% 18%, rgba(255,210,31,0.36), transparent 22%),
            radial-gradient(circle at 8% 85%, rgba(255,184,0,0.13), transparent 30%);
        pointer-events: none;
    }

    .eyebrow {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: rgba(255, 210, 31, 0.15);
        color: #ffe680;
        border: 1px solid rgba(255, 210, 31, 0.48);
        padding: 8px 14px;
        border-radius: 999px;
        font-size: 0.86rem;
        font-weight: 900;
        letter-spacing: 0.02em;
        position: relative;
    }

    .hero-title {
        color: #ffffff;
        font-size: clamp(2.05rem, 4.2vw, 4.3rem);
        line-height: 1.01;
        font-weight: 950;
        letter-spacing: -0.06em;
        margin-top: 19px;
        margin-bottom: 16px;
        max-width: 900px;
        position: relative;
    }

    .hero-title span {
        color: #FFD21F;
    }

    .hero-subtitle {
        color: #fff2bd;
        font-size: 1.04rem;
        line-height: 1.72;
        max-width: 880px;
        margin-bottom: 20px;
        position: relative;
    }

    .hero-pills {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        margin-top: 20px;
        position: relative;
    }

    .pill {
        background: rgba(255, 255, 255, 0.08);
        color: #fff7cf;
        border: 1px solid rgba(255, 210, 31, 0.30);
        border-radius: 999px;
        padding: 9px 13px;
        font-size: 0.88rem;
        font-weight: 800;
    }

    .glass-card {
        background: rgba(255, 255, 255, 0.86);
        border: 1px solid rgba(17, 17, 17, 0.08);
        border-radius: 24px;
        padding: 22px;
        box-shadow: 0 14px 44px rgba(20, 14, 0, 0.085);
        backdrop-filter: blur(12px);
        margin-bottom: 18px;
    }

    .metric-card {
        background: linear-gradient(180deg, #ffffff 0%, #fff7d1 100%);
        border: 1px solid rgba(17, 17, 17, 0.08);
        border-radius: 23px;
        padding: 20px;
        box-shadow: 0 12px 30px rgba(17, 17, 17, 0.08);
        min-height: 145px;
        position: relative;
        overflow: hidden;
    }

    .metric-card:after {
        content: "";
        position: absolute;
        width: 80px;
        height: 80px;
        right: -22px;
        top: -22px;
        border-radius: 50%;
        background: rgba(255, 210, 31, 0.20);
    }

    .metric-label {
        color: #5c4a00;
        font-size: 0.82rem;
        font-weight: 950;
        text-transform: uppercase;
        letter-spacing: 0.055em;
        margin-bottom: 8px;
    }

    .metric-value {
        color: #070707;
        font-size: 1.64rem;
        font-weight: 950;
        letter-spacing: -0.04em;
        margin-bottom: 7px;
        word-break: break-word;
    }

    .metric-help {
        color: #5c5c5c;
        font-size: 0.89rem;
        line-height: 1.46;
    }

    .section-title {
        font-size: 1.46rem;
        font-weight: 950;
        color: #111;
        letter-spacing: -0.037em;
        margin-bottom: 8px;
    }

    .section-subtitle {
        color: #5b5b5b;
        font-size: 0.97rem;
        line-height: 1.56;
        margin-bottom: 16px;
    }

    .verdict-box {
        border-radius: 28px;
        padding: 25px;
        color: #fffdf0;
        border: 1px solid rgba(255, 210, 31, 0.48);
        box-shadow: 0 18px 46px rgba(0,0,0,0.22);
        background: linear-gradient(135deg, #070707 0%, #241a00 60%, #544100 100%);
        margin-bottom: 18px;
    }

    .verdict-title {
        font-size: 1.46rem;
        font-weight: 950;
        color: #FFD21F;
        margin-bottom: 9px;
        letter-spacing: -0.02em;
    }

    .verdict-text {
        color: #fff7cf;
        font-size: 1rem;
        line-height: 1.65;
    }

    .mini-badge {
        display: inline-block;
        background: #FFD21F;
        color: #111;
        padding: 7px 10px;
        border-radius: 999px;
        font-size: 0.78rem;
        font-weight: 950;
        margin-right: 8px;
        margin-bottom: 8px;
    }

    .danger-badge {
        display: inline-block;
        background: #111;
        color: #FFD21F;
        padding: 7px 10px;
        border: 1px solid rgba(255, 210, 31, 0.45);
        border-radius: 999px;
        font-size: 0.78rem;
        font-weight: 950;
        margin-right: 8px;
        margin-bottom: 8px;
    }

    .warning-box {
        background: #fff2bd;
        border-left: 6px solid #FFD21F;
        border-radius: 18px;
        padding: 16px 18px;
        color: #2f2600;
        line-height: 1.58;
        font-weight: 650;
        margin-bottom: 18px;
    }

    .cta-card {
        background: linear-gradient(135deg, #FFD21F 0%, #ffb800 100%);
        color: #111;
        border-radius: 28px;
        padding: 26px;
        border: 1px solid rgba(0,0,0,0.10);
        box-shadow: 0 18px 44px rgba(122, 91, 0, 0.20);
        margin-top: 20px;
    }

    .cta-card h3 {
        color: #111;
        font-size: 1.58rem;
        font-weight: 950;
        margin-bottom: 8px;
        letter-spacing: -0.038em;
    }

    .cta-card p {
        color: #241b00;
        line-height: 1.58;
        font-weight: 650;
    }

    .stButton > button, .stDownloadButton > button {
        border-radius: 999px !important;
        border: 1px solid rgba(17,17,17,0.13) !important;
        background: linear-gradient(135deg, #111 0%, #2a2100 100%) !important;
        color: #FFD21F !important;
        font-weight: 950 !important;
        padding: 0.74rem 1.1rem !important;
        box-shadow: 0 8px 24px rgba(0,0,0,0.18) !important;
    }

    div[data-testid="stMetric"] {
        background: rgba(255,255,255,0.80);
        border: 1px solid rgba(0,0,0,0.08);
        border-radius: 20px;
        padding: 14px 16px;
        box-shadow: 0 8px 22px rgba(0,0,0,0.06);
    }

    div[data-testid="stTabs"] button {
        font-weight: 900;
    }

    .footer-note {
        color: #6b5d27;
        text-align: center;
        font-size: 0.86rem;
        margin-top: 24px;
    }

    @media (max-width: 768px) {
        .hero-card { padding: 27px 20px; border-radius: 22px; }
        .glass-card { padding: 18px; border-radius: 20px; }
        .metric-value { font-size: 1.34rem; }
        .metric-card { min-height: 132px; }
    }


    /* =====================================================
       FINANCIFY MOBILE + READABILITY PATCH
       Keeps the original theme, fixes mobile overflow and invisible text.
       ===================================================== */
    :root { color-scheme: light; }

    html, body, .stApp, [data-testid="stAppViewContainer"] {
        width: 100% !important;
        max-width: 100% !important;
        overflow-x: hidden !important;
        -webkit-text-size-adjust: 100%;
        text-rendering: optimizeLegibility;
    }

    *, *::before, *::after {
        box-sizing: border-box !important;
    }

    .main .block-container,
    [data-testid="stAppViewContainer"] .block-container {
        width: 100% !important;
        max-width: min(1260px, 100%) !important;
        padding-left: clamp(0.90rem, 3.2vw, 2.00rem) !important;
        padding-right: clamp(0.90rem, 3.2vw, 2.00rem) !important;
    }

    .block-container p,
    .block-container li,
    .block-container h1,
    .block-container h2,
    .block-container h3,
    .block-container h4,
    .block-container h5,
    .block-container h6,
    .block-container span,
    .hero-title,
    .hero-subtitle,
    .section-title,
    .section-subtitle,
    .metric-label,
    .metric-value,
    .metric-help,
    .verdict-title,
    .verdict-text,
    .light-text,
    .pill,
    .mini-badge,
    .soft-badge {
        overflow-wrap: anywhere !important;
        word-break: normal !important;
    }

    .hero-card,
    .glass-card,
    .dark-card,
    .metric-card,
    .verdict-box,
    .warning-box,
    .danger-box,
    .cta-card {
        max-width: 100% !important;
        isolation: isolate;
    }

    .hero-card > *,
    .dark-card > *,
    .verdict-box > * {
        position: relative;
        z-index: 1;
    }

    .glass-card,
    .metric-card,
    .warning-box,
    .danger-box,
    .cta-card {
        color: #111111 !important;
    }

    .glass-card p,
    .glass-card li,
    .glass-card span,
    .metric-card p,
    .metric-card li,
    .warning-box p,
    .warning-box li,
    .danger-box p,
    .danger-box li,
    .cta-card p,
    .cta-card li {
        opacity: 1 !important;
    }

    .dark-card,
    .dark-card p,
    .dark-card li,
    .dark-card span,
    .verdict-box,
    .verdict-box p,
    .verdict-box li,
    .verdict-box span,
    .hero-card,
    .hero-card p,
    .hero-card li,
    .hero-card span {
        color: #fff7cf !important;
        -webkit-text-fill-color: #fff7cf !important;
    }

    .hero-title,
    .hero-title span,
    .verdict-title,
    .section-title-light {
        -webkit-text-fill-color: currentColor !important;
    }

    .metric-label { color: #5c4a00 !important; }
    .metric-value { color: #070707 !important; }
    .metric-help { color: #4c4c4c !important; }
    .section-title { color: #111111 !important; }
    .section-subtitle { color: #4d4d4d !important; }
    .warning-box, .warning-box * { color: #2f2600 !important; -webkit-text-fill-color: #2f2600 !important; }
    .danger-box, .danger-box * { color: #3b120a !important; -webkit-text-fill-color: #3b120a !important; }
    .cta-card, .cta-card * { color: #111111 !important; -webkit-text-fill-color: #111111 !important; }

    /* Sidebar: readable labels on dark background, readable input text on light fields.
       Width is left to Streamlit default so desktop stays normal and mobile fully collapses. */
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] h4,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] [data-testid="stWidgetLabel"] *,
    section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] * {
        color: #fff8d8 !important;
        -webkit-text-fill-color: #fff8d8 !important;
        opacity: 1 !important;
    }

    section[data-testid="stSidebar"] input,
    section[data-testid="stSidebar"] textarea,
    section[data-testid="stSidebar"] [data-baseweb="input"] input,
    section[data-testid="stSidebar"] [data-baseweb="textarea"] textarea,
    section[data-testid="stSidebar"] [data-testid="stNumberInput"] input {
        background: #fffaf0 !important;
        color: #111111 !important;
        -webkit-text-fill-color: #111111 !important;
        caret-color: #111111 !important;
        border: 1px solid rgba(255, 210, 31, 0.50) !important;
        border-radius: 12px !important;
        font-size: 16px !important;
        min-height: 44px !important;
    }

    section[data-testid="stSidebar"] [data-baseweb="select"] > div,
    section[data-testid="stSidebar"] [data-baseweb="select"] div[role="button"] {
        background: #fffaf0 !important;
        color: #111111 !important;
        border-color: rgba(255, 210, 31, 0.50) !important;
        border-radius: 12px !important;
        min-height: 44px !important;
    }

    section[data-testid="stSidebar"] [data-baseweb="select"] *,
    div[data-baseweb="popover"] *,
    div[data-baseweb="menu"] * {
        color: #111111 !important;
        -webkit-text-fill-color: #111111 !important;
    }

    div[data-baseweb="popover"] [role="option"],
    div[data-baseweb="menu"] [role="option"] {
        background: #fffaf0 !important;
    }

    .stTextInput input,
    .stNumberInput input,
    .stTextArea textarea,
    .stSelectbox [data-baseweb="select"] > div {
        font-size: 16px !important;
    }

    /* Tables and Plotly should scroll/resize instead of cutting text on phones. */
    div[data-testid="stDataFrame"],
    div[data-testid="stTable"],
    .stDataFrame,
    .stTable {
        max-width: 100% !important;
        overflow-x: auto !important;
        -webkit-overflow-scrolling: touch !important;
        border-radius: 16px !important;
    }

    div[data-testid="stDataFrame"] * {
        font-size: clamp(0.74rem, 2.9vw, 0.92rem) !important;
    }

    .js-plotly-plot,
    .plotly,
    .plot-container,
    div[data-testid="stPlotlyChart"] {
        width: 100% !important;
        max-width: 100% !important;
    }

    div[data-testid="stPlotlyChart"] {
        overflow-x: auto !important;
        -webkit-overflow-scrolling: touch !important;
    }

    div[data-testid="stTabs"] [role="tablist"] {
        overflow-x: auto !important;
        overflow-y: hidden !important;
        white-space: nowrap !important;
        gap: 0.35rem !important;
        scrollbar-width: none;
    }

    div[data-testid="stTabs"] [role="tablist"]::-webkit-scrollbar {
        display: none;
    }

    div[data-testid="stTabs"] button,
    div[data-testid="stTabs"] button p {
        white-space: nowrap !important;
        font-size: clamp(0.78rem, 3.1vw, 0.94rem) !important;
        line-height: 1.2 !important;
    }

    @media (max-width: 768px) {
        .block-container {
            padding-top: 0.75rem !important;
            padding-bottom: 2rem !important;
        }

        .hero-card {
            padding: 1.25rem 1rem !important;
            border-radius: 21px !important;
            margin-bottom: 1rem !important;
        }

        .hero-title {
            font-size: clamp(1.72rem, 9vw, 2.35rem) !important;
            letter-spacing: -0.038em !important;
            line-height: 1.07 !important;
            margin-top: 0.95rem !important;
            margin-bottom: 0.75rem !important;
        }

        .hero-subtitle {
            font-size: 0.96rem !important;
            line-height: 1.55 !important;
            margin-bottom: 0.85rem !important;
        }

        .hero-pills {
            gap: 0.45rem !important;
            margin-top: 0.85rem !important;
        }

        .pill,
        .mini-badge,
        .soft-badge {
            font-size: 0.76rem !important;
            line-height: 1.2 !important;
            padding: 0.45rem 0.62rem !important;
        }

        .glass-card,
        .dark-card,
        .metric-card,
        .verdict-box,
        .warning-box,
        .danger-box,
        .cta-card {
            padding: 1rem !important;
            border-radius: 18px !important;
            margin-bottom: 0.95rem !important;
        }

        .metric-card {
            min-height: auto !important;
        }

        .metric-label {
            font-size: 0.73rem !important;
            line-height: 1.18 !important;
            letter-spacing: 0.045em !important;
        }

        .metric-value {
            font-size: clamp(1.15rem, 6.2vw, 1.55rem) !important;
            line-height: 1.13 !important;
        }

        .metric-help,
        .section-subtitle,
        .verdict-text,
        .light-text {
            font-size: 0.91rem !important;
            line-height: 1.50 !important;
        }

        .section-title,
        .section-title-light,
        .verdict-title {
            font-size: 1.18rem !important;
            line-height: 1.20 !important;
            letter-spacing: -0.025em !important;
        }

        [data-testid="column"] {
            width: 100% !important;
            flex: 1 1 100% !important;
            min-width: 100% !important;
            margin-bottom: 0.75rem !important;
        }

        .stButton > button,
        .stDownloadButton > button,
        section[data-testid="stSidebar"] .stButton > button {
            width: 100% !important;
            min-height: 46px !important;
            padding: 0.75rem 0.95rem !important;
            white-space: normal !important;
            line-height: 1.2 !important;
        }

        div[data-testid="stMetric"] {
            padding: 0.85rem 0.9rem !important;
        }

        div[data-testid="stMetric"] label,
        div[data-testid="stMetric"] [data-testid="stMetricLabel"] * {
            font-size: 0.76rem !important;
            white-space: normal !important;
        }

        div[data-testid="stMetricValue"] {
            font-size: 1.25rem !important;
            line-height: 1.15 !important;
            overflow-wrap: anywhere !important;
        }

        div[data-testid="stPlotlyChart"] {
            border-radius: 16px !important;
        }

        iframe,
        img,
        video,
        canvas,
        svg {
            max-width: 100% !important;
        }
    }

    @media (max-width: 420px) {
        .hero-title {
            font-size: clamp(1.58rem, 10vw, 2.05rem) !important;
        }

        .eyebrow {
            font-size: 0.74rem !important;
            padding: 0.43rem 0.58rem !important;
        }

        .metric-value {
            font-size: clamp(1.05rem, 7vw, 1.35rem) !important;
        }

        .block-container {
            padding-left: 0.72rem !important;
            padding-right: 0.72rem !important;
        }
    }

    </style>
    """,
    unsafe_allow_html=True,
)

# =====================================================
# Helpers
# =====================================================
def fmt_money(value, symbol="₹"):
    try:
        value = float(value)
        if not np.isfinite(value):
            return "—"
        sign = "-" if value < 0 else ""
        value_abs = abs(value)
        if value_abs >= 1e7:
            return f"{sign}{symbol}{value_abs/1e7:,.2f} Cr"
        if value_abs >= 1e5:
            return f"{sign}{symbol}{value_abs/1e5:,.2f} L"
        return f"{sign}{symbol}{value_abs:,.2f}"
    except Exception:
        return "—"


def fmt_cr(value, symbol="₹"):
    try:
        value = float(value)
        if not np.isfinite(value):
            return "—"
        return f"{symbol}{value:,.2f} Cr"
    except Exception:
        return "—"


def fmt_pct(value):
    try:
        value = float(value)
        if not np.isfinite(value):
            return "—"
        return f"{value*100:.2f}%"
    except Exception:
        return "—"


def safe_div(a, b):
    try:
        if b == 0 or not np.isfinite(a) or not np.isfinite(b):
            return np.nan
        return a / b
    except Exception:
        return np.nan


def growth_path(start_growth, stable_growth, years, fade_start_year=6):
    """Build a staged growth path that gradually fades toward stable growth."""
    rates = []
    for year in range(1, years + 1):
        if year < fade_start_year:
            rates.append(start_growth)
        else:
            fade_years = max(1, years - fade_start_year + 1)
            progress = (year - fade_start_year + 1) / fade_years
            g = start_growth + (stable_growth - start_growth) * progress
            rates.append(g)
    return rates


def calculate_dcf(
    latest_fcf_cr,
    shares_cr,
    cash_cr,
    debt_cr,
    start_growth,
    stable_growth,
    discount_rate,
    years,
    terminal_method,
    exit_multiple,
    margin_of_safety,
):
    """DCF in crore terms. Per-share value works because equity value in Cr / shares in Cr = rupees per share."""
    if latest_fcf_cr <= 0 or shares_cr <= 0 or years <= 0 or discount_rate <= 0:
        return None

    rates = growth_path(start_growth, stable_growth, years)
    rows = []
    fcf = latest_fcf_cr
    pv_fcf_total = 0.0

    for year, g in enumerate(rates, start=1):
        fcf = fcf * (1 + g)
        discount_factor = (1 + discount_rate) ** year
        pv_fcf = fcf / discount_factor
        pv_fcf_total += pv_fcf
        rows.append({
            "Year": year,
            "Growth Rate": g,
            "Projected FCF Cr": fcf,
            "Discount Factor": discount_factor,
            "PV of FCF Cr": pv_fcf,
        })

    final_fcf = fcf

    if terminal_method == "Gordon Growth Model":
        if stable_growth >= discount_rate:
            terminal_value = np.nan
        else:
            terminal_value = final_fcf * (1 + stable_growth) / (discount_rate - stable_growth)
    else:
        terminal_value = final_fcf * exit_multiple

    pv_terminal_value = terminal_value / ((1 + discount_rate) ** years) if np.isfinite(terminal_value) else np.nan
    enterprise_value = pv_fcf_total + pv_terminal_value if np.isfinite(pv_terminal_value) else np.nan
    net_cash = cash_cr - debt_cr
    equity_value = enterprise_value + net_cash if np.isfinite(enterprise_value) else np.nan
    fair_value_per_share = equity_value / shares_cr if shares_cr > 0 and np.isfinite(equity_value) else np.nan
    mos_price = fair_value_per_share * (1 - margin_of_safety) if np.isfinite(fair_value_per_share) else np.nan
    terminal_dependency = safe_div(pv_terminal_value, enterprise_value)

    return {
        "projection_df": pd.DataFrame(rows),
        "pv_fcf_total": pv_fcf_total,
        "terminal_value": terminal_value,
        "pv_terminal_value": pv_terminal_value,
        "enterprise_value": enterprise_value,
        "net_cash": net_cash,
        "equity_value": equity_value,
        "fair_value_per_share": fair_value_per_share,
        "mos_price": mos_price,
        "terminal_dependency": terminal_dependency,
        "final_fcf": final_fcf,
        "rates": rates,
    }


def scenario_calculations(
    latest_fcf_cr,
    shares_cr,
    cash_cr,
    debt_cr,
    start_growth,
    stable_growth,
    discount_rate,
    years,
    terminal_method,
    exit_multiple,
    margin_of_safety,
):
    configs = [
        {
            "Case": "Bear",
            "Start Growth": start_growth * 0.55,
            "Stable Growth": max(-0.05, stable_growth - 0.01),
            "Discount Rate": discount_rate + 0.02,
            "Exit Multiple": max(3.0, exit_multiple * 0.80),
        },
        {
            "Case": "Base",
            "Start Growth": start_growth,
            "Stable Growth": stable_growth,
            "Discount Rate": discount_rate,
            "Exit Multiple": exit_multiple,
        },
        {
            "Case": "Bull",
            "Start Growth": start_growth * 1.22,
            "Stable Growth": min(discount_rate - 0.015, stable_growth + 0.005),
            "Discount Rate": max(0.04, discount_rate - 0.01),
            "Exit Multiple": exit_multiple * 1.15,
        },
    ]

    rows = []
    detailed = {}
    for cfg in configs:
        calc = calculate_dcf(
            latest_fcf_cr=latest_fcf_cr,
            shares_cr=shares_cr,
            cash_cr=cash_cr,
            debt_cr=debt_cr,
            start_growth=cfg["Start Growth"],
            stable_growth=cfg["Stable Growth"],
            discount_rate=cfg["Discount Rate"],
            years=years,
            terminal_method=terminal_method,
            exit_multiple=cfg["Exit Multiple"],
            margin_of_safety=margin_of_safety,
        )
        detailed[cfg["Case"]] = calc
        rows.append({
            "Case": cfg["Case"],
            "Start Growth": cfg["Start Growth"],
            "Stable Growth": cfg["Stable Growth"],
            "Discount Rate": cfg["Discount Rate"],
            "Exit Multiple": cfg["Exit Multiple"],
            "PV FCF Cr": calc["pv_fcf_total"] if calc else np.nan,
            "PV Terminal Cr": calc["pv_terminal_value"] if calc else np.nan,
            "Enterprise Value Cr": calc["enterprise_value"] if calc else np.nan,
            "Equity Value Cr": calc["equity_value"] if calc else np.nan,
            "Fair Value/Share": calc["fair_value_per_share"] if calc else np.nan,
            "MOS Price": calc["mos_price"] if calc else np.nan,
            "Terminal Dependency": calc["terminal_dependency"] if calc else np.nan,
        })
    return pd.DataFrame(rows), detailed


def quality_score(start_growth, stable_growth, discount_rate, years, terminal_dependency, margin_of_safety, net_debt_to_fcf, terminal_method):
    score = 0
    notes = []

    spread = discount_rate - stable_growth
    if spread >= 0.07:
        score += 18
        notes.append("Discount rate has a healthy spread over stable growth.")
    elif spread >= 0.04:
        score += 13
        notes.append("Discount rate spread is acceptable, but terminal value needs caution.")
    elif spread > 0:
        score += 6
        notes.append("Discount rate is very close to stable growth. This can inflate terminal value.")
    else:
        score += 0
        notes.append("Stable growth must be lower than discount rate for Gordon Growth DCF.")

    if start_growth <= 0.08:
        score += 17
        notes.append("Starting growth assumption looks conservative.")
    elif start_growth <= 0.15:
        score += 12
        notes.append("Starting growth is reasonable if the company has durable quality.")
    elif start_growth <= 0.25:
        score += 6
        notes.append("Starting growth is aggressive. Verify moat, reinvestment runway and competition.")
    else:
        score += 2
        notes.append("Starting growth is very aggressive. The honey may be mixed with hope.")

    if np.isfinite(terminal_dependency):
        if terminal_dependency <= 0.55:
            score += 18
            notes.append("Terminal value dependency is controlled.")
        elif terminal_dependency <= 0.70:
            score += 12
            notes.append("Terminal value dependency is normal for DCF, but sensitivity matters.")
        elif terminal_dependency <= 0.82:
            score += 6
            notes.append("High terminal value dependency. Most value is coming from the far future.")
        else:
            score += 2
            notes.append("Very high terminal value dependency. This DCF is fragile.")
    else:
        notes.append("Terminal dependency could not be calculated because terminal value is invalid.")

    if margin_of_safety >= 0.30:
        score += 17
        notes.append("Margin of safety is strong.")
    elif margin_of_safety >= 0.20:
        score += 12
        notes.append("Margin of safety is decent.")
    elif margin_of_safety >= 0.10:
        score += 6
        notes.append("Margin of safety is thin for a DCF estimate.")
    else:
        score += 2
        notes.append("Margin of safety is too low. DCF assumptions are never that clean.")

    if years >= 10:
        score += 10
        notes.append("Projection period is long enough to model compounding and fade.")
    elif years >= 7:
        score += 7
        notes.append("Projection period is acceptable.")
    else:
        score += 3
        notes.append("Short projection period can make terminal value dominate.")

    if np.isfinite(net_debt_to_fcf):
        if net_debt_to_fcf <= 0:
            score += 10
            notes.append("Net cash position improves valuation comfort.")
        elif net_debt_to_fcf <= 3:
            score += 7
            notes.append("Net debt looks manageable versus FCF.")
        elif net_debt_to_fcf <= 6:
            score += 3
            notes.append("Net debt is meaningful. Check interest coverage and refinancing risk.")
        else:
            score += 1
            notes.append("High net debt can destroy DCF comfort.")

    if terminal_method == "Gordon Growth Model":
        score += 10
        notes.append("Gordon model is suitable for stable businesses but very sensitive to terminal growth.")
    else:
        score += 8
        notes.append("Exit multiple method is simple but depends on market mood at the exit year.")

    return min(int(score), 100), notes


def get_verdict(current_price, fair_value, mos_price, bear_value, bull_value, score, terminal_dependency):
    if not np.isfinite(fair_value):
        return "DCF Needs Cleaner Inputs 🛠️", "The model could not calculate a reliable value. Check FCF, shares, discount rate and terminal assumptions."

    if current_price <= 0:
        return "DCF Value Estimated 🍯", "Add current market price to compare fair value, margin of safety and implied growth."

    if current_price <= mos_price and score >= 65:
        return "Honey Discount Zone 🐝", "Price is below margin-of-safety value and assumptions look reasonably controlled. Still verify business quality before taking any decision."
    if current_price <= mos_price:
        return "Cheap, But Check Assumptions ⚠️", "Price is below margin-of-safety value, but the assumptions need more caution. Cheap output is not equal to safe investment."
    if current_price <= fair_value:
        return "Fair Value Zone ✅", "Price is below base DCF value, but the margin of safety is not strong. Watch assumptions carefully."
    if np.isfinite(bull_value) and current_price <= bull_value:
        return "Bull Case Required 🐂", "The price needs optimistic assumptions to look attractive. Growth, moat and cash-flow quality must be strong."
    if np.isfinite(terminal_dependency) and terminal_dependency > 0.80:
        return "Hope-Heavy DCF 🫧", "Price looks demanding and the DCF depends heavily on terminal value. This is where assumptions can become honey-coated imagination."
    return "Overvaluation Risk Zone 🚧", "The current price is above even the bullish DCF estimate. That does not mean sell, but expectations appear high."


def reverse_dcf_growth(
    target_price,
    latest_fcf_cr,
    shares_cr,
    cash_cr,
    debt_cr,
    stable_growth,
    discount_rate,
    years,
    terminal_method,
    exit_multiple,
):
    if target_price <= 0 or latest_fcf_cr <= 0 or shares_cr <= 0:
        return np.nan

    def price_for_growth(g):
        calc = calculate_dcf(
            latest_fcf_cr=latest_fcf_cr,
            shares_cr=shares_cr,
            cash_cr=cash_cr,
            debt_cr=debt_cr,
            start_growth=g,
            stable_growth=stable_growth,
            discount_rate=discount_rate,
            years=years,
            terminal_method=terminal_method,
            exit_multiple=exit_multiple,
            margin_of_safety=0,
        )
        return calc["fair_value_per_share"] if calc else np.nan

    low, high = -0.50, 0.60
    p_low = price_for_growth(low)
    p_high = price_for_growth(high)

    if not np.isfinite(p_low) or not np.isfinite(p_high):
        return np.nan
    if target_price < p_low:
        return low
    if target_price > p_high:
        return high

    for _ in range(90):
        mid = (low + high) / 2
        p_mid = price_for_growth(mid)
        if not np.isfinite(p_mid):
            return np.nan
        if p_mid < target_price:
            low = mid
        else:
            high = mid
    return (low + high) / 2


def make_breakdown_chart(base_calc, currency_symbol):
    labels = ["PV of Explicit FCF", "PV of Terminal Value", "Net Cash / Debt Adjustment"]
    values = [
        base_calc["pv_fcf_total"],
        base_calc["pv_terminal_value"],
        base_calc["net_cash"],
    ]
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=labels,
        y=values,
        text=[fmt_cr(v, currency_symbol) for v in values],
        textposition="outside",
        hovertemplate="%{x}<br>%{text}<extra></extra>",
    ))
    fig.update_layout(
        title="DCF Value Breakdown",
        template="plotly_white",
        height=420,
        margin=dict(l=20, r=20, t=60, b=60),
        yaxis_title="Value in Cr",
        font=dict(family="Inter", size=13),
        plot_bgcolor="rgba(255,255,255,0)",
        paper_bgcolor="rgba(255,255,255,0)",
    )
    return fig


def make_projection_chart(projection_df, currency_symbol):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=projection_df["Year"],
        y=projection_df["Projected FCF Cr"],
        mode="lines+markers",
        name="Projected FCF",
        hovertemplate="Year %{x}<br>FCF: %{y:,.2f} Cr<extra></extra>",
    ))
    fig.add_trace(go.Bar(
        x=projection_df["Year"],
        y=projection_df["PV of FCF Cr"],
        name="PV of FCF",
        opacity=0.52,
        hovertemplate="Year %{x}<br>PV FCF: %{y:,.2f} Cr<extra></extra>",
    ))
    fig.update_layout(
        title="FCF Projection vs Present Value",
        template="plotly_white",
        height=430,
        margin=dict(l=20, r=20, t=60, b=50),
        xaxis_title="Projection year",
        yaxis_title=f"{currency_symbol} Cr",
        font=dict(family="Inter", size=13),
        plot_bgcolor="rgba(255,255,255,0)",
        paper_bgcolor="rgba(255,255,255,0)",
    )
    return fig


def make_sensitivity_heatmap(
    latest_fcf_cr,
    shares_cr,
    cash_cr,
    debt_cr,
    start_growth,
    stable_growth,
    discount_rate,
    years,
    terminal_method,
    exit_multiple,
    currency_symbol,
):
    growth_points = np.array([start_growth - 0.04, start_growth - 0.02, start_growth, start_growth + 0.02, start_growth + 0.04])
    discount_points = np.array([discount_rate - 0.025, discount_rate - 0.0125, discount_rate, discount_rate + 0.0125, discount_rate + 0.025])
    discount_points = np.maximum(discount_points, 0.02)

    z = []
    for d in discount_points:
        row = []
        for g in growth_points:
            stable = min(stable_growth, d - 0.01) if terminal_method == "Gordon Growth Model" else stable_growth
            calc = calculate_dcf(
                latest_fcf_cr=latest_fcf_cr,
                shares_cr=shares_cr,
                cash_cr=cash_cr,
                debt_cr=debt_cr,
                start_growth=g,
                stable_growth=stable,
                discount_rate=d,
                years=years,
                terminal_method=terminal_method,
                exit_multiple=exit_multiple,
                margin_of_safety=0,
            )
            row.append(calc["fair_value_per_share"] if calc else np.nan)
        z.append(row)

    fig = go.Figure(data=go.Heatmap(
        z=z,
        x=[f"{g*100:.1f}%" for g in growth_points],
        y=[f"{d*100:.1f}%" for d in discount_points],
        text=[[fmt_money(v, currency_symbol) for v in row] for row in z],
        texttemplate="%{text}",
        hovertemplate="Start Growth: %{x}<br>Discount Rate: %{y}<br>Value: %{text}<extra></extra>",
    ))
    fig.update_layout(
        title="Sensitivity: Start Growth vs Discount Rate",
        xaxis_title="Start growth",
        yaxis_title="Discount rate",
        template="plotly_white",
        height=430,
        margin=dict(l=20, r=20, t=60, b=50),
        font=dict(family="Inter", size=13),
        plot_bgcolor="rgba(255,255,255,0)",
        paper_bgcolor="rgba(255,255,255,0)",
    )
    return fig


def build_report(
    company,
    currency_symbol,
    latest_fcf_cr,
    shares_cr,
    cash_cr,
    debt_cr,
    current_price,
    start_growth,
    stable_growth,
    discount_rate,
    years,
    terminal_method,
    exit_multiple,
    margin_of_safety,
    scenario_df,
    verdict_title,
    verdict_text,
    score,
    notes,
    implied_growth,
    terminal_dependency,
):
    generated = datetime.now().strftime("%d %b %Y, %I:%M %p")
    display = scenario_df.copy()
    for col in ["Start Growth", "Stable Growth", "Discount Rate", "Terminal Dependency"]:
        display[col] = display[col].map(fmt_pct)
    display["Exit Multiple"] = display["Exit Multiple"].map(lambda x: f"{x:.2f}x" if np.isfinite(x) else "—")
    for col in ["PV FCF Cr", "PV Terminal Cr", "Enterprise Value Cr", "Equity Value Cr"]:
        display[col] = display[col].map(lambda x: fmt_cr(x, currency_symbol))
    for col in ["Fair Value/Share", "MOS Price"]:
        display[col] = display[col].map(lambda x: fmt_money(x, currency_symbol))

    return f"""
FINANCIFY DCF VALUE MINI REPORT
Generated: {generated}

Company/Stock: {company or 'Not specified'}
Latest Free Cash Flow: {fmt_cr(latest_fcf_cr, currency_symbol)}
Shares Outstanding: {shares_cr:,.2f} Cr
Cash & Investments: {fmt_cr(cash_cr, currency_symbol)}
Total Debt: {fmt_cr(debt_cr, currency_symbol)}
Current Price: {fmt_money(current_price, currency_symbol) if current_price > 0 else 'Not entered'}

DCF ASSUMPTIONS
Start Growth: {fmt_pct(start_growth)}
Stable Growth: {fmt_pct(stable_growth)}
Discount Rate: {fmt_pct(discount_rate)}
Projection Period: {years} years
Terminal Method: {terminal_method}
Exit Multiple: {exit_multiple:.2f}x
Margin of Safety: {fmt_pct(margin_of_safety)}

VALUATION CASES
{display.to_string(index=False)}

FINANCIFY DCF VERDICT
{verdict_title}
{verdict_text}

Reverse DCF Implied Start Growth: {fmt_pct(implied_growth)}
Assumption Quality Score: {score}/100
Terminal Value Dependency: {fmt_pct(terminal_dependency)}

ASSUMPTION NOTES
- """ + "\n- ".join(notes) + """

Educational disclaimer: This DCF calculator is for learning and research only. It is not investment advice, a stock recommendation, or a buy/sell signal. Please do your own research or consult a SEBI-registered investment adviser before making decisions.
"""


def build_seo_draft(company, currency_symbol, latest_fcf_cr, current_price, base_value, mos_price, start_growth, stable_growth, discount_rate, terminal_method, terminal_dependency):
    stock_name = company.strip() if company.strip() else "This Stock"
    title = f"{stock_name} DCF Value Calculator: Estimate Fair Value Using Free Cash Flow"
    meta = f"Use this free DCF value calculator to estimate {stock_name}'s fair value using free cash flow, growth, discount rate, terminal value and margin of safety."
    excerpt = f"Estimate {stock_name}'s DCF value with bear, base and bull cases. Understand margin of safety, terminal value dependency and reverse implied growth."
    article = f"""
# {title}

A DCF calculator estimates what a business may be worth today based on the cash it can generate in the future. It sounds serious because it is serious, but it is not magic. A DCF is only as good as the assumptions used inside it.

This free Financify DCF calculator uses free cash flow, projected growth, discount rate, terminal value and margin of safety to estimate a possible fair value range.

## Inputs Used

- Latest free cash flow: {fmt_cr(latest_fcf_cr, currency_symbol)}
- Current price: {fmt_money(current_price, currency_symbol) if current_price > 0 else 'Not entered'}
- Start growth assumption: {fmt_pct(start_growth)}
- Stable growth assumption: {fmt_pct(stable_growth)}
- Discount rate: {fmt_pct(discount_rate)}
- Terminal method: {terminal_method}

## Estimated DCF Value

Based on these assumptions, the base DCF fair value is around {fmt_money(base_value, currency_symbol)} per share. After applying margin of safety, the preferred safety price is around {fmt_money(mos_price, currency_symbol)} per share.

## Why Terminal Value Matters

In many DCF models, a large part of value comes from terminal value. In this calculation, terminal value dependency is around {fmt_pct(terminal_dependency)}. If this number is too high, the model depends heavily on the far future.

## How to Use This Result

Do not treat DCF value as a perfect target price. Treat it as a range. Change growth, discount rate and terminal assumptions to see how sensitive the result is.

## What to Check Next

Before trusting any DCF result, check whether the business has durable quality:

- Low or manageable debt
- Consistent free cash flow
- Strong ROE and ROCE
- Stable or improving margins
- Honest accounting quality
- Reasonable valuation compared with business quality

You can use Financify's advanced tools to check these factors faster.

## Disclaimer

This calculator and article are for educational purposes only. They are not investment advice, stock recommendations or buy/sell signals. Please do your own research or consult a SEBI-registered investment adviser before investing.
""".strip()
    return title, meta, excerpt, article

# =====================================================
# Sidebar Inputs
# =====================================================
with st.sidebar:
    st.markdown("### 🐝 DCF Lab Inputs")
    st.caption("Keep assumptions realistic. DCF becomes dangerous when hope enters through the back door.")

    company = st.text_input("Company / Stock name", value="Example Stock")
    currency_symbol = st.selectbox("Currency", ["₹", "$", "€", "£"], index=0)

    st.divider()
    st.markdown("### Business numbers")
    latest_fcf_cr = st.number_input(
        "Latest Free Cash Flow, in Cr",
        min_value=0.01,
        value=1000.0,
        step=50.0,
        help="Use latest annual free cash flow. For Indian companies, enter amount in crore.",
    )
    shares_cr = st.number_input(
        "Shares outstanding, in Cr",
        min_value=0.01,
        value=100.0,
        step=1.0,
        help="Equity value in Cr divided by shares in Cr gives value per share.",
    )
    cash_cr = st.number_input("Cash & investments, in Cr", min_value=0.0, value=500.0, step=50.0)
    debt_cr = st.number_input("Total debt, in Cr", min_value=0.0, value=300.0, step=50.0)
    current_price = st.number_input("Current market price optional", min_value=0.0, value=900.0, step=10.0)

    st.divider()
    st.markdown("### DCF assumptions")
    years = st.slider("Projection period", min_value=5, max_value=15, value=10, step=1)
    start_growth = st.slider("Starting FCF growth", min_value=-10.0, max_value=35.0, value=12.0, step=0.5) / 100
    stable_growth = st.slider("Stable/terminal growth", min_value=0.0, max_value=7.0, value=4.0, step=0.25) / 100
    discount_rate = st.slider("Discount rate / required return", min_value=6.0, max_value=25.0, value=12.0, step=0.5) / 100
    margin_of_safety = st.slider("Margin of safety", min_value=0.0, max_value=60.0, value=25.0, step=1.0) / 100

    terminal_method = st.selectbox("Terminal value method", ["Gordon Growth Model", "Exit Multiple"], index=0)
    exit_multiple = st.slider("Exit FCF multiple", min_value=5.0, max_value=50.0, value=18.0, step=0.5)

    st.markdown("---")
    st.markdown(f"[🔓 Upgrade to Financify Pro]({SURECART_CHECKOUT_URL})")
    st.markdown(f"[🧰 Explore all tools]({TOOLS_PAGE_URL})")

# =====================================================
# Hero
# =====================================================
st.markdown(
    """
    <div class="hero-card">
        <div class="eyebrow">🐝 Free Financify Tool • DCF Value Lab</div>
        <div class="hero-title">DCF Value Calculator that <span>questions your assumptions</span></div>
        <div class="hero-subtitle">
            Estimate fair value using free cash flow, staged growth, discount rate, terminal value and margin of safety.
            This tool does not just give a number — it shows reverse DCF growth, terminal value dependency, scenario ranges,
            sensitivity heatmap and a Financify assumption-quality score.
        </div>
        <div class="hero-pills">
            <div class="pill">FCF-Based DCF</div>
            <div class="pill">Bear/Base/Bull Cases</div>
            <div class="pill">Reverse DCF</div>
            <div class="pill">Terminal Value Risk</div>
            <div class="pill">Shareable Report</div>
            <div class="pill">SEO Draft Generator</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# =====================================================
# Calculate
# =====================================================
if terminal_method == "Gordon Growth Model" and stable_growth >= discount_rate:
    st.error("Stable/terminal growth must be lower than discount rate for Gordon Growth DCF. Increase discount rate or reduce stable growth.")
    st.stop()

scenario_df, detailed = scenario_calculations(
    latest_fcf_cr=latest_fcf_cr,
    shares_cr=shares_cr,
    cash_cr=cash_cr,
    debt_cr=debt_cr,
    start_growth=start_growth,
    stable_growth=stable_growth,
    discount_rate=discount_rate,
    years=years,
    terminal_method=terminal_method,
    exit_multiple=exit_multiple,
    margin_of_safety=margin_of_safety,
)

base_calc = detailed["Base"]
bear_value = scenario_df.loc[scenario_df["Case"] == "Bear", "Fair Value/Share"].iloc[0]
base_value = scenario_df.loc[scenario_df["Case"] == "Base", "Fair Value/Share"].iloc[0]
bull_value = scenario_df.loc[scenario_df["Case"] == "Bull", "Fair Value/Share"].iloc[0]
mos_price = scenario_df.loc[scenario_df["Case"] == "Base", "MOS Price"].iloc[0]
terminal_dependency = base_calc["terminal_dependency"]
net_debt = debt_cr - cash_cr
net_debt_to_fcf = safe_div(net_debt, latest_fcf_cr)

score, notes = quality_score(
    start_growth=start_growth,
    stable_growth=stable_growth,
    discount_rate=discount_rate,
    years=years,
    terminal_dependency=terminal_dependency,
    margin_of_safety=margin_of_safety,
    net_debt_to_fcf=net_debt_to_fcf,
    terminal_method=terminal_method,
)

implied_growth = reverse_dcf_growth(
    target_price=current_price,
    latest_fcf_cr=latest_fcf_cr,
    shares_cr=shares_cr,
    cash_cr=cash_cr,
    debt_cr=debt_cr,
    stable_growth=stable_growth,
    discount_rate=discount_rate,
    years=years,
    terminal_method=terminal_method,
    exit_multiple=exit_multiple,
)

verdict_title, verdict_text = get_verdict(
    current_price=current_price,
    fair_value=base_value,
    mos_price=mos_price,
    bear_value=bear_value,
    bull_value=bull_value,
    score=score,
    terminal_dependency=terminal_dependency,
)

upside = (base_value / current_price - 1) if current_price > 0 and np.isfinite(base_value) else np.nan

# =====================================================
# Metrics
# =====================================================
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Base DCF Value</div>
        <div class="metric-value">{fmt_money(base_value, currency_symbol)}</div>
        <div class="metric-help">Estimated fair value per share before safety buffer.</div>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">MOS Buy Zone</div>
        <div class="metric-value">{fmt_money(mos_price, currency_symbol)}</div>
        <div class="metric-help">Base DCF value after margin of safety.</div>
    </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Upside/Downside</div>
        <div class="metric-value">{fmt_pct(upside)}</div>
        <div class="metric-help">Compared with current price entered.</div>
    </div>
    """, unsafe_allow_html=True)
with col4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">DCF Quality Score</div>
        <div class="metric-value">{score}/100</div>
        <div class="metric-help">Checks whether assumptions look realistic.</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# =====================================================
# Main layout
# =====================================================
left, right = st.columns([0.92, 1.38], gap="large")

with left:
    st.markdown(f"""
    <div class="verdict-box">
        <div class="verdict-title">{verdict_title}</div>
        <div class="verdict-text">{verdict_text}</div>
        <br>
        <span class="mini-badge">Reverse DCF Growth: {fmt_pct(implied_growth)}</span>
        <span class="mini-badge">Terminal Dependence: {fmt_pct(terminal_dependency)}</span>
        <span class="mini-badge">Net Debt/FCF: {net_debt_to_fcf:.2f}x</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="glass-card">
        <div class="section-title">🧠 DCF Reality Check</div>
        <div class="section-subtitle">A DCF is not a target price machine. It is an assumption testing machine.</div>
    """, unsafe_allow_html=True)

    reality_checks = [
        "Is latest FCF normal, or unusually high/low?",
        "Can the business reinvest capital at attractive returns?",
        "Is growth supported by revenue, margins and ROCE?",
        "Is debt low enough to protect future cash flows?",
        "Is terminal growth lower than nominal GDP-like growth?",
        "Would the stock still look reasonable in bear case?",
        "Does margin of safety protect you from being wrong?",
    ]
    for item in reality_checks:
        st.checkbox(item, value=False)
    st.markdown("</div>", unsafe_allow_html=True)

with right:
    st.markdown("""
    <div class="glass-card">
        <div class="section-title">📊 DCF Value Breakdown</div>
        <div class="section-subtitle">See how much value comes from explicit cash flows, terminal value and net cash/debt adjustment.</div>
    """, unsafe_allow_html=True)
    st.plotly_chart(make_breakdown_chart(base_calc, currency_symbol), use_container_width=True, config=PLOTLY_MOBILE_CONFIG)
    st.markdown("</div>", unsafe_allow_html=True)

# =====================================================
# Tabs
# =====================================================
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📈 Projections",
    "🐻 Scenarios",
    "🔥 Sensitivity",
    "🍯 Assumption Notes",
    "📤 Share Report",
    "📝 SEO Draft",
])

with tab1:
    st.markdown("""
    <div class="glass-card">
        <div class="section-title">Free Cash Flow Projection</div>
        <div class="section-subtitle">Growth starts from your assumption and fades toward stable growth over time.</div>
    </div>
    """, unsafe_allow_html=True)
    st.plotly_chart(make_projection_chart(base_calc["projection_df"], currency_symbol), use_container_width=True, config=PLOTLY_MOBILE_CONFIG)

    proj_display = base_calc["projection_df"].copy()
    proj_display["Growth Rate"] = proj_display["Growth Rate"].map(fmt_pct)
    proj_display["Projected FCF Cr"] = proj_display["Projected FCF Cr"].map(lambda x: fmt_cr(x, currency_symbol))
    proj_display["Discount Factor"] = proj_display["Discount Factor"].map(lambda x: f"{x:.2f}x")
    proj_display["PV of FCF Cr"] = proj_display["PV of FCF Cr"].map(lambda x: fmt_cr(x, currency_symbol))
    st.dataframe(proj_display, use_container_width=True, hide_index=True)

with tab2:
    st.markdown("""
    <div class="glass-card">
        <div class="section-title">Bear / Base / Bull DCF Range</div>
        <div class="section-subtitle">A serious DCF should produce a range, not one overconfident number.</div>
    </div>
    """, unsafe_allow_html=True)
    scen_display = scenario_df.copy()
    for col in ["Start Growth", "Stable Growth", "Discount Rate", "Terminal Dependency"]:
        scen_display[col] = scen_display[col].map(fmt_pct)
    scen_display["Exit Multiple"] = scen_display["Exit Multiple"].map(lambda x: f"{x:.2f}x" if np.isfinite(x) else "—")
    for col in ["PV FCF Cr", "PV Terminal Cr", "Enterprise Value Cr", "Equity Value Cr"]:
        scen_display[col] = scen_display[col].map(lambda x: fmt_cr(x, currency_symbol))
    for col in ["Fair Value/Share", "MOS Price"]:
        scen_display[col] = scen_display[col].map(lambda x: fmt_money(x, currency_symbol))
    st.dataframe(scen_display, use_container_width=True, hide_index=True)

    labels = scen_display["Case"].tolist()
    raw_values = scenario_df["Fair Value/Share"].tolist()
    mos_values = scenario_df["MOS Price"].tolist()
    fig = go.Figure()
    fig.add_trace(go.Bar(x=labels, y=raw_values, name="Fair Value", text=[fmt_money(v, currency_symbol) for v in raw_values], textposition="outside"))
    fig.add_trace(go.Bar(x=labels, y=mos_values, name="MOS Price", text=[fmt_money(v, currency_symbol) for v in mos_values], textposition="outside"))
    if current_price > 0:
        fig.add_hline(y=current_price, line_dash="dash", annotation_text="Current Price")
    fig.update_layout(
        title="DCF Value Range",
        barmode="group",
        template="plotly_white",
        height=420,
        margin=dict(l=20, r=20, t=60, b=50),
        yaxis_title="Value per share",
        font=dict(family="Inter", size=13),
        plot_bgcolor="rgba(255,255,255,0)",
        paper_bgcolor="rgba(255,255,255,0)",
    )
    st.plotly_chart(fig, use_container_width=True, config=PLOTLY_MOBILE_CONFIG)

with tab3:
    st.markdown("""
    <div class="glass-card">
        <div class="section-title">Sensitivity Honeycomb</div>
        <div class="section-subtitle">Small assumption changes can move valuation sharply. This is where DCF shows its real nature.</div>
    </div>
    """, unsafe_allow_html=True)
    st.plotly_chart(
        make_sensitivity_heatmap(
            latest_fcf_cr=latest_fcf_cr,
            shares_cr=shares_cr,
            cash_cr=cash_cr,
            debt_cr=debt_cr,
            start_growth=start_growth,
            stable_growth=stable_growth,
            discount_rate=discount_rate,
            years=years,
            terminal_method=terminal_method,
            exit_multiple=exit_multiple,
            currency_symbol=currency_symbol,
        ),
        use_container_width=True,
        config=PLOTLY_MOBILE_CONFIG,
    )

with tab4:
    st.markdown("""
    <div class="glass-card">
        <div class="section-title">Assumption Quality Notes</div>
        <div class="section-subtitle">This is the Financify layer: the tool challenges your assumptions before you trust the output.</div>
    """, unsafe_allow_html=True)
    for note in notes:
        st.markdown(f"- {note}")
    st.markdown("</div>", unsafe_allow_html=True)

    terminal_warning = ""
    if np.isfinite(terminal_dependency) and terminal_dependency > 0.75:
        terminal_warning = "Most of this valuation is coming from terminal value. Reduce growth, increase discount rate, or use a stronger margin of safety to test fragility."
    else:
        terminal_warning = "Terminal value dependency is not extreme, but still important. Always test bear case."

    st.markdown(f"""
    <div class="warning-box">
    <b>Terminal Value Reality:</b> {terminal_warning}
    </div>
    """, unsafe_allow_html=True)

with tab5:
    report = build_report(
        company=company,
        currency_symbol=currency_symbol,
        latest_fcf_cr=latest_fcf_cr,
        shares_cr=shares_cr,
        cash_cr=cash_cr,
        debt_cr=debt_cr,
        current_price=current_price,
        start_growth=start_growth,
        stable_growth=stable_growth,
        discount_rate=discount_rate,
        years=years,
        terminal_method=terminal_method,
        exit_multiple=exit_multiple,
        margin_of_safety=margin_of_safety,
        scenario_df=scenario_df,
        verdict_title=verdict_title,
        verdict_text=verdict_text,
        score=score,
        notes=notes,
        implied_growth=implied_growth,
        terminal_dependency=terminal_dependency,
    ).strip()

    st.markdown("""
    <div class="glass-card">
        <div class="section-title">Shareable DCF Mini Report</div>
        <div class="section-subtitle">This helps the free tool spread. Users can copy, download and share the output.</div>
    </div>
    """, unsafe_allow_html=True)
    st.text_area("Copy report", value=report, height=390)
    st.download_button(
        "⬇️ Download DCF report",
        data=report,
        file_name=f"financify_dcf_report_{company.replace(' ', '_').lower() or 'stock'}.txt",
        mime="text/plain",
    )

    csv_data = scenario_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇️ Download scenario CSV",
        data=csv_data,
        file_name=f"financify_dcf_scenarios_{company.replace(' ', '_').lower() or 'stock'}.csv",
        mime="text/csv",
    )

    share_text = f"I estimated {company or 'a stock'} DCF value using Financify. Base value: {fmt_money(base_value, currency_symbol)}, MOS price: {fmt_money(mos_price, currency_symbol)}. Try the free tools: {TOOLS_PAGE_URL}"
    whatsapp_url = f"https://wa.me/?text={quote_plus(share_text)}"
    twitter_url = f"https://twitter.com/intent/tweet?text={quote_plus(share_text)}"
    st.markdown(f"[📲 Share on WhatsApp]({whatsapp_url})  &nbsp;&nbsp; [𝕏 Share on X]({twitter_url})", unsafe_allow_html=True)

with tab6:
    title, meta, excerpt, article = build_seo_draft(
        company=company,
        currency_symbol=currency_symbol,
        latest_fcf_cr=latest_fcf_cr,
        current_price=current_price,
        base_value=base_value,
        mos_price=mos_price,
        start_growth=start_growth,
        stable_growth=stable_growth,
        discount_rate=discount_rate,
        terminal_method=terminal_method,
        terminal_dependency=terminal_dependency,
    )
    st.markdown("""
    <div class="glass-card">
        <div class="section-title">SEO Article Draft Generator</div>
        <div class="section-subtitle">Use this as a WordPress draft below the tool. Edit it with your own examples before publishing.</div>
    </div>
    """, unsafe_allow_html=True)
    st.text_input("SEO title", value=title)
    st.text_area("Meta description", value=meta, height=90)
    st.text_area("Excerpt", value=excerpt, height=90)
    st.text_area("Article draft", value=article, height=520)

    faq_schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": "What is a DCF calculator?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "A DCF calculator estimates the present value of a business based on future free cash flows, discount rate and terminal value assumptions."
                }
            },
            {
                "@type": "Question",
                "name": "Is DCF value the same as target price?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "No. DCF value is an estimate based on assumptions. It should be used as a valuation range, not a guaranteed target price."
                }
            },
            {
                "@type": "Question",
                "name": "Why does margin of safety matter in DCF?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "Margin of safety protects investors from being wrong about growth, discount rate, terminal value or business quality."
                }
            }
        ]
    }
    st.text_area("Optional FAQ schema for WordPress", value=str(faq_schema).replace("'", '"'), height=260)

# =====================================================
# CTA + Disclaimer
# =====================================================
st.markdown(f"""
<div class="cta-card">
    <h3>DCF tells value. Financify Pro checks quality.</h3>
    <p>
    This free DCF tool helps users estimate value. But a serious investor should also check debt, ROE, ROCE, margin trend,
    CFO, FCF consistency, valuation comfort, bubble risk and market cycle. That is where your premium Financify tools become useful.
    </p>
    <p>👉 <a href="{SURECART_CHECKOUT_URL}" target="_blank" style="color:#111;font-weight:950;">Upgrade to Financify Pro</a> &nbsp; | &nbsp;
    <a href="{TOOLS_PAGE_URL}" target="_blank" style="color:#111;font-weight:950;">Explore all Financify tools</a></p>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<div class="warning-box">
<b>Educational disclaimer:</b> This DCF calculator is for learning and research only. It is not investment advice, a stock recommendation, or a buy/sell signal. DCF outputs depend fully on user-entered assumptions. Please do your own research or consult a SEBI-registered investment adviser before making financial decisions.
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="footer-note">🐝 Financify • Madness of Money Bees • Free DCF Value Lab for practical finance learners</div>
""", unsafe_allow_html=True)
