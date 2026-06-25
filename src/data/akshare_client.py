"""Public data access layer.

All AKShare integration lives here. Public fetchers return normalized annual
financial data so metrics, risk rules, pages, and exports never depend on raw
provider column names.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import reduce

import pandas as pd

from src.config import DEFAULT_COMPANIES
from src.data.cache import read_csv_cache, write_csv_cache
from src.data.sample_data import load_sample_financials, load_sample_peer_snapshot
from src.data.peers import build_peer_snapshot
from src.data.schema import FinancialDataResult, ensure_standard_columns
from src.data.seed import read_seed_financials


@dataclass(frozen=True)
class AShareSymbol:
    """Provider-specific formats for one A-share code."""

    code: str
    market: str
    eastmoney: str
    sina: str


def normalize_a_share_symbol(symbol: str) -> AShareSymbol:
    """Normalize common A-share inputs into provider-specific symbols."""

    text = symbol.strip().upper().replace(" ", "")
    market = ""
    code = text

    if "." in text:
        left, right = text.split(".", maxsplit=1)
        if left.isdigit():
            code = left
            market = right[:2]
    elif text[:2] in {"SH", "SZ", "BJ"}:
        market = text[:2]
        code = text[2:]

    if not code.isdigit() or len(code) != 6:
        raise ValueError(f"A-share symbol must be a six-digit code, got {symbol!r}")

    if not market:
        if code.startswith(("6", "9")):
            market = "SH"
        elif code.startswith(("0", "2", "3")):
            market = "SZ"
        elif code.startswith(("4", "8")):
            market = "BJ"
        else:
            raise ValueError(f"Cannot infer A-share market for {symbol!r}")

    return AShareSymbol(
        code=code,
        market=market,
        eastmoney=f"{market}{code}",
        sina=f"{market.lower()}{code}",
    )


def normalize_eastmoney_annual_financials(
    symbol: str,
    balance: pd.DataFrame,
    profit: pd.DataFrame,
    cash: pd.DataFrame,
) -> pd.DataFrame:
    """Normalize Eastmoney yearly statement frames into the project schema."""

    symbol_info = normalize_a_share_symbol(symbol)
    profit_frame = _prepare_provider_frame(
        profit,
        date_col="REPORT_DATE",
        report_type_col="REPORT_TYPE",
        mapping={
            "company_name": ["SECURITY_NAME_ABBR"],
            "revenue": ["OPERATE_INCOME", "TOTAL_OPERATE_INCOME"],
            "net_profit": ["PARENT_NETPROFIT", "NETPROFIT"],
            "_operating_cost": ["OPERATE_COST", "TOTAL_OPERATE_COST"],
        },
    )
    balance_frame = _prepare_provider_frame(
        balance,
        date_col="REPORT_DATE",
        report_type_col="REPORT_TYPE",
        mapping={
            "company_name": ["SECURITY_NAME_ABBR"],
            "accounts_receivable": [
                "ACCOUNTS_RECE",
                "ACCOUNTS_RECEIVABLE",
                "ACCOUNT_RECE",
                "NOTE_ACCOUNTS_RECE",
            ],
            "inventory": ["INVENTORY"],
            "total_assets": ["TOTAL_ASSETS"],
            "total_liabilities": ["TOTAL_LIABILITIES"],
            "short_term_borrowing": ["SHORT_LOAN", "SHORTTERM_LOAN", "SHORT_BORROW"],
        },
    )
    cash_frame = _prepare_provider_frame(
        cash,
        date_col="REPORT_DATE",
        report_type_col="REPORT_TYPE",
        mapping={
            "company_name": ["SECURITY_NAME_ABBR"],
            "operating_cash_flow": ["NETCASH_OPERATE", "NETCASH_OPERATENOTE"],
        },
    )

    return _merge_statement_frames(symbol_info, [profit_frame, balance_frame, cash_frame])


def normalize_sina_annual_financials(
    symbol: str,
    balance: pd.DataFrame,
    profit: pd.DataFrame,
    cash: pd.DataFrame,
) -> pd.DataFrame:
    """Normalize Sina three-statement frames into the project schema."""

    symbol_info = normalize_a_share_symbol(symbol)
    profit_frame = _prepare_provider_frame(
        profit,
        date_col="报告日",
        report_type_col=None,
        mapping={
            "revenue": ["营业收入", "营业总收入"],
            "net_profit": ["归属于母公司所有者的净利润", "净利润"],
            "_operating_cost": ["营业成本", "营业总成本"],
        },
    )
    balance_frame = _prepare_provider_frame(
        balance,
        date_col="报告日",
        report_type_col=None,
        mapping={
            "accounts_receivable": ["应收账款", "应收票据及应收账款"],
            "inventory": ["存货"],
            "total_assets": ["资产总计"],
            "total_liabilities": ["负债合计"],
            "short_term_borrowing": ["短期借款"],
        },
    )
    cash_frame = _prepare_provider_frame(
        cash,
        date_col="报告日",
        report_type_col=None,
        mapping={
            "operating_cash_flow": [
                "经营活动产生的现金流量净额",
                "经营活动现金流量净额",
            ],
        },
    )

    return _merge_statement_frames(symbol_info, [profit_frame, balance_frame, cash_frame])


def fetch_company_financials(symbol: str, prefer_live: bool = True) -> FinancialDataResult:
    """Fetch annual financial data for one A-share company.

    The fallback order is committed seed snapshot, normalized cache, Eastmoney
    live, Sina live, then explicitly labeled sample data. `prefer_live=False`
    forces the offline labeled sample path (used for tests and demos).
    """

    symbol_info = normalize_a_share_symbol(symbol)
    cache_name = f"normalized_financials_{symbol_info.code}.csv"

    if prefer_live:
        seeded = read_seed_financials(symbol_info.code)
        if seeded is not None and not seeded.empty:
            return FinancialDataResult(data=seeded, source="seed:normalized")

        cached = read_csv_cache(cache_name)
        if cached is not None and not cached.empty:
            return FinancialDataResult(data=ensure_standard_columns(cached), source="cache:normalized")

    failures: list[str] = []
    if prefer_live:
        for source_name, fetcher in (
            ("akshare:eastmoney:yearly", _fetch_eastmoney_financials),
            ("akshare:sina", _fetch_sina_financials),
        ):
            try:
                live_data = fetcher(symbol_info)
                if not live_data.empty:
                    live_data = ensure_standard_columns(live_data)
                    write_csv_cache(cache_name, live_data)
                    return FinancialDataResult(data=live_data, source=source_name)
            except Exception as exc:  # pragma: no cover - exercised by live upstream failures
                failures.append(f"{source_name}: {type(exc).__name__}: {exc}")

    data = load_sample_financials(symbol_info.code)
    failure_note = "；".join(failures[:2])
    if failure_note:
        failure_note = f" live source failures: {failure_note}"
    return FinancialDataResult(
        data=data,
        source="sample",
        warning=f"当前使用本地演示数据，并非实时公开财报数据。{failure_note}",
    )


def fetch_live_financials(symbol: str) -> pd.DataFrame:
    """Live-only normalized fetch (Eastmoney then Sina), bypassing seed/cache/sample.

    Used by the seed-build script to refresh the committed snapshot. Raises
    RuntimeError if both live providers fail or return empty.
    """

    symbol_info = normalize_a_share_symbol(symbol)
    errors: list[str] = []
    for name, fetcher in (
        ("eastmoney", _fetch_eastmoney_financials),
        ("sina", _fetch_sina_financials),
    ):
        try:
            data = fetcher(symbol_info)
            if not data.empty:
                return ensure_standard_columns(data)
            errors.append(f"{name}: empty")
        except Exception as exc:
            errors.append(f"{name}: {type(exc).__name__}: {exc}")
    raise RuntimeError(f"live fetch failed for {symbol}: {'; '.join(errors)}")


def fetch_peer_snapshot(symbol: str):
    """Fetch a peer-comparison snapshot.

    Prefers real same-industry peers built from the committed seed dataset; falls
    back to the labeled sample peers when the symbol is outside the universe.
    """

    try:
        code = normalize_a_share_symbol(symbol).code
    except ValueError:
        code = symbol.strip()

    snapshot = build_peer_snapshot(code)
    if snapshot is not None and not snapshot.empty:
        return FinancialDataResult(data=snapshot, source="seed:peers")

    return FinancialDataResult(
        data=load_sample_peer_snapshot(symbol.strip()),
        source="sample",
        warning="当前使用本地演示同业数据。真实同业口径将在数据层统一接入。",
    )


def _fetch_eastmoney_financials(symbol_info: AShareSymbol) -> pd.DataFrame:
    import akshare as ak

    balance = ak.stock_balance_sheet_by_yearly_em(symbol=symbol_info.eastmoney)
    profit = ak.stock_profit_sheet_by_yearly_em(symbol=symbol_info.eastmoney)
    cash = ak.stock_cash_flow_sheet_by_yearly_em(symbol=symbol_info.eastmoney)
    return normalize_eastmoney_annual_financials(symbol_info.code, balance, profit, cash)


def _fetch_sina_financials(symbol_info: AShareSymbol) -> pd.DataFrame:
    import akshare as ak

    balance = ak.stock_financial_report_sina(stock=symbol_info.sina, symbol="资产负债表")
    profit = ak.stock_financial_report_sina(stock=symbol_info.sina, symbol="利润表")
    cash = ak.stock_financial_report_sina(stock=symbol_info.sina, symbol="现金流量表")
    return normalize_sina_annual_financials(symbol_info.code, balance, profit, cash)


def _prepare_provider_frame(
    df: pd.DataFrame,
    *,
    date_col: str,
    report_type_col: str | None,
    mapping: dict[str, list[str]],
) -> pd.DataFrame:
    if df is None or df.empty or date_col not in df.columns:
        return pd.DataFrame({"year": pd.Series(dtype="int64")})

    frame = df.copy()
    frame["_report_text"] = frame[date_col].astype(str)
    frame["year"] = frame["_report_text"].str.extract(r"(\d{4})")[0]
    frame = frame.dropna(subset=["year"])
    frame["year"] = frame["year"].astype(int)

    annual_mask = frame["_report_text"].str.contains(r"12-31|1231", regex=True, na=False)
    if report_type_col and report_type_col in frame.columns:
        annual_mask = annual_mask | frame[report_type_col].astype(str).str.contains("年报", na=False)
    frame = frame[annual_mask].copy()

    result = pd.DataFrame({"year": frame["year"]})
    for target, candidates in mapping.items():
        source_col = _first_existing_column(frame, candidates)
        if source_col is None:
            result[target] = pd.NA
        elif target == "company_name":
            result[target] = frame[source_col]
        else:
            result[target] = pd.to_numeric(frame[source_col], errors="coerce")

    return result.drop_duplicates(subset=["year"], keep="first")


def _merge_statement_frames(symbol_info: AShareSymbol, frames: list[pd.DataFrame]) -> pd.DataFrame:
    non_empty_frames = [frame for frame in frames if not frame.empty]
    if not non_empty_frames:
        return ensure_standard_columns(pd.DataFrame())

    merged = reduce(lambda left, right: pd.merge(left, right, on="year", how="outer"), non_empty_frames)
    merged = _coalesce_duplicate_columns(merged)

    if "_operating_cost" in merged.columns:
        merged["gross_profit"] = merged["revenue"] - merged["_operating_cost"]

    merged["symbol"] = symbol_info.code
    if "company_name" not in merged.columns or merged["company_name"].isna().all():
        merged["company_name"] = DEFAULT_COMPANIES.get(symbol_info.code, symbol_info.code)
    else:
        merged["company_name"] = merged["company_name"].ffill().bfill()

    merged = merged.dropna(subset=["year"]).copy()
    merged["year"] = merged["year"].astype(int)

    standard = ensure_standard_columns(merged)
    numeric_columns = [col for col in standard.columns if col not in {"symbol", "company_name"}]
    for column in numeric_columns:
        standard[column] = pd.to_numeric(standard[column], errors="coerce")

    return standard.sort_values("year").reset_index(drop=True)


def _coalesce_duplicate_columns(df: pd.DataFrame) -> pd.DataFrame:
    result = df.copy()
    duplicate_bases = {
        column.rsplit("_", maxsplit=1)[0]
        for column in result.columns
        if column.endswith(("_x", "_y"))
    }
    for base in duplicate_bases:
        candidates = [column for column in result.columns if column == base or column.startswith(f"{base}_")]
        result[base] = result[candidates].bfill(axis=1).iloc[:, 0]
        drop_candidates = [column for column in candidates if column != base]
        result = result.drop(columns=drop_candidates)
    return result


def _first_existing_column(df: pd.DataFrame, candidates: list[str]) -> str | None:
    for candidate in candidates:
        if candidate in df.columns:
            return candidate
    return None
