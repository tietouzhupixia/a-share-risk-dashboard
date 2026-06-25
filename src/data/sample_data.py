"""Labeled demo data used when live public data is unavailable."""

import pandas as pd

from src.config import DEFAULT_COMPANIES, DEFAULT_SYMBOL
from src.data.schema import ensure_standard_columns


def load_sample_financials(symbol: str = DEFAULT_SYMBOL) -> pd.DataFrame:
    """Return a compact annual financial panel for local UI and test runs."""

    company_name = DEFAULT_COMPANIES.get(symbol, "样例公司")
    rows = [
        {
            "symbol": symbol,
            "company_name": company_name,
            "year": 2018,
            "revenue": 130_055_000_000,
            "net_profit": 2_780_000_000,
            "operating_cash_flow": 12_520_000_000,
            "accounts_receivable": 49_210_000_000,
            "inventory": 26_330_000_000,
            "total_assets": 194_570_000_000,
            "total_liabilities": 133_880_000_000,
            "gross_profit": 21_650_000_000,
            "short_term_borrowing": 35_210_000_000,
        },
        {
            "symbol": symbol,
            "company_name": company_name,
            "year": 2019,
            "revenue": 127_739_000_000,
            "net_profit": 1_614_000_000,
            "operating_cash_flow": 14_740_000_000,
            "accounts_receivable": 43_920_000_000,
            "inventory": 25_580_000_000,
            "total_assets": 195_640_000_000,
            "total_liabilities": 132_900_000_000,
            "gross_profit": 18_580_000_000,
            "short_term_borrowing": 31_500_000_000,
        },
        {
            "symbol": symbol,
            "company_name": company_name,
            "year": 2020,
            "revenue": 156_598_000_000,
            "net_profit": 4_234_000_000,
            "operating_cash_flow": 45_390_000_000,
            "accounts_receivable": 41_210_000_000,
            "inventory": 31_390_000_000,
            "total_assets": 201_017_000_000,
            "total_liabilities": 136_500_000_000,
            "gross_profit": 30_220_000_000,
            "short_term_borrowing": 28_300_000_000,
        },
        {
            "symbol": symbol,
            "company_name": company_name,
            "year": 2021,
            "revenue": 216_142_000_000,
            "net_profit": 3_045_000_000,
            "operating_cash_flow": 65_480_000_000,
            "accounts_receivable": 58_440_000_000,
            "inventory": 43_360_000_000,
            "total_assets": 295_780_000_000,
            "total_liabilities": 191_540_000_000,
            "gross_profit": 28_360_000_000,
            "short_term_borrowing": 40_100_000_000,
        },
        {
            "symbol": symbol,
            "company_name": company_name,
            "year": 2022,
            "revenue": 424_061_000_000,
            "net_profit": 16_622_000_000,
            "operating_cash_flow": 140_838_000_000,
            "accounts_receivable": 71_980_000_000,
            "inventory": 79_100_000_000,
            "total_assets": 493_861_000_000,
            "total_liabilities": 372_470_000_000,
            "gross_profit": 72_460_000_000,
            "short_term_borrowing": 49_500_000_000,
        },
        {
            "symbol": symbol,
            "company_name": company_name,
            "year": 2023,
            "revenue": 602_315_000_000,
            "net_profit": 30_041_000_000,
            "operating_cash_flow": 169_725_000_000,
            "accounts_receivable": 109_820_000_000,
            "inventory": 87_690_000_000,
            "total_assets": 679_548_000_000,
            "total_liabilities": 529_370_000_000,
            "gross_profit": 121_540_000_000,
            "short_term_borrowing": 61_900_000_000,
        },
        {
            "symbol": symbol,
            "company_name": company_name,
            "year": 2024,
            "revenue": 731_200_000_000,
            "net_profit": 40_250_000_000,
            "operating_cash_flow": 182_300_000_000,
            "accounts_receivable": 152_900_000_000,
            "inventory": 118_700_000_000,
            "total_assets": 818_900_000_000,
            "total_liabilities": 646_800_000_000,
            "gross_profit": 145_500_000_000,
            "short_term_borrowing": 86_200_000_000,
        },
    ]
    return ensure_standard_columns(pd.DataFrame(rows))


def load_sample_peer_snapshot(symbol: str = DEFAULT_SYMBOL) -> pd.DataFrame:
    """Return a small peer-comparison table for UI scaffolding."""

    rows = [
        {
            "symbol": symbol,
            "company_name": DEFAULT_COMPANIES.get(symbol, "样例公司"),
            "industry": "新能源制造",
            "revenue_growth": 0.214,
            "roa": 0.049,
            "asset_liability_ratio": 0.790,
            "ocf_to_profit": 4.529,
            "ar_to_revenue": 0.209,
        },
        {
            "symbol": "300750",
            "company_name": "宁德时代",
            "industry": "新能源制造",
            "revenue_growth": 0.221,
            "roa": 0.091,
            "asset_liability_ratio": 0.682,
            "ocf_to_profit": 1.861,
            "ar_to_revenue": 0.143,
        },
        {
            "symbol": "601012",
            "company_name": "隆基绿能",
            "industry": "新能源制造",
            "revenue_growth": -0.078,
            "roa": 0.011,
            "asset_liability_ratio": 0.604,
            "ocf_to_profit": 0.734,
            "ar_to_revenue": 0.118,
        },
        {
            "symbol": "002460",
            "company_name": "赣锋锂业",
            "industry": "新能源制造",
            "revenue_growth": -0.196,
            "roa": -0.018,
            "asset_liability_ratio": 0.536,
            "ocf_to_profit": -0.420,
            "ar_to_revenue": 0.067,
        },
        {
            "symbol": "002812",
            "company_name": "恩捷股份",
            "industry": "新能源制造",
            "revenue_growth": -0.054,
            "roa": 0.034,
            "asset_liability_ratio": 0.572,
            "ocf_to_profit": 1.210,
            "ar_to_revenue": 0.172,
        },
    ]
    return pd.DataFrame(rows)

