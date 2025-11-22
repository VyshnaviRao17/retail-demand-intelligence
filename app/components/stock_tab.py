import streamlit as st
from components.ui_components import metric_card


def render_stock_tab(forecast_json):
    st.subheader("📦 Smart Stock Advisor")

    # Immutable local copy to avoid triggering re-runs
    forecast_values = tuple(float(v) for v in forecast_json["forecast_values"])

    # ------------------------------
    # INPUTS (User interaction only)
    # ------------------------------
    st.markdown("### 📥 Input Parameters")

    c1, c2, c3 = st.columns(3)

    # These widgets cause reruns, but calculations are extremely small, so it's fine
    current_stock = c1.number_input("Current Stock", value=50, min_value=0)
    lead_time = int(c2.number_input("Lead Time (days)", value=7, min_value=1))
    safety_pct = c3.slider("Safety Stock (%)", 0, 50, 15)

    # ------------------------------
    # COMPUTATION (Very lightweight)
    # ------------------------------
    lead_time = min(lead_time, len(forecast_values))  # Prevent out-of-range
    demand_next = sum(forecast_values[:lead_time])
    safety_stock = int(demand_next * (safety_pct / 100))
    recommended = max(0, int(demand_next + safety_stock - current_stock))

    # ------------------------------
    # KPI CARDS
    # ------------------------------
    st.markdown("### 📊 Stock Summary")

    k1, k2, k3 = st.columns(3)

    with k1:
        metric_card("Demand (Lead Time)", int(demand_next), "📈", "blue")

    with k2:
        metric_card("Safety Stock", safety_stock, "🛡️", "yellow")

    with k3:
        metric_card(
            "Recommended Reorder",
            recommended,
            "📦",
            "red" if recommended > 0 else "green",
        )

    # ------------------------------
    # SYSTEM RECOMMENDATION BOX
    # ------------------------------
    st.markdown("### 🧠 System Recommendation")

    if recommended > 0:
        st.markdown(
            f"""
            <div style="
                background-color:#FFF3CD;
                padding:16px;
                border-radius:12px;
                border-left:6px solid #FFCD39;
                font-size:17px;
                font-weight:600;
            ">
                ⚠️ Stock low! You should reorder <strong>{recommended} units</strong>.
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            """
            <div style="
                background-color:#D1FADF;
                padding:16px;
                border-radius:12px;
                border-left:6px solid #12B76A;
                font-size:17px;
                font-weight:600;
            ">
                ✔️ Stock is sufficient. No reorder needed.
            </div>
            """,
            unsafe_allow_html=True,
        )
