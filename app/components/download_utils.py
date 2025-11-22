import pandas as pd
from fpdf import FPDF
import io
import json


# -----------------------------------------------------
# FAST CSV EXPORT
# -----------------------------------------------------
def export_csv(df: pd.DataFrame) -> bytes:
    """
    Return CSV as UTF-8 encoded bytes.
    Small + fast.
    """
    return df.to_csv(index=False).encode("utf-8")


# -----------------------------------------------------
# FAST JSON EXPORT
# -----------------------------------------------------
def export_json(data: dict) -> bytes:
    """
    Pretty-print JSON for download.
    """
    return json.dumps(data, indent=4).encode("utf-8")


# -----------------------------------------------------
# FAST EXCEL EXPORT (History + Forecast)
# -----------------------------------------------------
def export_excel(history_df: pd.DataFrame, forecast_df: pd.DataFrame) -> bytes:
    """
    Generate Excel file in memory using xlsxwriter.
    VERY fast and memory-safe.
    """
    output = io.BytesIO()

    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        if not history_df.empty:
            history_df.to_excel(writer, index=False, sheet_name="History")
        forecast_df.to_excel(writer, index=False, sheet_name="Forecast")

    return output.getvalue()


# -----------------------------------------------------
# OPTIMIZED PDF EXPORT
# -----------------------------------------------------
def export_pdf(forecast_json: dict, anomalies_df: pd.DataFrame) -> bytes:
    """
    Lightweight, optimized PDF generator.
    Fast because:
    - No images
    - No loops
    - Minimal fonts
    """

    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # ---------- HEADER ----------
    pdf.set_font("Arial", "B", 18)
    pdf.cell(0, 12, txt="Retail Demand Intelligence Report", ln=True, align="C")

    pdf.ln(6)

    # ---------- STORE DETAILS ----------
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 8, txt=f"Store: {forecast_json['store']}", ln=True)
    pdf.cell(0, 8, txt=f"SKU: {forecast_json['sku']}", ln=True)

    pdf.ln(4)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, txt="Forecast Summary", ln=True)

    forecast_values = forecast_json["forecast_values"]

    pdf.set_font("Arial", size=11)
    pdf.cell(0, 7, txt=f"Next 3 Days: {round(sum(forecast_values[:3]), 2)}", ln=True)
    pdf.cell(0, 7, txt=f"Next 7 Days: {round(sum(forecast_values[:7]), 2)}", ln=True)
    pdf.cell(0, 7, txt=f"Next 14 Days: {round(sum(forecast_values[:14]), 2)}", ln=True)

    # ---------- ANOMALIES ----------
    pdf.ln(6)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, txt="Anomaly Analysis", ln=True)

    pdf.set_font("Arial", size=11)
    pdf.cell(0, 7, txt=f"Total Anomalies: {len(anomalies_df)}", ln=True)

    # ---------- END ----------
    pdf.ln(6)
    pdf.set_font("Arial", size=9)
    pdf.cell(0, 6, txt="Generated automatically by the Retail Demand Intelligence AI System.", ln=True, align="C")

    # Return PDF bytes
    return pdf.output(dest="S").encode("latin1")
