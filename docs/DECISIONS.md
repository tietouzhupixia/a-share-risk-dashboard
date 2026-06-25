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
