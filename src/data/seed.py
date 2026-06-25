"""Committed seed dataset layer.

Unlike `data/cache/` (local, ephemeral, git-ignored), the seed dataset under
`data/seed/financials/<code>.csv` is a curated, version-controlled snapshot of
normalized public financials. It sits at the top of the fetch fallback chain so
the app — including the clean Streamlit Cloud environment — always serves real
data without depending on a live AKShare round-trip.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.config import SEED_DIR
from src.data.schema import ensure_standard_columns

FINANCIALS_DIR = SEED_DIR / "financials"


def seed_path(code: str) -> Path:
    """Return the seed CSV path for a six-digit code."""

    safe_code = code.strip().replace("/", "_").replace("\\", "_")
    return FINANCIALS_DIR / f"{safe_code}.csv"


def has_seed(code: str) -> bool:
    """Return True if a non-empty seed file exists for this code."""

    path = seed_path(code)
    return path.exists() and path.stat().st_size > 0


def read_seed_financials(code: str) -> pd.DataFrame | None:
    """Read the committed seed snapshot for a code, or None if absent/empty.

    `symbol` and `company_name` are read as strings so six-digit codes keep their
    leading zeros (e.g. ``000895`` must not be coerced to ``895``).
    """

    path = seed_path(code)
    if not path.exists():
        return None
    df = pd.read_csv(path, dtype={"symbol": str, "company_name": str})
    if df.empty:
        return None
    if "symbol" in df.columns:
        df["symbol"] = df["symbol"].astype(str).str.strip().str.zfill(6)
    return ensure_standard_columns(df)


def write_seed_financials(code: str, df: pd.DataFrame) -> Path:
    """Standardize and write a seed snapshot for a code; return the path."""

    FINANCIALS_DIR.mkdir(parents=True, exist_ok=True)
    standardized = ensure_standard_columns(df)
    path = seed_path(code)
    standardized.to_csv(path, index=False, encoding="utf-8-sig")
    return path
