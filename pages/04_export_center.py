"""Export center page."""

import streamlit as st

from src.ai import build_evidence_linked_summary
from src.config import DEFAULT_SYMBOL
from src.data import fetch_company_financials, is_valid_a_share_symbol
from src.export import build_company_pdf_report, build_company_workbook
from src.metrics import add_financial_metrics
from src.risk import evaluate_risks
from src.ui.layout import configure_page
from src.ui.source_status import render_data_source_status


@st.cache_data(show_spinner=False)
def load_export_payload(symbol: str):
    result = fetch_company_financials(symbol)
    metrics = add_financial_metrics(result.data)
    signals = evaluate_risks(metrics)
    summary = build_evidence_linked_summary(metrics, signals)
    workbook = build_company_workbook(metrics, signals)
    pdf_report = build_company_pdf_report(
        metrics_df=metrics,
        signals=signals,
        summary=summary,
        data_source=result.source,
    )
    return result, metrics, signals, workbook, pdf_report


def render() -> None:
    configure_page("导出中心")
    st.title("导出中心")

    symbol = st.text_input("A股代码", value=DEFAULT_SYMBOL)
    if not is_valid_a_share_symbol(symbol):
        st.info("请输入有效的 6 位 A 股代码，例如 600519、002594、300750。")
        st.stop()
    result, metrics, signals, workbook, pdf_report = load_export_payload(symbol)
    render_data_source_status(result.source, result.warning)

    latest = metrics.sort_values("year").iloc[-1]
    base_file_name = f"{symbol}_{int(latest['year'])}_financial_risk_analysis"

    st.download_button(
        "下载财务指标与风险信号 Excel",
        data=workbook,
        file_name=f"{base_file_name}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )

    st.download_button(
        "下载一页式公司风险报告 PDF",
        data=pdf_report,
        file_name=f"{base_file_name}.pdf",
        mime="application/pdf",
    )

    st.caption("PDF 报告复用公司分析页的证据绑定摘要，不重新计算指标或风险规则。")


if __name__ == "__main__":
    render()
