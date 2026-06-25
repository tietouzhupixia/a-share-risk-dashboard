from io import BytesIO

import pandas as pd
from pypdf import PdfReader

from src.ai.summary import build_evidence_linked_summary
from src.export.pdf_exporter import build_company_pdf_report
from src.risk.rules import RiskSignal


def test_build_company_pdf_report_contains_summary_evidence_and_disclaimer():
    metrics = pd.DataFrame(
        [
            {
                "symbol": "002594",
                "company_name": "比亚迪",
                "year": 2025,
                "revenue_growth": 0.08,
                "net_profit_growth": 0.12,
                "roa": 0.04,
                "asset_liability_ratio": 0.72,
                "ocf_to_profit": 0.90,
                "ar_to_revenue": 0.10,
                "inventory_to_revenue": 0.18,
                "ar_turnover_days": 36.5,
            }
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

    pdf_bytes = build_company_pdf_report(
        metrics_df=metrics,
        signals=signals,
        summary=summary,
        data_source="seed:normalized",
    )

    assert pdf_bytes.startswith(b"%PDF")

    reader = PdfReader(BytesIO(pdf_bytes))
    text = "\n".join(page.extract_text() or "" for page in reader.pages)

    assert "比亚迪" in text
    assert "seed:normalized" in text
    assert "E1" in text
    assert "资产负债率偏高" in text
    assert "不构成投资建议" in text
