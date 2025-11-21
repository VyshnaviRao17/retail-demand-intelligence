# app/components/ui_utils.py
import streamlit as st
import time

def inject_global_css():
    """Call once at app start to inject global styles/animations."""
    css = """
    <style>
    /* page background subtle */
    .reportview-container .main {
        transition: background-color 300ms ease;
    }

    /* header animation already exists; add subtle parallax */
    .animated-header {
        will-change: transform, opacity;
    }

    /* fade-in for charts & sections */
    .fade-in {
        opacity: 0;
        transform: translateY(6px);
        animation: fadeInUp 0.55s ease forwards;
    }
    @keyframes fadeInUp {
        to { opacity: 1; transform: translateY(0); }
    }

    /* subtle tab content container */
    .stTabs [role="tabpanel"] {
        padding-top: 6px;
        transition: opacity 250ms ease;
    }

    /* sidebar card rounded */
    .sidebar-card {
        background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));
        border-radius: 12px;
        padding: 8px;
        margin-bottom: 12px;
    }

    /* small spinner center */
    .centered-spinner { display:flex; justify-content:center; align-items:center; padding:18px; }

    /* dark override (applied via injecting another block when dark) */
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

def show_loading(message="Loading…", seconds=0.6):
    """Simple visual spinner that also reveals space for charts (non-blocking)."""
    # Use streamlit spinner for blocking tasks or show a short friendly demo spinner
    with st.spinner(message):
        if seconds > 0:
            time.sleep(seconds)  # short animated pause to let users feel loading

def dark_mode_css(enable: bool):
    """Inject a dark-mode CSS toggle by setting background/text overrides (best effort)."""
    if enable:
        css = """
        <style>
        .reportview-container .main { background: #0f1724; color: #e6eef8; }
        .stApp .css-1v3fvcr { background: #0f1724; } /* Streamlit class names vary - best-effort */
        .metric-card { background: #071029 !important; color: #e6eef8 !important; }
        .metric-title, .metric-value { color: #e6eef8 !important; }
        </style>
        """
        st.markdown(css, unsafe_allow_html=True)
    else:
        # remove by injecting neutral style (can't truly remove earlier CSS); this sets base back to light
        css = """
        <style>
        .reportview-container .main { background: #ffffff; color: #0f1724; }
        .metric-card { background: white !important; color: #0f1724 !important; }
        .metric-title, .metric-value { color: #0f1724 !important; }
        </style>
        """
        st.markdown(css, unsafe_allow_html=True)
