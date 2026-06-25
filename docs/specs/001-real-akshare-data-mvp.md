# Spec: Real AKShare Data MVP

## Objective

Build the first reliable real-data path for the A-share financial risk dashboard.

The target user can enter a six-digit A-share code, such as `600519` or `002594`, and the app will attempt to fetch annual public financial-statement data through AKShare, normalize it into the existing standard schema, and keep the existing metrics, risk rules, charts, summary, and Excel export working.

This feature is specifically a data-layer MVP. It does not redesign pages, add PDF export, add LLM output, or build full industry peer matching.

## Assumptions

1. The first supported scope is non-financial A-share annual statements.
2. Annual reports are preferred over quarterly reports.
3. Eastmoney yearly statement APIs are the primary source when available.
4. Sina financial reports are an allowed fallback because AKShare documents them as a three-statement source.
5. If all public live sources fail, the app must fall back to explicitly labeled sample data and not crash.
6. Local CSV cache is acceptable for raw public data and normalized annual data.

## Tech Stack

- Python 3.12 in local `.venv`
- Streamlit 1.58.0
- AKShare 1.18.64
- pandas 3.0.3
- pytest 9.1.1

## Source References

- AKShare stock documentation documents annual Eastmoney statement functions:
  - `stock_balance_sheet_by_yearly_em`
  - `stock_profit_sheet_by_yearly_em`
  - `stock_cash_flow_sheet_by_yearly_em`
- AKShare stock documentation also documents Sina three-statement fallback:
  - `stock_financial_report_sina(stock="sh600600", symbol="资产负债表")`
- Streamlit official documentation states `st.cache_data` is for functions that return data such as DataFrame transforms and database/API queries.
- Streamlit official documentation supports the current `pages/` directory multipage structure.

## Commands

```bash
.venv\Scripts\python.exe -m pytest -q
.venv\Scripts\python.exe -m compileall app.py pages src tests
.venv\Scripts\streamlit.exe run app.py --server.port 8501 --server.headless true
```

## Project Structure

```text
src/data/akshare_client.py     # Public data source orchestration
src/data/schema.py             # Standard schema and normalization helpers
src/data/cache.py              # Local CSV cache helpers
src/data/sample_data.py        # Explicit fallback/demo data
tests/                         # Unit and smoke tests for mappings/fallbacks
docs/DATA_DICTIONARY.md        # Field mapping and source policy
docs/plans/                    # Ordered implementation tasks
docs/specs/                    # Feature specifications
```

## Code Style

Keep external source handling inside `src/data/`.

```python
def fetch_company_financials(symbol: str, prefer_live: bool = True) -> FinancialDataResult:
    """Return standard annual financial data with source and warning metadata."""
    clean_symbol = normalize_a_share_symbol(symbol)
    ...
```

Guidelines:

- Use typed function signatures for data-layer helpers.
- Return `FinancialDataResult` from public fetchers.
- Keep raw AKShare DataFrame column names out of metrics/risk/UI modules.
- Use explicit fallback paths and user-readable warnings.

## Testing Strategy

Use pytest.

Small tests:

- Symbol normalization: `600519 -> SH600519`, `002594 -> SZ002594`, `sh600519 -> SH600519`.
- Eastmoney raw frames normalize into all `STANDARD_FINANCIAL_COLUMNS`.
- Sina raw frames normalize into all `STANDARD_FINANCIAL_COLUMNS`.
- Fallback returns labeled sample data when live fetchers fail.

Medium tests:

- Normalized output can pass through `add_financial_metrics()` and `evaluate_risks()`.

Live network tests are optional and must be marked or skipped by default because upstream finance sources can fail.

## Boundaries

Always:

- Keep AKShare calls in `src/data/akshare_client.py`.
- Keep standard field names defined by `src/data/schema.py`.
- Cache public raw/normalized data only under `data/cache/`.
- Update `docs/DATA_DICTIONARY.md` when mappings change.
- Update `docs/TASK_LOG.md` after each AI session.

Ask first:

- Adding a paid/private data source.
- Changing metric formulas.
- Replacing the Streamlit multipage structure.
- Adding a new dependency.

Never:

- Commit Wind, CSMAR, Choice, or private raw data.
- Put AKShare calls directly in page files.
- Present sample fallback data as real public data.
- Let a network/source failure crash the app.

## Success Criteria

- `fetch_company_financials("600519", prefer_live=True)` returns standard annual rows from AKShare when a live source succeeds.
- The returned DataFrame includes every field in `STANDARD_FINANCIAL_COLUMNS`.
- The returned source label distinguishes live Eastmoney, live Sina, cache, and sample fallback.
- If live fetchers fail, sample fallback returns with a warning.
- Existing pages continue to work without major UI changes.
- `pytest -q` passes.
- `compileall` passes.

## Current Slice

Slice 1 implements:

- Symbol normalization.
- Eastmoney yearly-statement normalization.
- Sina statement normalization.
- Cache helper support for normalized data.
- Public `fetch_company_financials(..., prefer_live=True)` fallback chain.
- Unit tests for mapping and fallback behavior.

## Open Questions

- Whether to use parent net profit or total net profit as the default project-wide `net_profit`. Current choice: parent net profit when available, otherwise net profit.
- Whether financial firms need a separate schema. Current choice: mark them as future scope.
- Whether to persist raw statement tables separately from normalized tables. Current choice: normalized CSV cache first; raw cache can be added if debugging requires it.

