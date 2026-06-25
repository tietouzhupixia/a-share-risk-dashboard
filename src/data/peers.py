"""Real industry peer snapshots built from the committed seed dataset.

For a company in the curated universe, gather its same-industry peers, compute
the standard metrics from each peer's seed financials, and take the latest year.
This replaces the hand-written demo peer table with real public data.
"""

from __future__ import annotations

import pandas as pd

from src.data.seed import read_seed_financials
from src.data.universe import companies_in_industry, get_company
from src.metrics.financial_metrics import add_financial_metrics

PEER_METRICS = (
    "revenue_growth",
    "roa",
    "asset_liability_ratio",
    "ocf_to_profit",
    "ar_to_revenue",
)


def build_peer_snapshot(code: str) -> pd.DataFrame | None:
    """Return a latest-year peer-metric table for the company's industry.

    Returns None when the code is outside the universe or fewer than two
    same-industry peers have seed data (so the caller can fall back to sample).
    """

    company = get_company(code)
    if company is None:
        return None

    rows: list[dict] = []
    for peer in companies_in_industry(company.industry):
        financials = read_seed_financials(peer.code)
        if financials is None or financials.empty:
            continue
        metrics = add_financial_metrics(financials)
        latest = metrics.sort_values("year").iloc[-1]
        row = {"symbol": peer.code, "company_name": peer.name, "industry": peer.industry}
        for metric in PEER_METRICS:
            value = latest.get(metric)
            row[metric] = float(value) if pd.notna(value) else None
        rows.append(row)

    if len(rows) < 2:
        return None
    return pd.DataFrame(rows)
