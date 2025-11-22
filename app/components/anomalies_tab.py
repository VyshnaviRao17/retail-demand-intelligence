import streamlit as st
import plotly.graph_objs as go
import pandas as pd
from components.download_utils import export_csv


# ------------------------------------------------
# CACHING HELPERS
# ------------------------------------------------

@st.cache_data(show_spinner=False)
def _build_anomaly_figure(
    dates: tuple,
    sales: tuple,
    rolling7: tuple,
):
    """Build and cache the anomalies chart."""
    fig = go.Figure()

    # Sales bars
    fig.add_trace(
        go.Bar(
            x=list(dates),
            y=list(sales),
            name="Sales",
            marker_color="#FF6B6B",
        )
    )

    # Rolling avg line
    fig.add_trace(
        go.Scatter(
            x=list(dates),
            y=list(rolling7),
            mode="lines+markers",
            name="7-Day Avg",
            line=dict(color="#4D96FF", width=3),
            marker=dict(size=6),
        )
    )

    fig.update_layout(
        template="plotly_white",
        height=420,
        margin=dict(l=12, r=12, t=30, b=12),
        title="Actual Sales vs Rolling 7-Day Average",
    )

    return fig


@st.cache_data(show_spinner=False)
def _export_anomaly_csv(df: pd.DataFrame) -> bytes:
    """Convert anomalies df to CSV bytes with caching."""
    return export_csv(df)


# ------------------------------------------------
# MAIN RENDER FUNCTION (FAST)
# ------------------------------------------------

def render_anomalies_tab(df: pd.DataFrame):
    st.subheader("⚠️ Anomaly Detection")

    if df.empty:
        st.success("✔ No anomalies detected.")
        return

    # Convert DF columns to immutable tuples for caching
    dates = tuple(str(d) for d in df["date"])
    sales = tuple(float(v) for v in df["sales"])
    rolling7 = tuple(float(v) for v in df["rolling_7"])

    # ---------------- KPIs ----------------
    c1, c2 = st.columns(2)
    c1.metric("Total Anomalies", len(df))
    c2.metric("Affected Days", df["date"].nunique())

    # ---------------- Chart (CACHED) ----------------
    st.markdown("### 📊 Actual vs Rolling Average")

    fig = _build_anomaly_figure(dates, sales, rolling7)

    st.markdown('<div class="fade-in">', unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # ---------------- Table ----------------
    st.markdown("### 🔍 Detailed Report")
    st.dataframe(df, use_container_width=True)

    # ---------------- Download ----------------
    st.markdown("### 📥 Download Anomalies CSV")

    csv_bytes = _export_anomaly_csv(df)

    st.download_button(
        "⬇ Download CSV",
        data=csv_bytes,
        file_name="anomalies.csv",
        mime="text/csv",
    )
