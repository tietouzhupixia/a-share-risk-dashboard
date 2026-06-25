# AI Workflow

这个文件是给后续 AI 的操作流程，目标是防止项目越写越乱。

## Before Editing

1. Read `AGENTS.md`.
2. Read this file.
3. Read `docs/PAGE_REGISTRY.md`.
4. Read recent entries in `docs/TASK_LOG.md`.
5. Identify your acting role:
   - Project Architect
   - Data Source Agent
   - Metrics & Risk Agent
   - Streamlit UI Agent
   - AI Summary Agent
   - Export Agent
   - QA & Deploy Agent
   - Documentation Agent

## During Editing

- Keep code in its owning module.
- Prefer small functions with typed inputs/outputs.
- Pages should call `src/` functions; pages should not become notebooks.
- Do not introduce new dependencies unless they are added to `requirements.txt`.
- Do not silently change metric definitions.
- Do not remove another AI/user's work unless the user explicitly asks.

## After Editing

Update the right governance file:

| Change Type | Required Update |
|---|---|
| New/changed Streamlit page | `docs/PAGE_REGISTRY.md` |
| New/changed data source | `docs/DATA_DICTIONARY.md` |
| New/changed metric | `docs/DATA_DICTIONARY.md` and `docs/RISK_RULES_SPEC.md` if used in rules |
| New/changed risk rule | `docs/RISK_RULES_SPEC.md` |
| Architecture decision | `docs/DECISIONS.md` |
| Any AI session | `docs/TASK_LOG.md` |

## Smoke Checks

Run what is relevant:

```bash
python -m compileall app.py pages src tests
pytest
streamlit run app.py
```

If a command cannot be run, write the reason in `docs/TASK_LOG.md`.

## Handoff Note

Every AI session should leave enough context for the next AI:

```markdown
## YYYY-MM-DD HH:MM - Role

- Goal:
- Changed:
- Verified:
- Decisions:
- Next:
```

