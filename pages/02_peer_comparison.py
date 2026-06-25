"""Peer comparison page."""

import streamlit as st

from src.config import DEFAULT_SYMBOL
from src.data import fetch_peer_snapshot, is_valid_a_share_symbol
from src.ui.charts import peer_bar_chart
from src.ui.layout import configure_page, format_percent
from src.ui.source_status import render_data_source_status


@st.cache_data(show_spinner=False)
def load_peers(symbol: str):
    return fetch_peer_snapshot(symbol)


def render() -> None:
    configure_page("同业比较")
    st.title("同业比较")

    symbol = st.text_input("A股代码", value=DEFAULT_SYMBOL)
    if not is_valid_a_share_symbol(symbol):
        st.info("请输入有效的 6 位 A 股代码，例如 600519、002594、300750。")
        st.stop()
    result = load_peers(symbol)
    peer_df = result.data

    render_data_source_status(result.source, result.warning)

    metric = st.selectbox(
        "比较指标",
        ["ar_to_revenue", "roa", "asset_liability_ratio", "ocf_to_profit", "revenue_growth"],
        format_func={
            "ar_to_revenue": "应收账款/营收",
            "roa": "ROA",
            "asset_liability_ratio": "资产负债率",
            "ocf_to_profit": "经营现金流/净利润",
            "revenue_growth": "收入增长率",
        }.get,
    )

    st.plotly_chart(peer_bar_chart(peer_df, metric, "同业指标比较"), use_container_width=True)

    table = peer_df.copy()
    for column in ["ar_to_revenue", "roa", "asset_liability_ratio", "revenue_growth"]:
        table[column] = table[column].map(format_percent)
    st.dataframe(table, use_container_width=True)


if __name__ == "__main__":
    render()

