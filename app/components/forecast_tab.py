import streamlit as st
import plotly.graph_objs as go
import pandas as pd
from components.download_utils import export_csv, export_json, export_excel


def render_forecast_tab(forecast_json):
    st.subheader("📈 Forecast Overview")

    # --- KPIs ---
    c1, c2, c3 = st.columns(3)
    c1.metric("Store", forecast_json["store"])
    c2.metric("SKU", forecast_json["sku"])
    c3.metric("Days Forecasted", len(forecast_json["forecast_values"]))

    # --- Extract Data ---
    history_dates = forecast_json.get("history_dates", [])
    history_values = forecast_json.get("history_values", [])
    forecast_dates = forecast_json["forecast_dates"]
    forecast_values = forecast_json["forecast_values"]

    upper = [v * 1.15 for v in forecast_values]
    lower = [v * 0.85 for v in forecast_values]

    # --- Chart ---
    fig = go.Figure()

    if len(history_dates) > 0:
        fig.add_trace(go.Scatter(
            x=history_dates, y=history_values,
            mode='lines+markers', name='History',
            line=dict(width=3, color='#4D96FF')
        ))

    fig.add_trace(go.Scatter(
        x=forecast_dates, y=forecast_values,
        mode='lines+markers', name='Forecast',
        line=dict(width=3, color='#FF6B6B')
    ))

    fig.add_trace(go.Scatter(
        x=forecast_dates + forecast_dates[::-1],
        y=upper + lower[::-1],
        fill='toself', fillcolor='rgba(77,150,255,0.12)',
        line=dict(color='rgba(0,0,0,0)'), showlegend=False
    ))

    fig.update_layout(
        template="plotly_white",
        height=430,
        title="Sales Forecast (Next 14 Days)"
    )

    st.markdown('<div class="fade-in">', unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # --- Summary ---
    st.markdown("### 🔢 Summary")
    s1, s2, s3 = st.columns(3)
    s1.metric("Next 3 Days", sum(forecast_values[:3]))
    s2.metric("Next 7 Days", sum(forecast_values[:7]))
    s3.metric("Next 14 Days", sum(forecast_values[:14]))

    # --- Downloads ---
    st.markdown("### 📥 Download Data")

    history_df = pd.DataFrame({"date": history_dates, "value": history_values})
    forecast_df = pd.DataFrame({"date": forecast_dates, "forecast": forecast_values})

    d1, d2, d3 = st.columns(3)

    d1.download_button("⬇ Forecast CSV", export_csv(forecast_df),
                       "forecast.csv", "text/csv")
    d2.download_button("📘 Forecast JSON", export_json(forecast_json),
                       "forecast.json", "application/json")
    d3.download_button("📊 Excel Report", export_excel(history_df, forecast_df),
                       "forecast.xlsx",
                       "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
