# Next Steps

This file is the quick handoff for the next AI/developer entering the project.
**Read order (per `AGENTS.md`): this file → `AGENTS.md` → `docs/PROJECT_STRUCTURE.md` →
`docs/PAGE_REGISTRY.md` → `docs/TASK_LOG.md`.** The newest TASK_LOG entry is the most
detailed record of where things stand.

Last updated: 2026-06-25.

## Current Status (as of 2026-06-25)

The project is a runnable, **deployed, and Cloud-verified** Streamlit app. Repo and live URL:

- Repo: https://github.com/tietouzhupixia/a-share-risk-dashboard (branch `main`)
- Live: https://a-share-risk-dashboard-hmft7s3jyqsew6doqizjpp.streamlit.app/
- Everything is committed and pushed; `git status` is clean. No work is stranded locally.

What works today:

- **Four pages**: 公司分析 (company), 同业比较 (peer), 风险预警 (risk), 导出中心 (export Excel).
  All show a data-source status caption.
- **Real data with a robust fallback chain**: `seed → cache → Eastmoney live → Sina live → sample`.
- **Committed seed dataset** `data/seed/financials/<code>.csv` — **28 non-financial large caps,
  13 industries, 1990–2025, 717 company-year rows, 0 missing core fields**. Because it is in Git,
  the Cloud app serves real data with no live call. Verified live: company page shows
  `seed:normalized`, peer page shows `seed:peers` (real same-industry peers).
- **Reproducible data build**: `python -m scripts.build_seed_dataset` refreshes the whole snapshot.
- **Input validation**: empty/invalid A-share codes show a friendly message instead of crashing.
- **Tests**: 34 passing across 9 test files (TDD). `compileall` clean.

## Completed (high level)

- [x] Project skeleton + AI collaboration contract (`AGENTS.md`).
- [x] Real AKShare data layer: symbol normalization, Eastmoney/Sina mapping, normalized cache, fallback.
- [x] Source-status captions on all data pages.
- [x] Screenshots in README (`docs/assets/`), Deployment section + `docs/DEPLOYMENT.md`.
- [x] **Deployed to Streamlit Community Cloud; live URL recorded.**
- [x] **Data Depth & Robustness main line (DONE & Cloud-verified)** — see
  `docs/plans/002-data-depth-robustness-plan.md`: committed 28-company seed snapshot at the top of
  the fallback chain, reproducible build script, real seed-backed industry peers, data-quality fixes
  (string codes keep leading zeros, names backfilled from the universe), input guards.

## Immediate Next Task (pick one — the project is at a clean checkpoint)

No work is half-finished. The next owner chooses a main line. Recommended first, then alternatives:

1. **(Recommended) Functional depth — evidence-linked AI summary and/or one-page PDF report.**
   The rule-based summary already exists in `src/ai/`; add an optional LLM polish that stays bound
   to the same evidence, and/or a PDF/one-page export in `src/export/`. Highest recruiter value
   ("金融分析 + AI 产品化"). Respect the "Do Not Do Yet" gates below (LLM only after summaries are
   evidence-linked; keep a non-LLM fallback).
2. **More data depth.** Add `src/data/quality.py` (reusable data-quality checks; today coverage is
   validated only via `scripts/verify_company_coverage.py`), expand the universe beyond 28, or add a
   periodic seed refresh. Keep banks/insurers out until a financial-sector schema is built.
3. **Front-end / robustness polish.** Migrate `use_container_width=True` → `width="stretch"` to clear
   the Streamlit 1.58 deprecation warnings seen in Cloud logs (harmless today, slated for removal).

For any choice: stay inside module boundaries (`AGENTS.md`), do not change metric formulas or risk
thresholds without updating `docs/RISK_RULES_SPEC.md`, add focused tests, and update `docs/TASK_LOG.md`.

## Operational notes (learned this project — save the next person time)

- **Streamlit Cloud caching gotcha**: a git push triggers a hot "Updated app!" that does **not** clear
  `@st.cache_data`. After a deploy, the pages may show a stale data-source label. Fix: **Manage app →
  ⋮ → Reboot app** (full restart clears the cache). A push that changes deps also clears it.
- **Cloud rebuild is slow** (a few minutes; reinstalls `akshare` and friends). Don't double-push/reboot.
- **Screenshots**: app runs locally on port 8501; screenshots were taken with Playwright driving the
  installed Chrome (`channel="chrome"`, no chromium download). Playwright is in the local `.venv` only,
  intentionally **not** in `requirements.txt`. Naive `chrome --headless --screenshot` only captures the
  Streamlit loading skeleton — wait for rendered content.
- **Local == Cloud versions** (Streamlit 1.58, pandas 3.0, numpy 2.5), so local tests exercise the
  deployed runtime. No version drift.

## Commands

```bash
.venv\Scripts\python.exe -m pytest -q
.venv\Scripts\python.exe -m compileall app.py pages src scripts tests
.venv\Scripts\python.exe -m scripts.build_seed_dataset                 # refresh whole seed snapshot
.venv\Scripts\python.exe -m scripts.verify_company_coverage 600519 002594 300750
.venv\Scripts\streamlit.exe run app.py --server.port 8501 --server.headless true
```

## Do Not Do Yet

- Do not add LLM API calls before summaries are evidence-linked; always keep a non-LLM fallback.
- Do not change risk-rule formulas/thresholds without updating `docs/RISK_RULES_SPEC.md`.
- Do not add banks/insurers/brokers to the universe without a dedicated financial-sector schema.
- Do not commit secrets, paid-database raw data, or large files (see `AGENTS.md`).
