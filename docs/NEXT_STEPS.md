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

## Immediate Next Task

Screenshots and the deployment checklist are both done. The remaining portfolio step is to
actually go live:

> Perform the Streamlit Community Cloud deployment by following `docs/DEPLOYMENT.md`
> (push repo to GitHub → create app on share.streamlit.io → Python 3.10/3.11 → smoke check),
> then record the resulting public URL in the README and `docs/DEPLOYMENT.md`.

Acceptance:

- A public Streamlit Cloud URL exists and opens all four pages.
- README links the live URL near the top (next to the screenshots).
- Deployment follows `docs/DEPLOYMENT.md` without changing metric formulas or risk thresholds.
- `docs/TASK_LOG.md` is updated.

Optional polish (not required): replace the static company-analysis screenshot with a short GIF
of switching pages, if a recorder is available.

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
