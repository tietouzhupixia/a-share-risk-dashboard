from src.data.sample_data import load_sample_financials
from src.metrics import add_financial_metrics


def test_add_financial_metrics_smoke():
    metrics = add_financial_metrics(load_sample_financials())

    assert "revenue_growth" in metrics.columns
    assert "asset_liability_ratio" in metrics.columns
    assert "ar_turnover_days" in metrics.columns
    assert len(metrics) >= 3

