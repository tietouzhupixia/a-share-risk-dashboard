# Page Registry

每次新增、删除、重命名或实质修改页面，必须更新本文件。

| Page File | Page Name | Owner Role | Purpose | Primary Modules Used | Status |
|---|---|---|---|---|---|
| `app.py` | 首页 | Streamlit UI Agent | 项目入口、导航、样例公司 | `src/config.py`, `src/ui/layout.py` | Stable |
| `pages/01_company_analysis.py` | 公司分析 | Streamlit UI Agent | 公司查询、核心指标卡、趋势图、证据绑定摘要、摘要证据表、数据来源状态 | `src/data/`, `src/metrics/`, `src/risk/`, `src/ai/`, `src/ui/` | MVP |
| `pages/02_peer_comparison.py` | 同业比较 | Streamlit UI Agent | 真实同行业指标横向比较（基于 seed 快照），含数据来源提示 | `src/data/`, `src/metrics/`, `src/ui/` | MVP |
| `pages/03_risk_rules.py` | 风险预警 | Streamlit UI Agent | 展示透明风险规则、触发证据和数据来源状态 | `src/risk/`, `src/data/`, `src/metrics/`, `src/ui/` | MVP |
| `pages/04_export_center.py` | 导出中心 | Streamlit UI Agent | 下载 Excel 与一页式 PDF 公司风险报告，展示数据来源状态 | `src/export/`, `src/data/`, `src/metrics/`, `src/ai/`, `src/ui/` | MVP |

## Update Checklist

When a page changes:

- [ ] Page file exists.
- [ ] Page purpose is still accurate.
- [ ] Imported modules are listed.
- [ ] Status updated: Skeleton / MVP / Stable / Deprecated.
- [ ] Related task logged in `docs/TASK_LOG.md`.
