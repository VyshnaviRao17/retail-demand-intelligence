import streamlit as st

def _inject_card_css():
    css = """
    <style>

    .metric-card {
        padding: 18px;
        border-radius: 16px;
        text-align: center;
        background: white;
        margin-bottom: 18px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        transition: all 0.25s ease;
    }

    .metric-card:hover {
        transform: translateY(-6px) scale(1.03);
        box-shadow: 0 12px 30px rgba(0,0,0,0.15);
    }

    .metric-card-blue { border-left: 6px solid #4D96FF; }
    .metric-card-green { border-left: 6px solid #12B76A; }
    .metric-card-red { border-left: 6px solid #FF4D4D; }
    .metric-card-yellow { border-left: 6px solid #F4B740; }

    .metric-card-blue:hover { box-shadow: 0 12px 28px rgba(77,150,255,0.32); }
    .metric-card-green:hover { box-shadow: 0 12px 28px rgba(18,183,106,0.32); }
    .metric-card-red:hover { box-shadow: 0 12px 28px rgba(255,77,77,0.32); }
    .metric-card-yellow:hover { box-shadow: 0 12px 28px rgba(244,183,64,0.32); }

    .metric-title {
        font-size: 17px;
        font-weight: 600;
        color: #1E293B;
    }

    .metric-value {
        font-size: 28px;
        font-weight: 700;
        margin-top: 4px;
    }

    .metric-icon {
        font-size: 30px;
        opacity: 0.85;
        margin-top: 6px;
    }

    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


def metric_card(title, value, icon="📊", variant="blue"):
    if not st.session_state.get("_metric_card_css_loaded", False):
        _inject_card_css()
        st.session_state["_metric_card_css_loaded"] = True

    color_class = f"metric-card-{variant}"

    html = f"""
    <div class="metric-card {color_class}">
        <div class="metric-title">{title}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-icon">{icon}</div>
    </div>
    """

    st.markdown(html, unsafe_allow_html=True)
