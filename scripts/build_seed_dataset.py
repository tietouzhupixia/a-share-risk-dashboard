"""Build/refresh the committed seed dataset for the company universe.

Pulls live AKShare data for each universe symbol, normalizes it, and writes it to
`data/seed/financials/<code>.csv` (committed to Git). One command refreshes the
whole snapshot, so the deployed app serves real data without any live round-trip.

Usage:
    python -m scripts.build_seed_dataset                 # whole universe
    python -m scripts.build_seed_dataset 600519 000333   # specific symbols
    python -m scripts.build_seed_dataset --retries 5 --format json
"""

from __future__ import annotations

import argparse
import json
import time
from collections.abc import Callable, Iterable
from typing import Any

import pandas as pd

from src.data.akshare_client import fetch_live_financials
from src.data.seed import write_seed_financials
from src.data.universe import get_company, universe_codes

Fetcher = Callable[[str], pd.DataFrame]
Writer = Callable[[str, pd.DataFrame], Any]

DISPLAY_COLUMNS = (
    "symbol",
    "company_name",
    "status",
    "rows",
    "year_start",
    "year_end",
    "error",
)


def build_seed_for_symbol(
    code: str,
    *,
    fetcher: Fetcher = fetch_live_financials,
    writer: Writer = write_seed_financials,
    retries: int = 3,
    sleep_seconds: float = 0.0,
) -> dict[str, Any]:
    """Fetch one symbol live (with retries) and write its seed snapshot."""

    company = get_company(code)
    name = company.name if company else code

    last_error = ""
    for attempt in range(1, max(1, retries) + 1):
        try:
            data = fetcher(code)
            if data is None or data.empty:
                raise RuntimeError("empty result")
            data = data.copy()
            data["symbol"] = code
            if company is not None:
                # Universe is the source of truth for names; live sources (esp. Sina)
                # may omit the company name and otherwise fall back to the bare code.
                data["company_name"] = company.name
            writer(code, data)
            years = pd.to_numeric(data.get("year", pd.Series(dtype="float64")), errors="coerce").dropna()
            return {
                "symbol": code,
                "company_name": name,
                "status": "ok",
                "rows": int(len(data)),
                "year_start": int(years.min()) if not years.empty else "n/a",
                "year_end": int(years.max()) if not years.empty else "n/a",
                "error": "",
            }
        except Exception as exc:
            last_error = f"{type(exc).__name__}: {exc}"
            if attempt < retries and sleep_seconds:
                time.sleep(sleep_seconds)

    return {
        "symbol": code,
        "company_name": name,
        "status": "failed",
        "rows": 0,
        "year_start": "n/a",
        "year_end": "n/a",
        "error": last_error,
    }


def build_seed_dataset(
    codes: Iterable[str] | None = None,
    *,
    fetcher: Fetcher = fetch_live_financials,
    writer: Writer = write_seed_financials,
    retries: int = 3,
    sleep_seconds: float = 0.0,
) -> list[dict[str, Any]]:
    """Build seed snapshots for many symbols; return one report row per symbol."""

    target_codes = list(codes) if codes is not None else universe_codes()
    rows: list[dict[str, Any]] = []
    for code in target_codes:
        rows.append(
            build_seed_for_symbol(
                code, fetcher=fetcher, writer=writer, retries=retries, sleep_seconds=sleep_seconds
            )
        )
    return rows


def format_markdown_table(rows: list[dict[str, Any]]) -> str:
    header = "| " + " | ".join(DISPLAY_COLUMNS) + " |"
    separator = "| " + " | ".join("---" for _ in DISPLAY_COLUMNS) + " |"
    body = [
        "| " + " | ".join(str(row.get(col, "")).replace("|", "\\|") for col in DISPLAY_COLUMNS) + " |"
        for row in rows
    ]
    return "\n".join([header, separator, *body])


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("symbols", nargs="*", help="Specific six-digit codes; default = whole universe")
    parser.add_argument("--retries", type=int, default=3)
    parser.add_argument("--sleep", type=float, default=1.0, help="Seconds between retries")
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    args = parser.parse_args()

    codes = args.symbols or None
    rows = build_seed_dataset(codes, retries=args.retries, sleep_seconds=args.sleep)

    if args.format == "json":
        print(json.dumps(rows, ensure_ascii=False, indent=2))
    else:
        print(format_markdown_table(rows))

    ok = sum(1 for row in rows if row["status"] == "ok")
    print(f"\nseed build summary: {ok}/{len(rows)} ok")


if __name__ == "__main__":
    main()
