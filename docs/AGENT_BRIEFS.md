# Agent Briefs

这些不是外部平台的强制 agent 文件，而是本项目内部的角色协议。任何 AI 都可以选择一个角色来工作，避免跨边界乱改。

## Project Architect

- Use when: 目录、模块边界、跨模块契约、依赖策略发生变化。
- Allowed paths: `AGENTS.md`, `docs/`, `pyproject.toml`, `requirements.txt`, high-level package `__init__.py`.
- Avoid: 直接实现业务功能。
- Done when: 架构决策记录在 `docs/DECISIONS.md`，结构说明同步更新。

## Data Source Agent

- Use when: 接入 AKShare、缓存、字段映射、异常兜底、样例数据。
- Allowed paths: `src/data/`, `data/`, `docs/DATA_DICTIONARY.md`, tests for data shape.
- Avoid: 在页面里直接写 AKShare 调用。
- Done when: 数据输出符合 `src/data/schema.py`，失败时有明确 fallback。

## Metrics & Risk Agent

- Use when: 新增财务指标、风险规则、风险等级或证据字段。
- Allowed paths: `src/metrics/`, `src/risk/`, `docs/RISK_RULES_SPEC.md`, tests.
- Avoid: 让 LLM 生成没有数据证据的结论。
- Done when: 规则输出包含 level、reason、evidence、interpretation。

## Streamlit UI Agent

- Use when: 页面布局、图表、交互、用户体验。
- Allowed paths: `app.py`, `pages/`, `src/ui/`, `docs/PAGE_REGISTRY.md`.
- Avoid: 把业务逻辑塞进页面。
- Done when: 页面登记簿更新，页面能独立解释它展示什么。

## AI Summary Agent

- Use when: 生成摘要、prompt、证据引用、LLM 可选接入。
- Allowed paths: `src/ai/`, `docs/RISK_RULES_SPEC.md`, README demo text.
- Avoid: 直接写死投资建议或无证据判断。
- Done when: 摘要每个关键结论可追溯到指标或风险信号。

## Export Agent

- Use when: Excel/PDF/图片导出。
- Allowed paths: `src/export/`, `outputs/`, export page, export tests.
- Avoid: 在页面里手写复杂导出逻辑。
- Done when: 用户能下载文件，导出字段和页面展示口径一致。

## QA & Deploy Agent

- Use when: 测试、依赖、Streamlit Cloud 部署、CI。
- Allowed paths: `tests/`, `requirements.txt`, `.streamlit/`, `.github/`, README setup section.
- Avoid: 改业务口径。
- Done when: smoke checks 记录在 `docs/TASK_LOG.md`。

## Documentation Agent

- Use when: README、项目说明、页面登记、任务日志、求职包装。
- Allowed paths: `README.md`, `docs/`.
- Avoid: 未验证地夸大功能。
- Done when: 文档和实际文件一致。

