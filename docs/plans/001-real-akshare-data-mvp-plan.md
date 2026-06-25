# Implementation Plan: Real AKShare Data MVP

## Overview

This plan moves the project from sample-only data to a real public-data MVP while preserving the existing app structure. Work is sliced vertically so each step leaves the dashboard runnable.

## Architecture Decisions

- Data Source Agent owns this phase. UI pages should not be rewritten except for small source-status display tweaks.
- Use `src/data/akshare_client.py` as the only AKShare integration point.
- Use normalized annual data as the contract between data and metrics.
- Use source-labeled fallback order: normalized cache -> Eastmoney live -> Sina live -> sample data.
- Use pytest unit tests for mapping and fallback; live network tests stay optional.

## Dependency Graph

```text
Symbol normalization
    |
Raw statement adapters
    |
Annual schema normalization
    |
Cache read/write
    |
fetch_company_financials public API
    |
metrics/risk/export/pages continue to consume standard schema
```

## Task List

### Phase 1: Foundation

## Task 1: Write Spec And Plan

**Description:** Create the written contract for the real AKShare data MVP so future AI sessions know scope, commands, boundaries, and next tasks.

**Acceptance criteria:**

- [x] `docs/specs/001-real-akshare-data-mvp.md` exists.
- [x] `docs/plans/001-real-akshare-data-mvp-plan.md` exists.
- [x] Scope explicitly excludes PDF, LLM, and full peer matching.

**Verification:**

- [x] Manual read of both docs.

**Dependencies:** None

**Files likely touched:**

- `docs/specs/001-real-akshare-data-mvp.md`
- `docs/plans/001-real-akshare-data-mvp-plan.md`

**Estimated scope:** S

## Task 2: Add Mapping And Fallback Tests

**Description:** Write tests that describe the required data-layer behavior before implementation.

**Acceptance criteria:**

- [x] Symbol normalization tests exist.
- [x] Eastmoney raw table normalization test exists.
- [x] Sina raw table normalization test exists.
- [x] Fallback test exists.

**Verification:**

- [x] Initial tests fail before implementation.
- [x] Tests pass after implementation.

**Dependencies:** Task 1

**Files likely touched:**

- `tests/test_akshare_client.py`

**Estimated scope:** S

### Checkpoint: Foundation

- [x] Tests encode the data-layer contract.
- [x] No UI files changed.

### Phase 2: Data Source MVP

## Task 3: Implement Symbol And Statement Normalization

**Description:** Add helpers that convert user symbols and raw AKShare frames into `STANDARD_FINANCIAL_COLUMNS`.

**Acceptance criteria:**

- [x] `normalize_a_share_symbol()` returns Eastmoney and Sina symbol formats.
- [x] Eastmoney statement frames can be merged by annual report year.
- [x] Sina statement frames can be merged by annual report year.
- [x] Standard columns are numeric where metrics expect numeric values.

**Verification:**

- [x] `pytest -q tests/test_akshare_client.py`

**Dependencies:** Task 2

**Files likely touched:**

- `src/data/akshare_client.py`
- `src/data/schema.py`
- `tests/test_akshare_client.py`

**Estimated scope:** M

## Task 4: Implement Cache And Public Fetch Fallback

**Description:** Wire normalized cache and live-source fallback into `fetch_company_financials()`.

**Acceptance criteria:**

- [x] Cache is read before live calls unless `prefer_live=False` forces cache/sample path.
- [x] Live Eastmoney source is tried before Sina.
- [x] Any live-source failure falls through safely.
- [x] Sample fallback warning is explicit.

**Verification:**

- [x] `pytest -q`
- [x] `compileall app.py pages src tests`

**Dependencies:** Task 3

**Files likely touched:**

- `src/data/akshare_client.py`
- `src/data/cache.py`
- `tests/test_akshare_client.py`

**Estimated scope:** M

### Checkpoint: Data Source MVP

- [x] `fetch_company_financials("600519")` returns standard rows from live/cache/sample.
- [x] Existing metrics and risk rules run on returned data.

### Phase 3: Reader-Facing Product Polish

## Task 5: Add Data Source Status To Pages

**Description:** Make the existing pages show whether data came from live AKShare, cache, or sample fallback.

**Acceptance criteria:**

- [x] Company page displays source status.
- [x] Risk/export pages preserve current warning behavior.
- [x] No business logic moves into pages.

**Verification:**

- [x] Manual Streamlit smoke test.

**Dependencies:** Task 4

**Files likely touched:**

- `pages/01_company_analysis.py`
- `pages/03_risk_rules.py`
- `pages/04_export_center.py`
- `docs/PAGE_REGISTRY.md`

**Estimated scope:** S

## Task 6: Expand Real Company Coverage

**Description:** Verify and document at least three real companies across common non-financial industries.

**Acceptance criteria:**

- [x] `600519`, `002594`, `300750` tested or documented with current upstream status.
- [x] Known source failures recorded in task log.
- [x] README updated with live-data caveat.

**Verification:**

- [x] Manual smoke test for each symbol.

**Dependencies:** Task 5

**Files likely touched:**

- `README.md`
- `docs/TASK_LOG.md`

**Estimated scope:** S

### Checkpoint: MVP Complete

- [x] All tests pass.
- [x] Streamlit app runs.
- [x] At least one company returns live or cached public data.
- [x] Sample fallback remains available and labeled.
- [x] Three-symbol coverage documented in Task 6.

## Risks and Mitigations

| Risk | Impact | Mitigation |
|---|---:|---|
| AKShare upstream SSL or schema instability | High | Cache normalized data; fallback to Sina; fallback to sample with warning |
| Eastmoney fields differ by industry | Medium | Keep source-specific mapping functions; mark financial firms as future scope |
| Sina and Eastmoney field definitions differ | Medium | Document source priority and mapping choices in `DATA_DICTIONARY.md` |
| Live network tests become flaky | Medium | Keep live checks manual or optional; unit-test with raw fixture frames |

## Parallelization Opportunities

- Safe to parallelize after Task 4: README polish, UI source-status display, export formatting.
- Must be sequential: schema mapping before metrics/risk changes.
- Needs coordination: any change to metric formulas or risk thresholds.

## Next Step For Another AI

Task 6 is complete. The next AI should add a small README screenshot/GIF or prepare the Streamlit Cloud deployment checklist, without changing metric formulas or risk thresholds.
