import streamlit as st
import pandas as pd
import json
import sys
import os

# ---------- FIX: Add project root to Python path ----------
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# ---------- Backend ML Imports ----------
from src.predict import predict_next_14_days
from src.anomalies import detect_anomalies

# ---------- Component Imports ----------
from components.forecast_tab import render_forecast_tab
from components.anomalies_tab import render_anomalies_tab
from components.stock_tab import render_stock_tab
from components.insights_tab import render_insights_tab
from components.ui_utils import inject_global_css, dark_mode_css, show_loading
from components.download_utils import export_pdf


# ==========================================================
#               LOAD FORECAST FROM BACKEND
# ==========================================================
def load_forecast():
    dates, predictions = predict_next_14_days()

    forecast_json = {
        "store": "Store 1",
        "sku": "SKU 101",
        "history_dates": dates[:7],   # optional history
        "history_values": predictions[:7],
        "forecast_dates": dates,
        "forecast_values": predictions
    }

    return forecast_json


# ==========================================================
#                LOAD ANOMALIES FROM BACKEND
# ==========================================================
def load_anomalies():
    anomalies_df = detect_anomalies()
    return anomalies_df


# ==========================================================
#                       MAIN APP
# ==========================================================
def main():
    st.set_page_config(
        page_title="Retail Demand Intelligence",
        layout="wide"
    )

    inject_global_css()

    # ---------------- HEADER ----------------
    st.markdown(
        """
        <div style="
            background: linear-gradient(135deg, #4D96FF, #6EA8FE);
            padding: 26px;
            border-radius: 16px;
            text-align: center;
            box-shadow: 0 6px 20px rgba(0,0,0,0.12);
            margin-bottom: 22px;">
            <h1 style="color:white;font-size:40px;margin:0;">Retail Demand Intelligence Dashboard</h1>
            <p style="color:white;margin-top:8px;font-size:17px;">
                AI-Powered Forecasting • Anomaly Detection • Stock Planning • Insights
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ---------------- SIDEBAR ----------------
    with st.sidebar:
        st.markdown("## ⚙ Controls")

        dark = st.checkbox("Dark Mode")

        st.markdown("### Filters")
        st.selectbox("Store", ["Store 1", "Store 2", "Store 3"])
        st.selectbox("SKU", ["SKU 101", "SKU 102", "SKU 103"])

        st.markdown("---")

        # Load backend outputs
        forecast_json = load_forecast()
        anomalies_df = load_anomalies()

        # PDF Export
        st.markdown("### 📄 Export Report")
        pdf_bytes = export_pdf(forecast_json, anomalies_df)

        st.download_button(
            label="📄 Download PDF Report",
            data=pdf_bytes,
            file_name="retail_report.pdf",
            mime="application/pdf"
        )

        st.caption("Made with ❤️ using Streamlit + ML")

    # Apply dark theme
    dark_mode_css(dark)

    # Loading animation
    show_loading("Loading dashboard…", seconds=0.5)

    # ---------------- TABS ----------------
    tab1, tab2, tab3, tab4 = st.tabs([
        "📈 Forecast",
        "⚠️ Anomalies",
        "📦 Stock Advisor",
        "📊 Insights"
    ])

    with tab1:
        render_forecast_tab(forecast_json)

    with tab2:
        render_anomalies_tab(anomalies_df)

    with tab3:
        render_stock_tab(forecast_json)

    with tab4:
        render_insights_tab()


# ==========================================================
#                       RUN APP
# ==========================================================
if __name__ == "__main__":
    main()
