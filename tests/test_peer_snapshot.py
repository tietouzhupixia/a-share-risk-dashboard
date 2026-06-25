"""Tests for real, seed-backed industry peer snapshots."""

import pandas as pd

from src.data import peers, seed
from src.data.akshare_client import fetch_peer_snapshot


def _financials(code: str, name: str, scale: float) -> pd.DataFrame:
    years = [2022, 2023]
    return pd.DataFrame(
        {
            "symbol": [code, code],
            "company_name": [name, name],
            "year": years,
            "revenue": [90 * scale, 100 * scale],
            "net_profit": [9 * scale, 10 * scale],
            "operating_cash_flow": [12 * scale, 15 * scale],
            "accounts_receivable": [20 * scale, 22 * scale],
            "inventory": [15 * scale, 17 * scale],
            "total_assets": [200 * scale, 220 * scale],
            "total_liabilities": [120 * scale, 130 * scale],
            "gross_profit": [30 * scale, 33 * scale],
            "short_term_borrowing": [10 * scale, 11 * scale],
        }
    )


def _seed_food_peers(tmp_path, monkeypatch):
    monkeypatch.setattr(seed, "FINANCIALS_DIR", tmp_path)
    # Two companies in 食品饮料 (universe): 贵州茅台 + 五粮液
    seed.write_seed_financials("600519", _financials("600519", "贵州茅台", 1.0))
    seed.write_seed_financials("000858", _financials("000858", "五粮液", 0.8))


def test_build_peer_snapshot_uses_industry_members(tmp_path, monkeypatch):
    _seed_food_peers(tmp_path, monkeypatch)

    snap = peers.build_peer_snapshot("600519")
    assert snap is not None
    assert set(snap["company_name"]) >= {"贵州茅台", "五粮液"}
    assert (snap["industry"] == "食品饮料").all()
    for col in ["revenue_growth", "roa", "asset_liability_ratio", "ocf_to_profit", "ar_to_revenue"]:
        assert col in snap.columns
    # roa = net_profit / total_assets for the latest year = 10/220
    row = snap.set_index("symbol").loc["600519"]
    assert abs(row["roa"] - (10 / 220)) < 1e-6


def test_build_peer_snapshot_returns_none_outside_universe(tmp_path, monkeypatch):
    monkeypatch.setattr(seed, "FINANCIALS_DIR", tmp_path)
    assert peers.build_peer_snapshot("999999") is None


def test_fetch_peer_snapshot_real_source(tmp_path, monkeypatch):
    _seed_food_peers(tmp_path, monkeypatch)

    result = fetch_peer_snapshot("600519")
    assert result.source == "seed:peers"
    assert result.warning is None
    assert len(result.data) >= 2


def test_fetch_peer_snapshot_falls_back_to_sample(tmp_path, monkeypatch):
    monkeypatch.setattr(seed, "FINANCIALS_DIR", tmp_path)
    result = fetch_peer_snapshot("999999")
    assert result.source == "sample"
    assert result.warning
