"""Tests for the committed seed dataset layer and its fallback precedence."""

import pandas as pd

from src.data import seed
from src.data.akshare_client import fetch_company_financials
from src.data.schema import STANDARD_FINANCIAL_COLUMNS

SAMPLE = pd.DataFrame(
    {
        "symbol": ["000002", "000002"],
        "company_name": ["万科A", "万科A"],
        "year": [2022, 2023],
        "revenue": [100.0, 120.0],
        "net_profit": [10.0, 8.0],
        "total_assets": [500.0, 520.0],
        "total_liabilities": [300.0, 330.0],
    }
)


def test_read_seed_returns_none_when_missing(tmp_path, monkeypatch):
    monkeypatch.setattr(seed, "FINANCIALS_DIR", tmp_path)
    assert seed.read_seed_financials("000002") is None


def test_write_then_read_seed_roundtrip(tmp_path, monkeypatch):
    monkeypatch.setattr(seed, "FINANCIALS_DIR", tmp_path)
    path = seed.write_seed_financials("000002", SAMPLE)
    assert path.exists()

    loaded = seed.read_seed_financials("000002")
    assert loaded is not None and not loaded.empty
    assert set(STANDARD_FINANCIAL_COLUMNS) <= set(loaded.columns)
    assert sorted(loaded["year"].tolist()) == [2022, 2023]


def test_fetch_prefers_seed_over_cache_and_live(tmp_path, monkeypatch):
    monkeypatch.setattr(seed, "FINANCIALS_DIR", tmp_path)
    seed.write_seed_financials("000002", SAMPLE)

    result = fetch_company_financials("000002")
    assert result.source == "seed:normalized"
    assert not result.data.empty
    assert set(STANDARD_FINANCIAL_COLUMNS) <= set(result.data.columns)


def test_prefer_live_false_still_forces_sample_even_with_seed(tmp_path, monkeypatch):
    # prefer_live=False is the explicit "offline labeled sample" path; seed must not override it.
    monkeypatch.setattr(seed, "FINANCIALS_DIR", tmp_path)
    seed.write_seed_financials("600519", SAMPLE)

    result = fetch_company_financials("600519", prefer_live=False)
    assert result.source == "sample"


def test_seed_preserves_leading_zero_symbol(tmp_path, monkeypatch):
    # 000895 must not be coerced to 895 on CSV round-trip.
    monkeypatch.setattr(seed, "FINANCIALS_DIR", tmp_path)
    df = pd.DataFrame({"symbol": ["000895"], "company_name": ["双汇发展"], "year": [2023], "revenue": [5.0]})
    seed.write_seed_financials("000895", df)

    loaded = seed.read_seed_financials("000895")
    assert loaded["symbol"].iloc[0] == "000895"
    assert loaded["company_name"].iloc[0] == "双汇发展"


def test_has_seed(tmp_path, monkeypatch):
    monkeypatch.setattr(seed, "FINANCIALS_DIR", tmp_path)
    assert seed.has_seed("000002") is False
    seed.write_seed_financials("000002", SAMPLE)
    assert seed.has_seed("000002") is True
