import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from src.predict import predict_next_14_days
from src.anomalies import detect_anomalies

# Streamlit Page Setup
st.set_page_config(page_title="AI Retail Demand Intelligence", layout="wide")

st.title("🛒 AI Retail Demand Intelligence Dashboard")

# Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Forecast",
    "⚠️ Anomalies",
    "📦 Stock Advisor",
    "📊 Insights"
])

# -----------------------------
# FORECAST TAB
# -----------------------------
with tab1:
    st.subheader("14-Day Sales Forecast")

    dates, preds = predict_next_14_days()

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dates,
        y=preds,
        mode='lines+markers',
        name='Forecast'
    ))

    fig.update_layout(
        title="Predicted Sales for the next 14 days",
        xaxis_title="Date",
        yaxis_title="Predicted Sales",
        height=400
    )

    st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# ANOMALIES TAB
# -----------------------------
with tab2:
    st.subheader("Detected Anomalies")

    anomalies = detect_anomalies()

    st.write("These are days where sales spiked or dropped suddenly:")
    st.dataframe(anomalies)

# -----------------------------
# STOCK ADVISOR TAB
# -----------------------------
with tab3:
    st.subheader("Smart Stock Advisor")

    demand_7 = sum(preds[:7])
    safety = demand_7 * 0.15
    recommended = demand_7 + safety

    st.metric("📆 Next 7-Day Demand", round(demand_7))
    st.metric("🛡 Safety Stock (15%)", round(safety))
    st.metric("📦 Total Stock Required", round(recommended))

# -----------------------------
# INSIGHTS TAB
# -----------------------------
with tab4:
    st.subheader("📊 Key Insights")

    df = pd.read_csv("data/sales.csv")

    # Highest Sales Day
    max_day = df.loc[df['sales'].idxmax()]
    st.write(f"🔺 **Highest sales day:** {max_day['date']} → {max_day['sales']} units")

    # Lowest Sales Day
    min_day = df.loc[df['sales'].idxmin()]
    st.write(f"🔻 **Lowest sales day:** {min_day['date']} → {min_day['sales']} units")

    # Monthly Sales Trend
    df['date'] = pd.to_datetime(df['date'])
    df['month'] = df['date'].dt.strftime("%b")
    monthly_avg = df.groupby('month')['sales'].mean()

    st.write("📆 **Average Sales per Month**")
    st.bar_chart(monthly_avg)

    # Forecast Trend
    trend = "📈 Upward Trend" if preds[-1] > preds[0] else "📉 Downward Trend"
    st.success(f"**Overall Forecast Trend:** {trend}")
