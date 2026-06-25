"""Data access and normalization layer."""

from src.data.akshare_client import (
    fetch_company_financials,
    fetch_peer_snapshot,
    is_valid_a_share_symbol,
)

__all__ = ["fetch_company_financials", "fetch_peer_snapshot", "is_valid_a_share_symbol"]

