import pandas as pd

from src.data.akshare_client import (
    fetch_company_financials,
    is_valid_a_share_symbol,
    normalize_a_share_symbol,
    normalize_eastmoney_annual_financials,
    normalize_sina_annual_financials,
)


def test_is_valid_a_share_symbol():
    assert is_valid_a_share_symbol("600519")
    assert is_valid_a_share_symbol("sz002594")
    assert is_valid_a_share_symbol("SH600519")
    assert not is_valid_a_share_symbol("")
    assert not is_valid_a_share_symbol("   ")
    assert not is_valid_a_share_symbol("ABC")
    assert not is_valid_a_share_symbol("12345")
from src.data.schema import STANDARD_FINANCIAL_COLUMNS


def test_normalize_a_share_symbol_builds_provider_formats():
    sh_symbol = normalize_a_share_symbol("600519")
    sz_symbol = normalize_a_share_symbol("sz002594")

    assert sh_symbol.code == "600519"
    assert sh_symbol.eastmoney == "SH600519"
    assert sh_symbol.sina == "sh600519"
    assert sz_symbol.code == "002594"
    assert sz_symbol.eastmoney == "SZ002594"
    assert sz_symbol.sina == "sz002594"


def test_normalize_a_share_symbol_rejects_invalid_codes():
    try:
        normalize_a_share_symbol("ABC")
    except ValueError as exc:
        assert "six-digit" in str(exc)
    else:
        raise AssertionError("invalid symbol should raise ValueError")


def test_normalize_eastmoney_annual_financials_maps_standard_columns():
    profit = pd.DataFrame(
        [
            {
                "SECURITY_CODE": "600519",
                "SECURITY_NAME_ABBR": "贵州茅台",
                "REPORT_DATE": "2023-12-31 00:00:00",
                "REPORT_TYPE": "年报",
                "OPERATE_INCOME": 100.0,
                "OPERATE_COST": 35.0,
                "PARENT_NETPROFIT": 20.0,
            }
        ]
    )
    balance = pd.DataFrame(
        [
            {
                "SECURITY_CODE": "600519",
                "SECURITY_NAME_ABBR": "贵州茅台",
                "REPORT_DATE": "2023-12-31 00:00:00",
                "REPORT_TYPE": "年报",
                "ACCOUNTS_RECE": 10.0,
                "INVENTORY": 12.0,
                "TOTAL_ASSETS": 200.0,
                "TOTAL_LIABILITIES": 80.0,
                "SHORT_LOAN": 5.0,
            }
        ]
    )
    cash = pd.DataFrame(
        [
            {
                "SECURITY_CODE": "600519",
                "SECURITY_NAME_ABBR": "贵州茅台",
                "REPORT_DATE": "2023-12-31 00:00:00",
                "REPORT_TYPE": "年报",
                "NETCASH_OPERATE": 25.0,
            }
        ]
    )

    normalized = normalize_eastmoney_annual_financials("600519", balance, profit, cash)

    assert set(STANDARD_FINANCIAL_COLUMNS) <= set(normalized.columns)
    row = normalized.iloc[0]
    assert row["symbol"] == "600519"
    assert row["company_name"] == "贵州茅台"
    assert row["year"] == 2023
    assert row["revenue"] == 100.0
    assert row["gross_profit"] == 65.0
    assert row["net_profit"] == 20.0
    assert row["operating_cash_flow"] == 25.0
    assert row["accounts_receivable"] == 10.0


def test_normalize_sina_annual_financials_maps_standard_columns():
    balance = pd.DataFrame(
        [
            {
                "报告日": "20231231",
                "应收账款": 10.0,
                "存货": 12.0,
                "资产总计": 200.0,
                "负债合计": 80.0,
                "短期借款": 5.0,
            }
        ]
    )
    profit = pd.DataFrame(
        [
            {
                "报告日": "20231231",
                "营业收入": 100.0,
                "营业成本": 35.0,
                "归属于母公司所有者的净利润": 20.0,
            }
        ]
    )
    cash = pd.DataFrame(
        [
            {
                "报告日": "20231231",
                "经营活动产生的现金流量净额": 25.0,
            }
        ]
    )

    normalized = normalize_sina_annual_financials("600519", balance, profit, cash)

    assert set(STANDARD_FINANCIAL_COLUMNS) <= set(normalized.columns)
    row = normalized.iloc[0]
    assert row["year"] == 2023
    assert row["revenue"] == 100.0
    assert row["gross_profit"] == 65.0
    assert row["net_profit"] == 20.0
    assert row["operating_cash_flow"] == 25.0
    assert row["total_assets"] == 200.0


def test_fetch_company_financials_falls_back_to_sample_when_live_disabled():
    result = fetch_company_financials("600519", prefer_live=False)

    assert result.source == "sample"
    assert result.warning
    assert set(STANDARD_FINANCIAL_COLUMNS) <= set(result.data.columns)
    assert not result.data.empty

