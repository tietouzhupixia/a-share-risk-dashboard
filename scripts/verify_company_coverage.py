"""Verify live/cache/sample data coverage for recommended A-share symbols."""

from __future__ import annotations

import argparse
import json
from collections.abc import Iterable
from typing import Any

import pandas as pd

from src.data.akshare_client import fetch_company_financials
from src.data.schema import FinancialDataResult
from src.metrics.financial_metrics import add_financial_metrics
from src.risk.rules import evaluate_risks


TARGET_SYMBOLS = ("600519", "002594", "300750")
CORE_FIELDS = (
    "revenue",
    "net_profit",
    "operating_cash_flow",
    "accounts_receivable",
    "inventory",
    "total_assets",
    "total_liabilities",
    "gross_profit",
    "short_term_borrowing",
)
DISPLAY_COLUMNS = (
    "symbol",
    "company_name",
    "source",
    "rows",
    "year_start",
    "year_end",
    "missing_core_fields",
    "risk_signal_count",
    "warning",
)


def summarize_financial_result(symbol: str, result: FinancialDataResult) -> dict[str, Any]:
    """Return a compact coverage summary for one normalized financial result."""

    data = result.data.copy()
    years = pd.to_numeric(data.get("year", pd.Series(dtype="float64")), errors="coerce").dropna()

    company_name = symbol
    if "company_name" in data.columns and data["company_name"].notna().any():
        company_name = str(data["company_name"].dropna().iloc[0])

    risk_signal_count: int | str = "n/a"
    if not data.empty:
        try:
            metrics = add_financial_metrics(data)
            risk_signal_count = len(evaluate_risks(metrics))
        except Exception as exc:  # pragma: no cover - diagnostic script guard
            risk_signal_count = f"{type(exc).__name__}: {exc}"

    return {
        "symbol": symbol,
        "company_name": company_name,
        "source": result.source,
        "rows": int(len(data)),
        "year_start": int(years.min()) if not years.empty else "n/a",
        "year_end": int(years.max()) if not years.empty else "n/a",
        "missing_core_fields": _missing_core_fields(data),
        "risk_signal_count": risk_signal_count,
        "warning": result.warning or "",
    }


def verify_symbols(symbols: Iterable[str] = TARGET_SYMBOLS) -> list[dict[str, Any]]:
    """Fetch and summarize each symbol using the app's public data API."""

    summaries: list[dict[str, Any]] = []
    for symbol in symbols:
        result = fetch_company_financials(symbol)
        summaries.append(summarize_financial_result(symbol, result))
    return summaries


def format_markdown_table(rows: list[dict[str, Any]]) -> str:
    """Format coverage summaries as a GitHub-friendly Markdown table."""

    header = "| " + " | ".join(DISPLAY_COLUMNS) + " |"
    separator = "| " + " | ".join("---" for _ in DISPLAY_COLUMNS) + " |"
    body = [
        "| " + " | ".join(_markdown_cell(row.get(column, "")) for column in DISPLAY_COLUMNS) + " |"
        for row in rows
    ]
    return "\n".join([header, separator, *body])


def _missing_core_fields(data: pd.DataFrame) -> str:
    missing = [
        field
        for field in CORE_FIELDS
        if field not in data.columns or pd.to_numeric(data[field], errors="coerce").isna().all()
    ]
    return ", ".join(missing) if missing else "none"


def _markdown_cell(value: Any) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("symbols", nargs="*", default=list(TARGET_SYMBOLS))
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    args = parser.parse_args()

    summaries = verify_symbols(args.symbols)
    if args.format == "json":
        print(json.dumps(summaries, ensure_ascii=False, indent=2))
    else:
        print(format_markdown_table(summaries))


if __name__ == "__main__":
    main()
