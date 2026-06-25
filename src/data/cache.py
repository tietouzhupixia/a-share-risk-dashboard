"""Small file-cache helpers for public data pulls."""

from pathlib import Path

import pandas as pd

from src.config import CACHE_DIR


def cache_path(name: str) -> Path:
    """Return a safe cache path under `data/cache`."""

    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    safe_name = name.replace("/", "_").replace("\\", "_").replace(":", "_")
    return CACHE_DIR / safe_name


def read_csv_cache(name: str) -> pd.DataFrame | None:
    """Read a cached CSV if present."""

    path = cache_path(name)
    if not path.exists():
        return None
    return pd.read_csv(path)


def write_csv_cache(name: str, df: pd.DataFrame) -> Path:
    """Write a DataFrame to CSV cache and return the path."""

    path = cache_path(name)
    df.to_csv(path, index=False, encoding="utf-8-sig")
    return path

