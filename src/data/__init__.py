"""Data access and normalization layer."""

from src.data.akshare_client import fetch_company_financials, fetch_peer_snapshot

__all__ = ["fetch_company_financials", "fetch_peer_snapshot"]

