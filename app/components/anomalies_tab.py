import streamlit as st
import plotly.graph_objs as go
from components.download_utils import export_csv

def render_anomalies_tab(df):
    st.subheader("⚠️ Anomaly Detection")

    if df.empty:
        st.success("✔ No anomalies detected.")
        return

    # KPIs
    c1, c2 = st.columns(2)
    c1.metric("Total Anomalies", len(df))
    c2.metric("Affected Days", df['date'].nunique())

    # Chart
    st.markdown("### 📊 Actual vs Rolling Average")

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=df['date'], y=df['sales'],
        name="Sales", marker_color="#FF6B6B"
    ))

    fig.add_trace(go.Scatter(
        x=df['date'], y=df['rolling_7'],
        mode='lines+markers',
        name="7-Day Avg",
        line=dict(color="#4D96FF", width=3)
    ))

    fig.update_layout(template="plotly_white", height=420)

    st.markdown('<div class="fade-in">', unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Table
    st.markdown("### 🔍 Detailed Report")
    st.dataframe(df, use_container_width=True)

    # Download
    st.markdown("### 📥 Download Anomalies CSV")
    st.download_button("⬇ Anomalies CSV",
                       export_csv(df),
                       "anomalies.csv",
                       "text/csv")
