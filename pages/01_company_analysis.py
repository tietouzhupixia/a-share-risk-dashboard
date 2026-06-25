"""Company analysis page."""

import streamlit as st

from src.ai import build_rule_based_summary
from src.config import DEFAULT_SYMBOL
from src.data import fetch_company_financials, is_valid_a_share_symbol
from src.metrics import add_financial_metrics
from src.risk import evaluate_risks
from src.ui.charts import line_chart
from src.ui.layout import configure_page, format_number, format_percent
from src.ui.source_status import render_data_source_status


@st.cache_data(show_spinner=False)
def load_company(symbol: str):
    result = fetch_company_financials(symbol)
    metrics = add_financial_metrics(result.data)
    signals = evaluate_risks(metrics)
    return result, metrics, signals


def render() -> None:
    configure_page("公司分析")
    st.title("公司分析")

    symbol = st.text_input("A股代码", value=DEFAULT_SYMBOL, help="示例：002594、300750、600519")
    if not is_valid_a_share_symbol(symbol):
        st.info("请输入有效的 6 位 A 股代码，例如 600519、002594、300750。")
        st.stop()
    result, metrics, signals = load_company(symbol)
    render_data_source_status(result.source, result.warning)

    latest = metrics.sort_values("year").iloc[-1]
    st.subheader(f"{latest['company_name']} - {int(latest['year'])} 财务健康概览")

    cols = st.columns(4)
    cols[0].metric("营业收入增长率", format_percent(latest["revenue_growth"]))
    cols[1].metric("净利润增长率", format_percent(latest["net_profit_growth"]))
    cols[2].metric("ROA", format_percent(latest["roa"]))
    cols[3].metric("资产负债率", format_percent(latest["asset_liability_ratio"]))

    cols = st.columns(4)
    cols[0].metric("经营现金流/净利润", f"{latest['ocf_to_profit']:.2f}")
    cols[1].metric("应收账款/营收", format_percent(latest["ar_to_revenue"]))
    cols[2].metric("存货/营收", format_percent(latest["inventory_to_revenue"]))
    cols[3].metric("应收周转天数", f"{latest['ar_turnover_days']:.1f}")

    st.subheader("趋势图")
    left, right = st.columns(2)
    left.plotly_chart(
        line_chart(metrics, ["revenue", "net_profit"], "营业收入与净利润趋势"),
        use_container_width=True,
    )
    right.plotly_chart(
        line_chart(
            metrics,
            ["operating_cash_flow", "net_profit"],
            "经营现金流与净利润对比",
        ),
        use_container_width=True,
    )

    left, right = st.columns(2)
    left.plotly_chart(
        line_chart(metrics, ["ar_to_revenue", "inventory_to_revenue"], "营运资本占收入比例"),
        use_container_width=True,
    )
    right.plotly_chart(
        line_chart(
            metrics,
            ["accounts_receivable_growth", "revenue_growth"],
            "应收账款增速 vs 营收增速",
        ),
        use_container_width=True,
    )

    st.subheader("AI/规则摘要")
    st.write(build_rule_based_summary(metrics, signals))

    st.subheader("年度指标明细")
    display_columns = [
        "year",
        "revenue",
        "net_profit",
        "operating_cash_flow",
        "revenue_growth",
        "net_profit_growth",
        "asset_liability_ratio",
        "ar_to_revenue",
        "ar_turnover_days",
    ]
    st.dataframe(metrics[display_columns], use_container_width=True)

    st.caption(f"最新营业收入：{format_number(latest['revenue'])}")


if __name__ == "__main__":
    render()
