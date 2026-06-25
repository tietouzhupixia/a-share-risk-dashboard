# Implementation Plan: Data Depth & Robustness

主线：把项目从"3 家公司 + 易失败的 live AKShare"升级为"几十家公司 + 云端始终有真实数据"，
体现数据工程能力。**不改财务指标公式、风险规则阈值；UI 仅做必要的来源标注。**

## Overview

当前 `fetch_company_financials` 的兜底链是 `cache → Eastmoney live → Sina live → sample`，
而 `data/cache/` 不进 Git。所以云端是干净环境，首跑只能依赖易失败的 live AKShare，失败就退样例。

本主线引入一个**已提交的 seed 快照层**：把精选公司宇宙的标准化公开财报预生成成 CSV 并提交进仓库，
放在兜底链最前面。这样无论本地还是云端，demo 都先命中真实数据，live 只作为刷新/补充。

## Architecture Decisions

- **新增 seed 层（committed real data）**：`data/seed/financials/<code>.csv` 存放标准化后的公开年报快照，
  随仓库提交（区别于易变、不提交的 `data/cache/`）。兜底链变为
  `seed → cache → Eastmoney live → Sina live → sample`，seed 命中时 `source="seed:normalized"`。
  理由：seed 是**版本化的真实数据快照**，让云端 demo 稳定、可复现；cache 仍保持"本地易变缓存"的原定语义。
- **公司宇宙登记表**：`src/data/universe.py` 维护 ~28 家**非金融**大盘股（code、name、industry）。
  暂不纳入银行/保险/券商（三表 schema 不同，与 `DECISIONS.md` 既有约定一致），保证核心字段口径统一。
- **可复现的 seed 构建脚本**：`scripts/build_seed_dataset.py` 对宇宙逐只拉 live、标准化、写 seed，
  带重试与覆盖报告。这是数据工程的核心交付物：一条命令即可刷新整份快照。
- **数据质量校验**：把"缺字段/年份跨度/重复年份"等校验沉淀为可测的 `src/data/quality.py`，
  并扩展 `verify_company_coverage` 覆盖整份宇宙。
- **不动 `.gitignore` 的 cache 规则**：`data/seed/` 不在忽略清单内，默认就会被 Git 跟踪；
  seed 是公开财报数据，不违反"禁止提交付费数据库原始数据"。

## Task List

### Phase 1: Foundation（seed 管道，先用现有数据落地）

- [x] **Task 1 — Universe 登记表**（S）
  - `src/data/universe.py`：~28 家非金融大盘股 `(code, name, industry)` + 查询 helper（按 code、按行业）。
  - 验收：宇宙含已有 4 家；无重复 code；每条都有非空 industry；六位代码合法。
  - 测试：`tests/test_universe.py`。
- [x] **Task 2 — Seed 读取与兜底链接入**（M）
  - `src/data/seed.py`：`read_seed_financials(code)` 读 `data/seed/financials/<code>.csv`。
  - `fetch_company_financials`：在最前面加 seed 命中分支，`source="seed:normalized"`。
  - 用现有 3 份标准化缓存（600519/002594/300750）+ 4 号公司，先生成对应 seed 文件落地。
  - 验收：seed 存在时优先于 cache/live；seed 缺失时退回原链路不变。
  - 测试：`tests/test_seed_fallback.py`（seed 优先级、缺失回退）。
- [x] **Task 3 — 文档与来源标注**（S）
  - `src/ui/source_status.py` 识别 `seed:normalized` 文案（"已提交的标准化快照"）。
  - 更新 `DECISIONS.md`（seed 架构）、`DATA_DICTIONARY.md`（seed 来源）、`PROJECT_STRUCTURE.md`（data/seed）。

### Checkpoint: Foundation
- [x] `pytest -q` 全绿；`compileall` 通过。
- [x] 本地 `fetch_company_financials("600519")` 命中 `seed:normalized`。
- [x] 现有 3-4 家公司即使删掉 cache、断网也能出真实数据。

### Phase 2: Thickness（拉满整份宇宙）

- [x] **Task 4 — Seed 构建脚本**（M）
  - `scripts/build_seed_dataset.py`：逐只 live 拉取 + 标准化 + 写 seed + 重试 + 覆盖报告（markdown/json）。
  - 测试：用 fixture/mock 验证写入与报告逻辑，不依赖真实网络。
- [x] **Task 5 — 跑数据，填满宇宙**（M，需联网）
  - 运行脚本生成 ~28 家 seed CSV 并提交；失败的逐只重试/记录。
  - 验收：≥24 家核心字段无缺失、年份跨度合理。
- [x] **Task 6 — 数据质量校验 + 覆盖报告**（S）
  - `src/data/quality.py` + 扩展 `verify_company_coverage` 到整份宇宙；README 覆盖表从 3 → 全宇宙。

### Checkpoint: Thickness
- [x] 整份宇宙覆盖报告可一键生成；README 覆盖表更新。

### Phase 3: Real peers + 云端稳健（主线收益兑现）

- [x] **Task 7 — 行业分组真实同业**（M）
  - `fetch_peer_snapshot` 用 universe 的 industry 标签 + seed 财报 + 现有 metrics 组装真实同业，替换样例。
  - 不改指标公式；同业页来源标注更新。
  - 测试：`tests/test_peer_snapshot.py`。
- [x] **Task 8 — 云端稳健验证 + 文档**（S）
  - push 后确认线上各页对整份宇宙命中 `seed:normalized`；更新 `DEPLOYMENT.md`、`NEXT_STEPS.md`。

### Checkpoint: Complete
- [x] 线上 demo 对整份宇宙稳定出真实数据；同业页为真实行业口径。

## Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| live AKShare 逐只拉取慢/偶发失败 | Med | 构建脚本带重试；seed 一次成功后提交，运行期不再依赖 live |
| 个别公司字段映射缺口（特殊行业） | Med | 宇宙先选非金融大盘股；质量校验暴露缺字段，按需补映射或剔除 |
| seed 数据量过大 | Low | 标准化 CSV 每家 ~3-4KB，~28 家约 100KB，提交无压力 |
| 误改指标/风险口径 | High | 本主线只动 `src/data/`、脚本、文档；指标/风险文件零改动 |

## Open Questions

- 宇宙规模先定 ~28 家非金融大盘股；如需覆盖银行/保险，需要后续单独的金融业 schema 适配（不在本主线）。
