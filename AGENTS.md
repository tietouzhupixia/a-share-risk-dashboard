# AI Collaboration Contract

本文件是本项目给所有 AI/Agent/Copilot/Codex/Claude 的最高优先级协作规则。任何 AI 在修改代码前，必须先阅读本文件和 `docs/PROJECT_STRUCTURE.md`。

## Project Identity

- 项目名：A-Share Financial Risk Intelligence Dashboard
- 中文名：AI上市公司经营风险分析台
- 目标：输入一家 A 股公司，生成财务趋势、同业比较、风险预警和一页式分析摘要。
- 求职定位：金融研究、数据分析、经营分析、风险管理、商业分析、AI 产品化。

## Non-Negotiable Rules

1. 页面文件只允许放在 `app.py` 和 `pages/`。
2. 页面文件只负责展示和编排，不写复杂业务逻辑。
3. 数据获取放在 `src/data/`。
4. 财务指标放在 `src/metrics/`。
5. 风险规则放在 `src/risk/`。
6. AI 摘要和提示词放在 `src/ai/`。
7. 导出逻辑放在 `src/export/`。
8. 图表和页面组件放在 `src/ui/`。
9. 新增、删除或实质修改页面后，必须更新 `docs/PAGE_REGISTRY.md`。
10. 每次 AI 完成工作后，必须更新 `docs/TASK_LOG.md`。
11. 改变数据字段、指标口径或风险规则后，必须更新对应文档：
    - 字段/数据源：`docs/DATA_DICTIONARY.md`
    - 指标/风险规则：`docs/RISK_RULES_SPEC.md`
    - 架构决策：`docs/DECISIONS.md`
12. 不允许把密钥、Wind/CSMAR 原始数据、个人隐私数据提交进仓库。
13. 不允许把临时分析脚本散落在根目录。探索脚本统一放到 `scripts/`，若创建则必须说明用途。

## Directory Ownership

| Path | Owner Role | What Goes Here | What Must Not Go Here |
|---|---|---|---|
| `app.py` | Streamlit UI Agent | 首页、导航入口、项目说明 | 数据清洗、指标计算、复杂规则 |
| `pages/` | Streamlit UI Agent | 多页面入口文件 | 可复用业务逻辑 |
| `src/data/` | Data Source Agent | AKShare 客户端、缓存、字段标准化 | 风险解释、页面布局 |
| `src/metrics/` | Metrics Agent | 增长率、ROA、杠杆、现金流质量等指标 | Streamlit 组件 |
| `src/risk/` | Risk Rules Agent | 透明风险规则、风险等级、触发证据 | LLM 提示词 |
| `src/ai/` | AI Summary Agent | 规则摘要、LLM prompt、摘要后处理 | 原始财务拉取 |
| `src/export/` | Export Agent | Excel/PDF/图片导出 | 页面状态管理 |
| `src/ui/` | UI Agent | 图表、指标卡、布局组件 | 数据源调用细节 |
| `docs/` | Documentation Agent | 项目地图、页面登记、规则说明、日志 | 代码实现 |
| `data/` | Data Agent | 本地缓存和示例数据 | 私有付费数据库原始数据 |
| `outputs/` | Export Agent | 用户生成的报告和图表 | 源代码 |
| `tests/` | QA Agent | 指标、规则、导出测试 | 生产数据 |

## Agent Roles

选择最贴近当前任务的角色工作，并遵守对应边界。详细职责见 `docs/AGENT_BRIEFS.md`。

- Project Architect：只改架构、目录、规范、跨模块契约。
- Data Source Agent：只处理 AKShare、缓存、字段映射、异常兜底。
- Metrics & Risk Agent：只处理财务指标、风险规则、证据表。
- Streamlit UI Agent：只处理 `app.py`、`pages/` 和 `src/ui/`。
- AI Summary Agent：只处理摘要生成、提示词和证据引用。
- Export Agent：只处理 Excel、PDF、图片导出。
- QA & Deploy Agent：只处理测试、依赖、部署配置。
- Documentation Agent：只处理 README、docs、页面登记、任务日志。

## Required Workflow For Every AI Session

1. Read:
   - `AGENTS.md`
   - `docs/PROJECT_STRUCTURE.md`
   - `docs/PAGE_REGISTRY.md`
   - `docs/TASK_LOG.md`
2. Identify the role you are acting as.
3. Before editing, inspect existing related files.
4. Keep changes inside the correct module boundary.
5. If you add a function, add or update a focused test when reasonable.
6. If you add/change a page, update `docs/PAGE_REGISTRY.md`.
7. If you add/change an indicator or risk rule, update `docs/RISK_RULES_SPEC.md`.
8. At the end, update `docs/TASK_LOG.md` with:
   - date
   - acting role
   - files changed
   - reason
   - next recommended step

## Page Rules

Every page in `pages/` must satisfy:

- Filename format: `NN_short_english_name.py`
- Has a single `render()` function where possible.
- Calls reusable functions from `src/`.
- Does not directly call AKShare unless there is no existing wrapper.
- Has an entry in `docs/PAGE_REGISTRY.md`.

## Data Rules

- AKShare calls must be wrapped in `src/data/akshare_client.py`.
- Add retry/cache behavior before doing batch calls.
- Normalize external column names before metrics use them.
- Use `src/data/sample_data.py` only as local fallback/demo, never as final evidence without labeling it.

## Risk Rule Rules

- Every risk signal must include:
  - risk name
  - level
  - trigger reason
  - evidence fields
  - possible business interpretation
- Do not create a black-box risk score until the transparent rules are stable.
- Do not present AI-generated wording without underlying evidence.

## Handoff Format

At the end of every AI work session, add a short entry to `docs/TASK_LOG.md`:

```markdown
## YYYY-MM-DD HH:MM - Role Name

- Goal:
- Changed:
- Verified:
- Decisions:
- Next:
```

## Definition Of Done

A change is not complete unless:

- Code is in the right directory.
- Documentation impacted by the change is updated.
- Tests or a smoke check were run when feasible.
- The app still has a clear path to public Streamlit deployment.

