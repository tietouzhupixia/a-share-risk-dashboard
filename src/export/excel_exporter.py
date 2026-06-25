"""Excel export utilities."""

from io import BytesIO

import pandas as pd

from src.risk.rules import RiskSignal


def build_company_workbook(metrics_df: pd.DataFrame, signals: list[RiskSignal]) -> bytes:
    """Return an Excel workbook as bytes for Streamlit download buttons."""

    output = BytesIO()
    risk_df = pd.DataFrame([signal.to_dict() for signal in signals])

    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        metrics_df.to_excel(writer, sheet_name="financial_metrics", index=False)
        risk_df.to_excel(writer, sheet_name="risk_signals", index=False)

    output.seek(0)
    return output.read()

