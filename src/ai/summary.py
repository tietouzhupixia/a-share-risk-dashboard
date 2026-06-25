"""Evidence-first narrative summaries."""

import pandas as pd

from src.risk.rules import RiskSignal


def _pct(value: float) -> str:
    if pd.isna(value):
        return "N/A"
    return f"{value:.1%}"


def build_rule_based_summary(metrics_df: pd.DataFrame, signals: list[RiskSignal]) -> str:
    """Build a concise evidence-based summary without calling an LLM."""

    if metrics_df.empty:
        return "暂无可用财务数据，无法生成摘要。"

    latest = metrics_df.sort_values("year").iloc[-1]
    high_count = sum(signal.level == "High" for signal in signals)
    medium_count = sum(signal.level == "Medium" for signal in signals)
    leading_signal = signals[0].name if signals else "未触发明显风险规则"

    return (
        f"{latest['company_name']}在{int(latest['year'])}年营业收入同比增长"
        f"{_pct(latest['revenue_growth'])}，净利润同比增长{_pct(latest['net_profit_growth'])}。"
        f"最新资产负债率为{_pct(latest['asset_liability_ratio'])}，经营现金流/净利润为"
        f"{latest['ocf_to_profit']:.2f}，应收账款/营业收入为{_pct(latest['ar_to_revenue'])}。"
        f"当前透明规则共触发{high_count}个高风险信号和{medium_count}个中风险信号，"
        f"最需要关注的是：{leading_signal}。这些信号不构成投资建议，"
        f"但可作为进一步核查回款效率、营运资本和债务结构的线索。"
    )

