import pandas as pd

from scripts.verify_company_coverage import summarize_financial_result
from src.data.schema import FinancialDataResult


def test_summarize_financial_result_reports_source_years_and_missing_fields():
    result = FinancialDataResult(
        data=pd.DataFrame(
            [
                {
                    "symbol": "002594",
                    "company_name": "比亚迪",
                    "year": 2022,
                    "revenue": 100.0,
                    "net_profit": 10.0,
                    "operating_cash_flow": 12.0,
                    "accounts_receivable": 8.0,
                    "inventory": 15.0,
                    "total_assets": 300.0,
                    "total_liabilities": 120.0,
                    "gross_profit": 20.0,
                    "short_term_borrowing": pd.NA,
                }
            ]
        ),
        source="akshare:sina",
    )

    summary = summarize_financial_result("002594", result)

    assert summary["symbol"] == "002594"
    assert summary["company_name"] == "比亚迪"
    assert summary["source"] == "akshare:sina"
    assert summary["rows"] == 1
    assert summary["year_start"] == 2022
    assert summary["year_end"] == 2022
    assert summary["missing_core_fields"] == "short_term_borrowing"
