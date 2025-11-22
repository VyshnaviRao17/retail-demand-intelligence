# app/components/ui_utils.py
import streamlit as st
import time

# -------------------------------------------------
# GLOBAL CSS INJECTION  (runs once safely via cache)
# -------------------------------------------------

@st.cache_resource
def inject_global_css():
    """Inject global CSS only once per session for performance."""
    css = """
    <style>

    /* Root variables (easy theme switching) */
    :root {
        --primary-text: #0f1724;
        --background-light: #ffffff;
        --background-dark: #0f1724;
        --text-light: #ffffff;
    }

    /* Smooth transitions */
    .stApp, .main, .block-container {
        transition: background-color 300ms ease, color 300ms ease;
    }

    /* Fade-in animation used across app */
    .fade-in {
        opacity: 0;
        transform: translateY(6px);
        animation: fadeInUp 0.55s ease forwards;
        will-change: opacity, transform;
    }
    @keyframes fadeInUp {
        to { opacity: 1; transform: translateY(0); }
    }

    /* Card style */
    .sidebar-card {
        background: rgba(255,255,255,0.03);
        border-radius: 12px;
        padding: 12px;
        margin-bottom: 14px;
    }

    /* Tabs padding */
    .stTabs [role="tabpanel"] {
        padding-top: 6px !important;
    }

    /* Smooth chart container */
    .chart-container {
        transition: opacity 250ms ease;
    }

    /* Metric card styling (works with light/dark mode) */
    .metric-card {
        border-radius: 12px;
        padding: 14px 18px;
        background: var(--background-light);
        color: var(--primary-text);
        box-shadow: 0 1px 4px rgba(0,0,0,0.08);
        transition: background 250ms ease, color 250ms ease;
    }

    .metric-title { font-size: 14px; font-weight: 600; }
    .metric-value { font-size: 22px; font-weight: 700; }

    /* General text and background */
    .main, .block-container {
        background-color: var(--background-light);
        color: var(--primary-text);
    }

    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


# -------------------------------------------------
# LOADING SPINNER (NON-BLOCKING)
# -------------------------------------------------

def show_loading(message="Loading…", seconds=0.4):
    """
    Small spinner to smooth transitions.
    Uses ultra-short sleep for feel, not a full block.
    """
    with st.spinner(message):
        time.sleep(seconds)  # kept minimal for user-perception only


# -------------------------------------------------
# DARK MODE (LIGHTWEIGHT & GPU-ACCELERATED)
# -------------------------------------------------

@st.cache_resource
def _dark_css():
    """Cache the dark theme CSS block."""
    return """
    <style>
    :root {
        --primary-text: #e6eef8;
        --background-light: #0f1724;
    }

    body, .main, .block-container {
        background: var(--background-light) !important;
        color: var(--primary-text) !important;
    }

    .metric-card {
        background: #071029 !important;
        color: var(--primary-text) !important;
    }

    /* Set tab panel background for dark mode */
    .stTabs [role="tabpanel"] {
        background: #0c1423 !important;
    }
    </style>
    """

@st.cache_resource
def _light_css():
    """Cache light theme CSS block."""
    return """
    <style>
    :root {
        --primary-text: #0f1724;
        --background-light: #ffffff;
    }

    body, .main, .block-container {
        background: var(--background-light) !important;
        color: var(--primary-text) !important;
    }

    .metric-card {
        background: #ffffff !important;
        color: #0f1724 !important;
    }
    </style>
    """


def dark_mode_css(enable: bool):
    """Fast toggle between dark and light mode."""
    if enable:
        st.markdown(_dark_css(), unsafe_allow_html=True)
    else:
        st.markdown(_light_css(), unsafe_allow_html=True)
