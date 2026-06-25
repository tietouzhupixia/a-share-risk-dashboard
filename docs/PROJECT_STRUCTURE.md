# Project Structure

本文件说明“什么东西放哪里”。后续 AI 如果不确定，优先查这里，不要凭感觉新建目录。

## Top-Level Layout

```text
a-share-risk-dashboard/
├── app.py                       # Streamlit landing page and navigation
├── pages/                       # Streamlit multipage entry files
├── src/                         # Reusable business logic
├── docs/                        # Documentation and AI coordination files
├── data/                        # Local raw/processed/cache data, not private datasets
├── outputs/                     # Generated reports, exports, figures
├── scripts/                     # Reproducible maintenance and verification scripts
├── tests/                       # Unit and smoke tests
├── requirements.txt             # Streamlit Cloud dependencies
├── pyproject.toml               # Tool configuration
├── AGENTS.md                    # AI collaboration contract
└── README.md                    # Public project explanation
```

## `app.py`

放项目入口、页面导航、项目定位、样例公司提示。不要在这里写财务计算和风险规则。

## `pages/`

放 Streamlit 页面。每个页面是一个可展示的产品视图。

Current pages:

- `01_company_analysis.py`
- `02_peer_comparison.py`
- `03_risk_rules.py`
- `04_export_center.py`

新增页面时必须同步更新 `docs/PAGE_REGISTRY.md`。

## `src/data/`

放数据层代码。

- `akshare_client.py`：所有 AKShare 请求、fallback 和缓存入口。
- `seed.py`：已提交真实快照 `data/seed/` 的读写，位于兜底链最前面。
- `universe.py`：精选公司宇宙（code/name/industry），seed 构建范围与同业分组口径。
- `cache.py`：本地缓存读写。
- `schema.py`：标准字段名和数据契约。
- `sample_data.py`：无网络或接口失败时的演示数据。

禁止把风险解释、页面 UI 或导出逻辑放进这里。

## `src/metrics/`

放财务指标计算。

典型内容：

- 增长率
- ROA
- 资产负债率
- 经营现金流/净利润
- 应收账款/营业收入
- 存货/营业收入
- 应收账款周转天数

## `src/risk/`

放透明风险规则。

每条规则都要能回答：

- 触发了什么？
- 哪些数据触发？
- 风险等级是什么？
- 可能的业务解释是什么？

## `src/ai/`

放摘要生成逻辑。第一版优先做规则摘要，LLM 只做可选润色。

不要让 LLM 直接生成无证据结论。

## `src/export/`

放 Excel、PDF、图片导出逻辑。导出文件默认写入 `outputs/`，Streamlit 下载按钮可以使用内存对象。

## `src/ui/`

放图表、指标卡、布局组件。页面文件应尽量调用这里的组件。

## `docs/`

项目治理文件：

- `AGENT_BRIEFS.md`：角色分工。
- `AI_WORKFLOW.md`：AI 修改流程。
- `PAGE_REGISTRY.md`：页面登记簿。
- `DATA_DICTIONARY.md`：字段和指标字典。
- `RISK_RULES_SPEC.md`：风险规则说明。
- `DECISIONS.md`：架构和产品决策记录。
- `TASK_LOG.md`：每次 AI 工作日志。
- `specs/`：重要功能的规格说明。
- `plans/`：可交接的任务拆分和检查点。
- `NEXT_STEPS.md`：下一位 AI 的快速接手说明。

## `data/`

- `data/seed/financials/<code>.csv`：**已提交**的标准化公开年报快照（进 Git），让云端无需联网即出真实数据。
- `data/raw/`：原始公开数据缓存（不进 Git）。
- `data/processed/`：清洗后的中间数据（不进 Git）。
- `data/cache/`：接口缓存（不进 Git）。

不要提交大文件、私有数据、付费数据库原始数据。`data/seed/` 只放公开财报快照。

## `outputs/`

- `outputs/exports/`：Excel。
- `outputs/figures/`：图表图片。
- `outputs/reports/`：PDF 或报告文件。

这些是生成物，默认不进入 Git。

## `scripts/`

放可重复执行的项目维护脚本，例如真实公司覆盖验证。不要把一次性探索代码放在根目录；如果脚本会影响数据、缓存或文档，必须在 `docs/TASK_LOG.md` 说明用途和运行结果。
