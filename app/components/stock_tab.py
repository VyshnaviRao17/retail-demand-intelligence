import streamlit as st
from components.ui_components import metric_card

def render_stock_tab(forecast_json):
    st.subheader("📦 Smart Stock Advisor")

    forecast_values = forecast_json["forecast_values"]

    # Inputs
    st.markdown("### 📥 Input Parameters")
    c1, c2, c3 = st.columns(3)

    current_stock = c1.number_input("Current Stock", value=50, min_value=0)
    lead_time = c2.number_input("Lead Time (days)", value=7, min_value=1)
    safety_pct = c3.slider("Safety Stock (%)", 0, 50, 15)

    # Compute
    demand_next = sum(forecast_values[:lead_time])
    safety_stock = int(demand_next * (safety_pct / 100))
    recommended = max(0, int(demand_next + safety_stock - current_stock))

    # KPI Cards
    st.markdown("### 📊 Stock Summary")
    k1, k2, k3 = st.columns(3)

    with k1:
        metric_card("Demand (Lead Time)", demand_next, "📈", "blue")

    with k2:
        metric_card("Safety Stock", safety_stock, "🛡️", "yellow")

    with k3:
        metric_card("Recommended Reorder", recommended, "📦", "red" if recommended > 0 else "green")

    # Recommendation
    st.markdown("### 🧠 System Recommendation")

    if recommended > 0:
        st.markdown(
            f"""
            <div style="
                background-color:#FFF3CD;
                padding:15px;
                border-radius:10px;
                border-left:6px solid #FFCD39;
                font-size:18px;
                font-weight:600;
            ">
                ⚠️ Stock low! You should reorder <strong>{recommended} units</strong>.
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            """
            <div style="
                background-color:#D1FADF;
                padding:15px;
                border-radius:10px;
                border-left:6px solid #12B76A;
                font-size:18px;
                font-weight:600;
            ">
                ✔️ Stock is sufficient. No reorder needed.
            </div>
            """,
            unsafe_allow_html=True
        )
