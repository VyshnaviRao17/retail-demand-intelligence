import streamlit as st
import pandas as pd
from fpdf import FPDF
import io

# ---------- CSV EXPORT ----------
def export_csv(df):
    return df.to_csv(index=False).encode("utf-8")


# ---------- JSON EXPORT ----------
def export_json(data):
    import json
    return json.dumps(data, indent=4).encode("utf-8")


# ---------- EXCEL EXPORT ----------
def export_excel(history_df, forecast_df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        history_df.to_excel(writer, index=False, sheet_name="History")
        forecast_df.to_excel(writer, index=False, sheet_name="Forecast")
    return output.getvalue()


# ---------- PDF EXPORT ----------
def export_pdf(forecast_json, anomalies_df):
    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial", size=16)
    pdf.cell(200, 10, txt="Retail Demand Intelligence Report", ln=True, align="C")

    pdf.set_font("Arial", size=12)
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Store: {forecast_json['store']}", ln=True)
    pdf.cell(200, 10, txt=f"SKU: {forecast_json['sku']}", ln=True)

    pdf.ln(5)
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 8, txt="Forecast Summary:", ln=True)

    forecast_values = forecast_json["forecast_values"]
    pdf.cell(200, 8, txt=f"Next 3 Days: {sum(forecast_values[:3])}", ln=True)
    pdf.cell(200, 8, txt=f"Next 7 Days: {sum(forecast_values[:7])}", ln=True)
    pdf.cell(200, 8, txt=f"Next 14 Days: {sum(forecast_values[:14])}", ln=True)

    pdf.ln(10)
    pdf.cell(200, 8, txt="Anomaly Count: " + str(len(anomalies_df)), ln=True)

    pdf_output = pdf.output(dest="S").encode("latin1")
    return pdf_output
