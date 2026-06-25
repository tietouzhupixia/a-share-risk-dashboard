import pandas as pd

from src.ai.summary import build_evidence_linked_summary
from src.risk.rules import RiskSignal


def test_evidence_linked_summary_cites_metrics_and_risk_evidence():
    metrics = pd.DataFrame(
        [
            {
                "symbol": "002594",
                "company_name": "比亚迪",
                "year": 2024,
                "revenue_growth": 0.10,
                "net_profit_growth": 0.20,
                "asset_liability_ratio": 0.65,
                "ocf_to_profit": 1.10,
                "ar_to_revenue": 0.08,
                "inventory_to_revenue": 0.15,
                "ar_turnover_days": 29.2,
            },
            {
                "symbol": "002594",
                "company_name": "比亚迪",
                "year": 2025,
                "revenue_growth": 0.08,
                "net_profit_growth": 0.12,
                "asset_liability_ratio": 0.72,
                "ocf_to_profit": 0.90,
                "ar_to_revenue": 0.10,
                "inventory_to_revenue": 0.18,
                "ar_turnover_days": 36.5,
            },
        ]
    )
    signals = [
        RiskSignal(
            rule_id="HIGH_LEVERAGE",
            name="资产负债率偏高",
            level="Medium",
            reason="最新年度资产负债率高于 70%。",
            evidence={"year": 2025, "asset_liability_ratio": 0.72},
            interpretation="较高杠杆可能放大经营波动对偿债能力的影响。",
        )
    ]

    summary = build_evidence_linked_summary(metrics, signals)

    assert "比亚迪" in summary.narrative
    assert "[E1]" in summary.narrative
    assert "[E2]" in summary.narrative
    assert "[E4]" in summary.narrative
    assert "不构成投资建议" in summary.narrative
    assert list(summary.evidence.columns) == [
        "id",
        "conclusion",
        "metric",
        "value",
        "period",
        "source",
    ]
    assert summary.evidence["id"].tolist() == ["E1", "E2", "E3", "E4"]
    assert "营业收入增长率" in summary.evidence.iloc[0]["metric"]
    assert "资产负债率偏高" in summary.evidence.iloc[3]["conclusion"]


def test_evidence_linked_summary_handles_empty_metrics():
    summary = build_evidence_linked_summary(pd.DataFrame(), [])

    assert "暂无可用财务数据" in summary.narrative
    assert summary.evidence.empty
