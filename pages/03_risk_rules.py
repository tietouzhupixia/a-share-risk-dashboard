"""Risk rule page."""

import pandas as pd
import streamlit as st

from src.config import DEFAULT_SYMBOL
from src.data import fetch_company_financials, is_valid_a_share_symbol
from src.metrics import add_financial_metrics
from src.risk import evaluate_risks
from src.ui.layout import configure_page
from src.ui.source_status import render_data_source_status


@st.cache_data(show_spinner=False)
def load_risks(symbol: str):
    result = fetch_company_financials(symbol)
    metrics = add_financial_metrics(result.data)
    signals = evaluate_risks(metrics)
    return result, metrics, signals


def render() -> None:
    configure_page("风险预警")
    st.title("风险预警")

    symbol = st.text_input("A股代码", value=DEFAULT_SYMBOL)
    if not is_valid_a_share_symbol(symbol):
        st.info("请输入有效的 6 位 A 股代码，例如 600519、002594、300750。")
        st.stop()
    result, metrics, signals = load_risks(symbol)
    render_data_source_status(result.source, result.warning)

    if not signals:
        st.success("当前透明规则未触发明显风险信号。")
        return

    st.subheader("触发信号")
    risk_df = pd.DataFrame([signal.to_dict() for signal in signals])
    st.dataframe(risk_df, use_container_width=True)

    st.subheader("规则证据")
    for signal in signals:
        with st.expander(f"{signal.level} - {signal.name}", expanded=signal.level == "High"):
            st.write(signal.reason)
            st.json(signal.evidence)
            st.write(signal.interpretation)

    st.subheader("指标基础表")
    st.dataframe(metrics, use_container_width=True)


if __name__ == "__main__":
    render()
