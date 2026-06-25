# Implementation Plan: Functional Depth — Evidence Summary And Report

## Overview

This plan turns the dashboard from a data viewer into a recruiter-facing analysis product. The guiding rule is evidence first: every narrative conclusion must trace back to metrics or transparent risk-rule evidence. LLM polishing is optional and must never replace the non-LLM fallback.

## Architecture Decisions

- Keep deterministic summary logic in `src/ai/summary.py`.
- Keep optional LLM prompt templates in `src/ai/prompts.py`; no API call is allowed until evidence-linked summaries are stable.
- Reuse the same `EvidenceLinkedSummary.evidence` table for page display, future PDF, and possible LLM grounding.
- Do not change financial metric formulas or risk-rule thresholds in this main line.

## Task List

### Task 1: Evidence-Linked Rule Summary

**Description:** Replace the plain paragraph summary with a deterministic summary object containing a narrative and an evidence table. Each claim in the narrative cites `[E#]`, and `[E#]` appears in the table.

**Acceptance criteria:**

- [x] `build_evidence_linked_summary()` returns narrative plus evidence table.
- [x] The company analysis page shows the narrative and evidence table.
- [x] The old `build_rule_based_summary()` still works as a string fallback.
- [x] No LLM API call is introduced.

**Verification:**

- [x] `pytest -q tests/test_ai_summary.py`
- [x] Full test suite passes.

**Files touched:**

- `src/ai/summary.py`
- `src/ai/__init__.py`
- `pages/01_company_analysis.py`
- `tests/test_ai_summary.py`

**Estimated scope:** S

### Task 2: One-Page PDF Report

**Description:** Build a one-page company report export that reuses the same summary narrative and evidence table, plus selected metrics and risk signals.

**Acceptance criteria:**

- [x] PDF export uses existing metrics/risk/summary outputs; no duplicate formulas.
- [x] Export center offers a clearly labeled one-page company report.
- [x] PDF includes data source label and "not investment advice" disclaimer.

**Verification:**

- [x] Focused export test checks bytes are generated and required text appears when feasible.
- [x] Rendered sample PDF page visually checked from PNG.
- [x] Streamlit export page smoke test confirms Excel/PDF download controls render.

**Dependencies:** Task 1

**Files likely touched:**

- `src/export/pdf_exporter.py`
- `pages/04_export_center.py`
- `tests/`

**Estimated scope:** M

### Task 3: Optional LLM Polish

**Description:** Add optional LLM wording polish only after Task 1 evidence is stable. The LLM input must include evidence rows, and the app must keep the deterministic summary when secrets are absent.

**Acceptance criteria:**

- [ ] No secret is committed.
- [ ] LLM output must preserve evidence references.
- [ ] Non-LLM fallback remains the default safe path.

**Verification:**

- [ ] Tests cover fallback path without secrets.
- [ ] Prompt contract is documented.

**Dependencies:** Task 1

**Files likely touched:**

- `src/ai/prompts.py`
- `src/ai/summary.py`
- `docs/`

**Estimated scope:** M

## Next Step

Task 1 and Task 2 are complete. The next AI may choose Task 3: optional LLM polish that preserves `[E#]` references and keeps deterministic fallback. A safer alternative is export polish: add chart images to the PDF or improve Excel styling without changing formulas.
