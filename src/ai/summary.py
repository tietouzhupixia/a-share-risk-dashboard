"""Evidence-first narrative summaries."""

from dataclasses import dataclass
from typing import Any

import pandas as pd

from src.risk.rules import RiskSignal


EVIDENCE_COLUMNS = ["id", "conclusion", "metric", "value", "period", "source"]
EVIDENCE_LABELS = {
    "years": "年份",
    "year": "年份",
    "previous_year": "前一年",
    "latest_year": "最新年",
    "revenue_growth": "营业收入增长率",
    "accounts_receivable_growth": "应收账款增长率",
    "operating_cash_flow": "经营现金流",
    "net_profit": "净利润",
    "asset_liability_ratio": "资产负债率",
    "previous_gross_margin": "前一年毛利率",
    "latest_gross_margin": "最新年毛利率",
    "inventory_growth": "存货增长率",
    "short_term_borrowing_growth": "短期借款增长率",
    "previous_ar_turnover_days": "前一年应收周转天数",
    "latest_ar_turnover_days": "最新年应收周转天数",
}


@dataclass(frozen=True)
class EvidenceLinkedSummary:
    """Narrative summary plus a table that traces each claim to data."""

    narrative: str
    evidence: pd.DataFrame


def _pct(value: float) -> str:
    if pd.isna(value):
        return "N/A"
    return f"{value:.1%}"


def _number(value: float) -> str:
    if pd.isna(value):
        return "N/A"
    if abs(float(value)) >= 1000:
        return f"{float(value):,.0f}"
    return f"{float(value):.2f}"


def _format_evidence_value(key: str, value: Any) -> str:
    if isinstance(value, list):
        return "[" + ", ".join(_format_evidence_value(key, item) for item in value) + "]"
    if pd.isna(value):
        return "N/A"
    if any(token in key for token in ("growth", "ratio", "margin")):
        return _pct(float(value))
    if key.endswith("days"):
        return f"{float(value):.1f} 天"
    return _number(float(value)) if isinstance(value, int | float) else str(value)


def _format_signal_evidence(evidence: dict) -> str:
    return "；".join(
        f"{EVIDENCE_LABELS.get(key, key)}={_format_evidence_value(key, value)}"
        for key, value in evidence.items()
    )


def build_evidence_linked_summary(
    metrics_df: pd.DataFrame, signals: list[RiskSignal]
) -> EvidenceLinkedSummary:
    """Build a concise non-LLM summary where every conclusion cites evidence IDs."""

    if metrics_df.empty:
        return EvidenceLinkedSummary(
            narrative="暂无可用财务数据，无法生成摘要。",
            evidence=pd.DataFrame(columns=EVIDENCE_COLUMNS),
        )

    latest = metrics_df.sort_values("year").iloc[-1]
    high_count = sum(signal.level == "High" for signal in signals)
    medium_count = sum(signal.level == "Medium" for signal in signals)

    evidence_rows = [
        {
            "id": "E1",
            "conclusion": "收入与盈利变化",
            "metric": "营业收入增长率；净利润增长率",
            "value": (
                f"{_pct(latest['revenue_growth'])}；"
                f"{_pct(latest['net_profit_growth'])}"
            ),
            "period": int(latest["year"]),
            "source": "annual_metrics",
        },
        {
            "id": "E2",
            "conclusion": "现金流质量与杠杆水平",
            "metric": "经营现金流/净利润；资产负债率",
            "value": (
                f"{_number(latest['ocf_to_profit'])}；"
                f"{_pct(latest['asset_liability_ratio'])}"
            ),
            "period": int(latest["year"]),
            "source": "annual_metrics",
        },
        {
            "id": "E3",
            "conclusion": "营运资本占用",
            "metric": "应收账款/营业收入；存货/营业收入；应收周转天数",
            "value": (
                f"{_pct(latest['ar_to_revenue'])}；"
                f"{_pct(latest['inventory_to_revenue'])}；"
                f"{_number(latest['ar_turnover_days'])} 天"
            ),
            "period": int(latest["year"]),
            "source": "annual_metrics",
        },
    ]

    signal_refs: list[str] = []
    for index, signal in enumerate(signals[:3], start=4):
        evidence_id = f"E{index}"
        signal_refs.append(f"{signal.name}[{evidence_id}]")
        evidence_rows.append(
            {
                "id": evidence_id,
                "conclusion": signal.name,
                "metric": signal.reason,
                "value": _format_signal_evidence(signal.evidence),
                "period": "rule_window",
                "source": f"risk_rules:{signal.rule_id}",
            }
        )

    risk_sentence = (
        f"透明规则共触发{high_count}个高风险信号和{medium_count}个中风险信号，"
        f"重点关注{'、'.join(signal_refs)}。"
        if signal_refs
        else "当前未触发透明风险规则，但仍建议结合行业景气度和公司公告继续跟踪。"
    )
    narrative = (
        f"{latest['company_name']}在{int(latest['year'])}年营业收入同比增长"
        f"{_pct(latest['revenue_growth'])}，净利润同比增长{_pct(latest['net_profit_growth'])}[E1]。"
        f"经营现金流/净利润为{_number(latest['ocf_to_profit'])}，资产负债率为"
        f"{_pct(latest['asset_liability_ratio'])}[E2]。"
        f"应收账款/营业收入为{_pct(latest['ar_to_revenue'])}，存货/营业收入为"
        f"{_pct(latest['inventory_to_revenue'])}，应收账款周转天数为"
        f"{_number(latest['ar_turnover_days'])}天[E3]。"
        f"{risk_sentence}以上为基于公开年报口径和透明规则的经营风险提示，"
        f"不构成投资建议。"
    )

    return EvidenceLinkedSummary(
        narrative=narrative,
        evidence=pd.DataFrame(evidence_rows, columns=EVIDENCE_COLUMNS),
    )


def build_rule_based_summary(metrics_df: pd.DataFrame, signals: list[RiskSignal]) -> str:
    """Build a concise evidence-based summary without calling an LLM."""

    return build_evidence_linked_summary(metrics_df, signals).narrative
