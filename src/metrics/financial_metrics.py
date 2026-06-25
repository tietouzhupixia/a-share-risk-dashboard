"""Financial metric construction."""

import numpy as np
import pandas as pd


def safe_divide(numerator: pd.Series, denominator: pd.Series) -> pd.Series:
    """Vectorized division that returns NaN for zero or missing denominators."""

    clean_denominator = denominator.replace(0, np.nan)
    return numerator / clean_denominator


def add_financial_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """Add standard financial health and risk-monitoring metrics."""

    result = df.sort_values("year").copy()

    result["revenue_growth"] = result["revenue"].pct_change()
    result["net_profit_growth"] = result["net_profit"].pct_change()
    result["accounts_receivable_growth"] = result["accounts_receivable"].pct_change()
    result["inventory_growth"] = result["inventory"].pct_change()
    result["short_term_borrowing_growth"] = result["short_term_borrowing"].pct_change()

    result["roa"] = safe_divide(result["net_profit"], result["total_assets"])
    result["asset_liability_ratio"] = safe_divide(result["total_liabilities"], result["total_assets"])
    result["ocf_to_profit"] = safe_divide(result["operating_cash_flow"], result["net_profit"])
    result["ar_to_revenue"] = safe_divide(result["accounts_receivable"], result["revenue"])
    result["inventory_to_revenue"] = safe_divide(result["inventory"], result["revenue"])
    result["ar_turnover_days"] = result["ar_to_revenue"] * 365
    result["gross_margin"] = safe_divide(result["gross_profit"], result["revenue"])
    result["net_margin"] = safe_divide(result["net_profit"], result["revenue"])

    return result

