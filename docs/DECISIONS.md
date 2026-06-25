# Decision Log

记录架构、产品和口径决策。新 AI 不要反复推翻已定边界，除非用户明确要求。

## 2026-06-25 - Initial Project Skeleton

- Decision: 使用 Streamlit multipage 架构，页面放在 `app.py` 和 `pages/`。
- Decision: 业务逻辑集中在 `src/`，按 data/metrics/risk/ai/export/ui 分层。
- Decision: 第一版使用透明风险规则，不做黑箱 ML 风险评分。
- Decision: 导出功能第一阶段优先 Excel，PDF 作为后续增强。
- Decision: 使用 `AGENTS.md`、`docs/PAGE_REGISTRY.md`、`docs/TASK_LOG.md` 控制后续 AI 协作边界。

## 2026-06-25 - Real AKShare Data MVP Slice 1

- Decision: 数据层优先使用 AKShare 东财年度三大表，若上游失败则尝试新浪三大表。
- Decision: `fetch_company_financials()` 的 fallback order 为 normalized cache -> Eastmoney live -> Sina live -> labeled sample data。
- Decision: 标准化缓存写入 `data/cache/normalized_financials_<symbol>.csv`，该目录默认不进入 Git。
- Decision: `net_profit` 优先使用归母净利润；若缺失则使用净利润。
- Decision: 暂不为金融行业单独建 schema，先以非金融 A 股公司为 MVP 范围。

## 2026-06-25 - Data Depth & Robustness: Committed Seed Layer

- Decision: 新增**已提交的 seed 快照层** `data/seed/financials/<code>.csv`，存放标准化后的公开年报数据，随仓库进入 Git。与 `data/cache/`（本地易变、不提交）区分：seed 是版本化真实数据快照。
- Decision: `fetch_company_financials()` 兜底链调整为 `seed:normalized -> cache:normalized -> Eastmoney live -> Sina live -> sample`；seed 命中时 `source="seed:normalized"`。`prefer_live=False` 仍强制走 labeled sample（离线/测试路径），不被 seed 覆盖。
- Decision: 引入精选公司宇宙 `src/data/universe.py`（~28 家非金融大盘股，含 industry 标签），作为 seed 构建范围与未来真实同业分组的口径来源。银行/保险/券商仍排除（三表 schema 不同）。
- Rationale: 让 Streamlit Cloud 干净环境无需联网即可展示真实数据，消除"首跑依赖易失败 live AKShare"的软肋；live 退化为刷新/补充手段。seed 为公开财报数据，不违反禁止提交付费数据库原始数据的约定。
- 详见 `docs/plans/002-data-depth-robustness-plan.md`。
