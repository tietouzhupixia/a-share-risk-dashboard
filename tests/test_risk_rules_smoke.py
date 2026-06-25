from src.data.sample_data import load_sample_financials
from src.metrics import add_financial_metrics
from src.risk import evaluate_risks


def test_evaluate_risks_returns_signal_contract():
    metrics = add_financial_metrics(load_sample_financials())
    signals = evaluate_risks(metrics)

    assert signals
    first = signals[0].to_dict()
    assert {"rule_id", "name", "level", "reason", "evidence", "interpretation"} <= set(first)

