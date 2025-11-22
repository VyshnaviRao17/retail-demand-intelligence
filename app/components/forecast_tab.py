import streamlit as st
import pandas as pd
import plotly.graph_objs as go
from typing import Tuple, List

# import export helpers (they return bytes or encoded data)
from components.download_utils import export_csv, export_json, export_excel

# -----------------------
# Cached helpers (module-level)
# -----------------------

@st.cache_data(show_spinner=False)
def _build_dfs(
    hist_dates: Tuple[str, ...],
    hist_values: Tuple[float, ...],
    fc_dates: Tuple[str, ...],
    fc_values: Tuple[float, ...],
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Create light DataFrames from immutable tuples (cached)."""
    hist_df = pd.DataFrame({"date": list(hist_dates), "value": list(hist_values)}) if hist_dates else pd.DataFrame()
    fc_df = pd.DataFrame({"date": list(fc_dates), "forecast": list(fc_values)})
    return hist_df, fc_df


@st.cache_data(show_spinner=False)
def _build_forecast_figure(
    hist_dates: Tuple[str, ...],
    hist_values: Tuple[float, ...],
    fc_dates: Tuple[str, ...],
    fc_values: Tuple[float, ...],
) -> go.Figure:
    """Build the Plotly figure once per unique input (cached)."""
    upper = [v * 1.15 for v in fc_values]
    lower = [v * 0.85 for v in fc_values]

    fig = go.Figure()

    if hist_dates:
        fig.add_trace(
            go.Scatter(
                x=list(hist_dates),
                y=list(hist_values),
                mode="lines+markers",
                name="History",
                line=dict(width=3, color="#4D96FF"),
                marker=dict(size=6),
            )
        )

    fig.add_trace(
        go.Scatter(
            x=list(fc_dates),
            y=list(fc_values),
            mode="lines+markers",
            name="Forecast",
            line=dict(width=3, color="#FF6B6B"),
            marker=dict(size=6),
        )
    )

    # confidence band
    fig.add_trace(
        go.Scatter(
            x=list(fc_dates) + list(fc_dates)[::-1],
            y=upper + lower[::-1],
            fill="toself",
            fillcolor="rgba(77,150,255,0.12)",
            line=dict(color="rgba(255,255,255,0)"),
            showlegend=False,
            name="Confidence",
        )
    )

    fig.update_layout(
        template="plotly_white",
        height=430,
        margin=dict(l=12, r=12, t=36, b=12),
        title="Sales Forecast (Next 14 Days)",
        xaxis_title="Date",
        yaxis_title="Sales",
    )

    return fig


@st.cache_data(show_spinner=False)
def _export_forecast_csv(fc_dates: Tuple[str, ...], fc_values: Tuple[float, ...]) -> bytes:
    """Return CSV bytes for forecast (cached)."""
    df = pd.DataFrame({"date": list(fc_dates), "forecast": list(fc_values)})
    return export_csv(df)


@st.cache_data(show_spinner=False)
def _export_forecast_json(forecast_json_serializable) -> bytes:
    """Return JSON bytes for forecast (cached)."""
    return export_json(forecast_json_serializable)


@st.cache_data(show_spinner=False)
def _export_forecast_excel(
    hist_dates: Tuple[str, ...], hist_values: Tuple[float, ...], fc_dates: Tuple[str, ...], fc_values: Tuple[float, ...]
) -> bytes:
    """Return Excel bytes for forecast + history (cached)."""
    hist_df = pd.DataFrame({"date": list(hist_dates), "value": list(hist_values)}) if hist_dates else pd.DataFrame()
    fc_df = pd.DataFrame({"date": list(fc_dates), "forecast": list(fc_values)})
    return export_excel(hist_df, fc_df)


# -----------------------
# Render function (fast)
# -----------------------
def render_forecast_tab(forecast_json: dict):
    """Optimized forecast tab: accepts forecast_json and renders cached charts/exports."""
    st.subheader("📈 Forecast Overview")

    # --- Normalize inputs into immutable tuples for stable caching keys ---
    hist_dates = tuple(forecast_json.get("history_dates", []))
    hist_values = tuple(float(v) for v in forecast_json.get("history_values", []))
    fc_dates = tuple(forecast_json["forecast_dates"])
    fc_values = tuple(float(v) for v in forecast_json["forecast_values"])

    # --- KPIs (very cheap) ---
    c1, c2, c3 = st.columns(3)
    c1.metric("Store", forecast_json.get("store", "Store 1"))
    c2.metric("SKU", forecast_json.get("sku", "SKU 101"))
    c3.metric("Days Forecasted", len(fc_dates))

    # --- Build / fetch cached DataFrames & Figure ---
    hist_df, fc_df = _build_dfs(hist_dates, hist_values, fc_dates, fc_values)
    fig = _build_forecast_figure(hist_dates, hist_values, fc_dates, fc_values)

    # --- Plot (very fast: fig object is cached) ---
    st.markdown('<div class="fade-in">', unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # --- Summary metrics (cheap) ---
    s1, s2, s3 = st.columns(3)
    s1.metric("Next 3 Days", round(sum(fc_values[:3]), 2))
    s2.metric("Next 7 Days", round(sum(fc_values[:7]), 2))
    s3.metric("Next 14 Days", round(sum(fc_values[:14]), 2))

    # --- Downloads (cached exports) ---
    st.markdown("### 📥 Download Data")

    csv_bytes = _export_forecast_csv(fc_dates, fc_values)
    json_bytes = _export_forecast_json(forecast_json)
    excel_bytes = _export_forecast_excel(hist_dates, hist_values, fc_dates, fc_values)

    d1, d2, d3 = st.columns(3)
    d1.download_button("⬇ Forecast CSV", data=csv_bytes, file_name="forecast.csv", mime="text/csv")
    d2.download_button("📘 Forecast JSON", data=json_bytes, file_name="forecast.json", mime="application/json")
    d3.download_button(
        "📊 Excel Report",
        data=excel_bytes,
        file_name="forecast_report.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
