import streamlit as st
import pandas as pd
from components.ui_components import metric_card

def render_insights_tab():
    st.subheader("📊 Insights & KPIs")

    # KPI Cards
    c1, c2, c3 = st.columns(3)

    with c1:
        metric_card("Model Accuracy", "92%", "🎯", "green")

    with c2:
        metric_card("Weekly Anomalies", "3", "⚠️", "red")

    with c3:
        metric_card("High-Risk SKUs", "4", "🔥", "yellow")

    st.markdown("---")

    # Table: Unstable SKUs
    st.markdown("### 🔥 Top Unstable SKUs")

    data = pd.DataFrame({
        "SKU": [101, 102, 105, 110],
        "Instability Score": [0.91, 0.83, 0.79, 0.74]
    })

    st.markdown('<div class="fade-in">', unsafe_allow_html=True)
    st.table(data)
    st.markdown('</div>', unsafe_allow_html=True)
