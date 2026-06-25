"""Transparent rule-based risk alerts."""

from dataclasses import asdict, dataclass

import pandas as pd


@dataclass(frozen=True)
class RiskSignal:
    rule_id: str
    name: str
    level: str
    reason: str
    evidence: dict
    interpretation: str

    def to_dict(self) -> dict:
        return asdict(self)


def _recent(df: pd.DataFrame, n: int = 2) -> pd.DataFrame:
    return df.sort_values("year").tail(n)


def evaluate_risks(metrics_df: pd.DataFrame) -> list[RiskSignal]:
    """Evaluate transparent financial risk signals."""

    if metrics_df.empty:
        return []

    df = metrics_df.sort_values("year").copy()
    latest = df.iloc[-1]
    signals: list[RiskSignal] = []

    recent_two = _recent(df, 2)
    ar_pressure = (
        recent_two["accounts_receivable_growth"] > recent_two["revenue_growth"]
    ).fillna(False)
    if len(recent_two) == 2 and ar_pressure.all():
        signals.append(
            RiskSignal(
                rule_id="AR_GROWTH_GT_REVENUE_2Y",
                name="应收账款增速连续高于收入增速",
                level="High",
                reason="最近两年应收账款增速均高于营业收入增速。",
                evidence={
                    "years": recent_two["year"].tolist(),
                    "revenue_growth": recent_two["revenue_growth"].round(4).tolist(),
                    "accounts_receivable_growth": recent_two[
                        "accounts_receivable_growth"
                    ].round(4).tolist(),
                },
                interpretation="可能表明收入增长伴随回款压力上升，需要关注信用政策和客户账期。",
            )
        )

    cash_gap = (recent_two["operating_cash_flow"] < recent_two["net_profit"]).fillna(False)
    if len(recent_two) == 2 and cash_gap.all():
        signals.append(
            RiskSignal(
                rule_id="OCF_BELOW_PROFIT_2Y",
                name="经营现金流连续低于净利润",
                level="High",
                reason="最近两年经营现金流量净额均低于净利润。",
                evidence={
                    "years": recent_two["year"].tolist(),
                    "operating_cash_flow": recent_two["operating_cash_flow"].round(0).tolist(),
                    "net_profit": recent_two["net_profit"].round(0).tolist(),
                },
                interpretation="可能表明利润转化为现金的质量偏弱，需要进一步核查回款和营运资本。",
            )
        )

    if latest["asset_liability_ratio"] >= 0.70:
        signals.append(
            RiskSignal(
                rule_id="HIGH_LEVERAGE",
                name="资产负债率偏高",
                level="Medium",
                reason="最新年度资产负债率高于 70%。",
                evidence={
                    "year": int(latest["year"]),
                    "asset_liability_ratio": round(float(latest["asset_liability_ratio"]), 4),
                },
                interpretation="较高杠杆可能放大经营波动对偿债能力的影响。",
            )
        )

    if len(df) >= 2:
        previous = df.iloc[-2]
        gross_margin_drop = latest["gross_margin"] - previous["gross_margin"]
        if gross_margin_drop <= -0.05:
            signals.append(
                RiskSignal(
                    rule_id="GROSS_MARGIN_DROP",
                    name="毛利率明显下降",
                    level="Medium",
                    reason="最新年度毛利率较前一年下降超过 5 个百分点。",
                    evidence={
                        "previous_year": int(previous["year"]),
                        "latest_year": int(latest["year"]),
                        "previous_gross_margin": round(float(previous["gross_margin"]), 4),
                        "latest_gross_margin": round(float(latest["gross_margin"]), 4),
                    },
                    interpretation="可能反映价格压力、成本上升或产品结构变化。",
                )
            )

        if (
            latest["inventory_growth"] > latest["revenue_growth"]
            and latest["revenue_growth"] > 0
        ):
            signals.append(
                RiskSignal(
                    rule_id="INVENTORY_GROWTH_GT_REVENUE",
                    name="存货增长快于收入",
                    level="Medium",
                    reason="最新年度收入增长为正，但存货增速高于收入增速。",
                    evidence={
                        "year": int(latest["year"]),
                        "revenue_growth": round(float(latest["revenue_growth"]), 4),
                        "inventory_growth": round(float(latest["inventory_growth"]), 4),
                    },
                    interpretation="可能提示备货压力、需求预测偏差或库存周转放缓。",
                )
            )

        if latest["short_term_borrowing_growth"] >= 0.30:
            signals.append(
                RiskSignal(
                    rule_id="SHORT_DEBT_JUMP",
                    name="短期借款快速上升",
                    level="Medium",
                    reason="最新年度短期借款增速超过 30%。",
                    evidence={
                        "year": int(latest["year"]),
                        "short_term_borrowing_growth": round(
                            float(latest["short_term_borrowing_growth"]), 4
                        ),
                    },
                    interpretation="可能表明短期融资需求上升，需要结合现金流和债务期限结构判断。",
                )
            )

        if (
            latest["revenue_growth"] > 0
            and latest["ar_turnover_days"] > previous["ar_turnover_days"]
        ):
            signals.append(
                RiskSignal(
                    rule_id="GROWTH_WITH_COLLECTION_PRESSURE",
                    name="收入增长但回款效率下降",
                    level="Medium",
                    reason="最新年度收入增长为正，但应收账款周转天数上升。",
                    evidence={
                        "previous_year": int(previous["year"]),
                        "latest_year": int(latest["year"]),
                        "revenue_growth": round(float(latest["revenue_growth"]), 4),
                        "previous_ar_turnover_days": round(
                            float(previous["ar_turnover_days"]), 2
                        ),
                        "latest_ar_turnover_days": round(float(latest["ar_turnover_days"]), 2),
                    },
                    interpretation="可能表明销售扩张伴随账期拉长，需要关注增长质量。",
                )
            )

    return signals

