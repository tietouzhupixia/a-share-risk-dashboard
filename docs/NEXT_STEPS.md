# Next Steps

This file is the quick handoff for the next AI entering the project.

## Current Status

- Project skeleton is runnable.
- Real AKShare data MVP Slice 1 is implemented in `src/data/akshare_client.py`.
- Company analysis, risk rules, and export pages now show a compact data-source status through `src/ui/source_status.py`.
- Three-symbol coverage has been verified for `600519`, `002594`, and `300750`.
- `600519`, `002594`, and `300750` now have local normalized cache files in this workspace after successful verification runs.
- If live sources fail, the app falls back to labeled sample data instead of crashing.
- Unit tests cover symbol normalization, Eastmoney fixture mapping, Sina fixture mapping, fallback, and page-facing source-status text.
- README now has a `界面预览 (Screenshots)` section with real local screenshots of all four pages under `docs/assets/`, plus a `Deployment` section and `docs/DEPLOYMENT.md` checklist.
- **The app is live on Streamlit Community Cloud: https://a-share-risk-dashboard-hmft7s3jyqsew6doqizjpp.streamlit.app/** (repo: https://github.com/tietouzhupixia/a-share-risk-dashboard).

## Completed Slices

- [x] Project skeleton and AI collaboration contract.
- [x] Specs and task plan for real AKShare data MVP.
- [x] Data-layer tests for provider mapping and fallback.
- [x] Data-layer implementation for:
  - symbol normalization
  - Eastmoney annual-statement normalization
  - Sina annual-statement normalization
  - normalized CSV cache under `data/cache/`
  - public `fetch_company_financials()` fallback chain
- [x] Reader-facing source-status helper and page integration for company/risk/export pages.
- [x] Three-symbol public-data coverage verification and README caveats.
- [x] Streamlit Cloud deployment checklist (`docs/DEPLOYMENT.md`) and README `Deployment` section.
- [x] Real local screenshots of all four pages embedded in README (`docs/assets/`).
- [x] **Deployed to Streamlit Community Cloud and live URL recorded in README + `docs/DEPLOYMENT.md`.**
- [x] **Data Depth & Robustness: committed 28-company seed snapshot (`data/seed/`) at top of the
  fallback chain; reproducible `scripts/build_seed_dataset.py`; data-quality fixes (string codes,
  universe names); real seed-backed industry peers on the peer page.** (local; pending commit/push)

## Immediate Next Task

Data Depth & Robustness main line (see `docs/plans/002-data-depth-robustness-plan.md`) is largely
done locally: a committed 28-company seed snapshot (`data/seed/`) now sits at the top of the
fallback chain, and the peer-comparison page uses real same-industry peers built from it.

The next step is to ship it and verify on Cloud:

> 1. Commit and push — **must include the new real data and modules**:
>    `git add data/seed src tests scripts docs README.md && git commit && git push`.
>    Streamlit Cloud auto-rebuilds.
> 2. Cloud smoke pass: open the live URL, try several universe symbols
>    (e.g. `600519` 茅台, `000895` 双汇, `600276` 恒瑞), confirm each shows
>    `数据来源：已提交的标准化快照` and the peer page shows real industry peers (no demo warning).
> 3. Note the observed Cloud sources in `docs/TASK_LOG.md`.

Acceptance:

- Pushed repo contains `data/seed/financials/*.csv` (28 files) and the new `src/data/{seed,universe,peers}.py`.
- Cloud serves `seed:normalized` for universe companies and `seed:peers` on the peer page.
- No metric formulas or risk thresholds changed.

## After That (optional, within the same main line or beyond)

- Add a reusable `src/data/quality.py` data-quality module (currently coverage is validated via
  `scripts/verify_company_coverage.py`; the universe is at 0 missing core fields).
- Expand the universe further, or refresh the seed snapshot periodically.
- Then consider the other main lines: evidence-linked AI summary, PDF/one-page report.

### How the screenshots were produced (reproducible)

- The app was run locally (`streamlit run app.py`, port 8501).
- Screenshots were captured with headless Chrome via Playwright using the installed Chrome
  channel (no chromium download). Playwright was installed only into the local `.venv` and is
  intentionally NOT added to `requirements.txt`, so deployment is unaffected.
- Naive `chrome --headless --screenshot` captured only Streamlit's loading skeleton; waiting for
  the rendered page (Playwright `wait_for_selector`) was required to get real content.

## After That

- Then consider PDF export or evidence-linked AI summary polish.

## Commands

```bash
.venv\Scripts\python.exe -m pytest -q
.venv\Scripts\python.exe -m compileall app.py pages src tests
.venv\Scripts\python.exe -m scripts.verify_company_coverage 600519 002594 300750
.venv\Scripts\streamlit.exe run app.py --server.port 8501 --server.headless true
```

## Do Not Do Yet

- Do not add PDF export before real data and page status are stable.
- Do not add LLM API calls before summaries are evidence-linked.
- Do not redesign the UI while data-source reliability is still being verified.
- Do not change risk-rule formulas without updating `docs/RISK_RULES_SPEC.md`.
