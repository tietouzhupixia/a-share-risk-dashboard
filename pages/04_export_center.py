"""Export center page."""

import streamlit as st

from src.config import DEFAULT_SYMBOL
from src.data import fetch_company_financials
from src.export import build_company_workbook
from src.metrics import add_financial_metrics
from src.risk import evaluate_risks
from src.ui.layout import configure_page
from src.ui.source_status import render_data_source_status


@st.cache_data(show_spinner=False)
def load_export_payload(symbol: str):
    result = fetch_company_financials(symbol)
    metrics = add_financial_metrics(result.data)
    signals = evaluate_risks(metrics)
    workbook = build_company_workbook(metrics, signals)
    return result, metrics, signals, workbook


def render() -> None:
    configure_page("导出中心")
    st.title("导出中心")

    symbol = st.text_input("A股代码", value=DEFAULT_SYMBOL)
    result, metrics, signals, workbook = load_export_payload(symbol)
    render_data_source_status(result.source, result.warning)

    latest = metrics.sort_values("year").iloc[-1]
    file_name = f"{symbol}_{int(latest['year'])}_financial_risk_analysis.xlsx"

    st.download_button(
        "下载财务指标与风险信号 Excel",
        data=workbook,
        file_name=file_name,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )

    st.caption("PDF 和图表图片导出会在 Excel 口径稳定后接入。")


if __name__ == "__main__":
    render()
