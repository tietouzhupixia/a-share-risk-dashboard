"""Standard data contracts for annual financial data."""

from dataclasses import dataclass

import pandas as pd

STANDARD_FINANCIAL_COLUMNS = [
    "symbol",
    "company_name",
    "year",
    "revenue",
    "net_profit",
    "operating_cash_flow",
    "accounts_receivable",
    "inventory",
    "total_assets",
    "total_liabilities",
    "gross_profit",
    "short_term_borrowing",
]


@dataclass(frozen=True)
class FinancialDataResult:
    """Container returned by data-source functions."""

    data: pd.DataFrame
    source: str
    warning: str | None = None


def ensure_standard_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Return a copy with all standard columns present and ordered first."""

    result = df.copy()
    for column in STANDARD_FINANCIAL_COLUMNS:
        if column not in result.columns:
            result[column] = pd.NA

    ordered = STANDARD_FINANCIAL_COLUMNS + [
        column for column in result.columns if column not in STANDARD_FINANCIAL_COLUMNS
    ]
    return result[ordered]

