"""Tests for the seed-dataset build script (network-free via injected fetcher)."""

import pandas as pd

from scripts import build_seed_dataset as bsd

DF = pd.DataFrame(
    {
        "symbol": ["600519", "600519"],
        "company_name": ["贵州茅台", "贵州茅台"],
        "year": [2022, 2023],
        "revenue": [90.0, 100.0],
    }
)


def test_build_seed_for_symbol_success():
    written = {}

    def fake_writer(code, df):
        written[code] = df
        return f"data/seed/financials/{code}.csv"

    row = bsd.build_seed_for_symbol("600519", fetcher=lambda code: DF, writer=fake_writer)

    assert row["status"] == "ok"
    assert row["rows"] == 2
    assert row["year_start"] == 2022 and row["year_end"] == 2023
    assert "600519" in written


def test_build_seed_for_symbol_retries_then_fails():
    calls = {"n": 0}

    def flaky(code):
        calls["n"] += 1
        raise RuntimeError("boom")

    row = bsd.build_seed_for_symbol(
        "600519", fetcher=flaky, writer=lambda code, df: None, retries=3
    )

    assert row["status"] == "failed"
    assert calls["n"] == 3
    assert "boom" in row["error"]


def test_build_seed_dataset_aggregates_rows():
    rows = bsd.build_seed_dataset(
        ["600519", "000333"], fetcher=lambda code: DF, writer=lambda code, df: None, retries=1
    )

    assert [r["symbol"] for r in rows] == ["600519", "000333"]
    assert all(r["status"] == "ok" for r in rows)
