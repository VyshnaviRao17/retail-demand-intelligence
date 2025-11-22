import streamlit as st
import pandas as pd
import json
import sys
import os
from typing import Tuple, List

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Backend
from src.predict import predict_next_14_days
from src.anomalies import detect_anomalies

# UI Components
from components.forecast_tab import render_forecast_tab
from components.anomalies_tab import render_anomalies_tab
from components.stock_tab import render_stock_tab
from components.insights_tab import render_insights_tab
from components.ui_utils import inject_global_css, dark_mode_css
from components.download_utils import export_pdf


# ----------------------------------------------------------
# SUPER CACHING LAYER (Fixes 90% of Lag)
# ----------------------------------------------------------

@st.cache_data(show_spinner=False)
def cached_sales():
    df = pd.read_csv("data/sales.csv")
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"])
    return df


@st.cache_data(show_spinner=True)
def cached_forecast():
    """Compute forecast once per session."""
    return predict_next_14_days()


@st.cache_data(show_spinner=True)
def cached_anomalies():
    """Compute anomalies once per session."""
    return detect_anomalies()


@st.cache_data(show_spinner=False)
def cached_pdf(f_json, anomalies):
    return export_pdf(f_json, anomalies)


# ----------------------------------------------------------
# Build reusable forecast JSON
# ----------------------------------------------------------
def make_forecast_json(dates, preds):
    return {
        "store": "Store 1",
        "sku": "SKU 101",
        "history_dates": dates[:7],
        "history_values": preds[:7],
        "forecast_dates": dates,
        "forecast_values": preds,
    }


# ----------------------------------------------------------
# MAIN APP
# ----------------------------------------------------------
def main():
    st.set_page_config(page_title="Retail Demand Intelligence", layout="wide")
    inject_global_css()

    # ---------------- HEADER ----------------
    st.markdown(
        """
        <div style="background: linear-gradient(135deg, #4D96FF, #6EA8FE);
        padding: 18px; border-radius: 12px; box-shadow: 0px 4px 14px rgba(0,0,0,0.1);
        text-align:center; margin-bottom:20px;">
            <h1 style="color:white;">Retail Demand Intelligence</h1>
            <p style="color:white; margin:0;">Fast, cached, optimized performance</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ---------------- SIDEBAR ----------------
    with st.sidebar:
        st.markdown("## ⚙ Controls")
        dark = st.checkbox("Dark Mode")
        st.selectbox("Store", ["Store 1", "Store 2", "Store 3"])
        st.selectbox("SKU", ["SKU 101", "SKU 102", "SKU 103"])

        st.markdown("---")
        if st.button("🔁 Refresh ML Cache"):
            st.cache_data.clear()
            st.experimental_rerun()

    dark_mode_css(dark)

    # ---------------- LOAD EVERYTHING (CACHED) ----------------
    with st.spinner("Loading forecasts…"):
        dates, preds = cached_forecast()

    with st.spinner("Loading anomaly detection…"):
        anomalies_df = cached_anomalies()

    forecast_json = make_forecast_json(dates, preds)

    # Prebuild PDF for fast download
    pdf_bytes = cached_pdf(forecast_json, anomalies_df)

    # ---------------- TABS ----------------
    tab1, tab2, tab3, tab4 = st.tabs(
        ["📈 Forecast", "⚠️ Anomalies", "📦 Stock Advisor", "📊 Insights"]
    )

    with tab1:
        render_forecast_tab(forecast_json)

    with tab2:
        render_anomalies_tab(anomalies_df)

    with tab3:
        render_stock_tab(forecast_json)

    with tab4:
        render_insights_tab()

    # Sidebar downloads
    with st.sidebar:
        st.markdown("---")
        st.download_button("📄 PDF Report", data=pdf_bytes, file_name="report.pdf")
        st.download_button(
            "⬇ Forecast CSV",
            pd.DataFrame({"date": dates, "forecast": preds}).to_csv(index=False),
            file_name="forecast.csv",
        )
        st.download_button(
            "⬇ Anomalies CSV",
            anomalies_df.to_csv(index=False).encode("utf-8"),
            file_name="anomalies.csv",
        )


if __name__ == "__main__":
    main()
