# Task Log

每次 AI 工作后必须新增一条记录。最新记录放在最上方。

## 2026-06-25 16:00 - Shipping & Launch / Documentation Agent

- Goal: 用户已把仓库 push 到 GitHub 并在 Streamlit Community Cloud 部署成功，拿到公开 URL；把上线信息写回交接文档。不改任何指标公式、风险阈值、UI 或功能。
- Changed: `README.md` 顶部新增 Live Demo 链接、`Deployment` 段改为"已部署"并附 URL；`docs/DEPLOYMENT.md` 新增"当前部署状态"段（URL、仓库、冒烟结果）；`docs/NEXT_STEPS.md` 标记部署完成，下一步改为产品深化三选一。仅文档改动。
- Verified: `curl` 访问 https://a-share-risk-dashboard-hmft7s3jyqsew6doqizjpp.streamlit.app/ 返回 HTTP 303（Streamlit 正常重定向到加载页），约 4s，说明线上可达。GitHub 仓库 https://github.com/tietouzhupixia/a-share-risk-dashboard 已存在。部署过程：用户本地 git init/commit/push；首次 push 因 SOCKS5 代理导致 GCM 浏览器登录失败，改用 PAT 手动登录成功；Streamlit Cloud 选 main 分支、入口 app.py 部署成功。
- Decisions: 公开 URL 同时写进 README 顶部、README Deployment 段、docs/DEPLOYMENT.md 三处，方便招聘方和后续 AI。代理环境下 GitHub HTTPS 登录建议用 Personal Access Token，而非浏览器流。
- Next: 线上冒烟（点四个页面、试 600519/002594/300750、记录云端各自命中 live/sample），或推进真实行业同业口径，或 PDF/AI 摘要润色（仍受 NEXT_STEPS 的 Do Not Do Yet 约束）。

## 2026-06-25 15:30 - Shipping & Launch / Documentation Agent

- Goal: 执行 `docs/NEXT_STEPS.md` 的作品集包装下一步——给 README 增加运行截图；不改财务指标公式、风险阈值，不重构 UI，不新增 PDF/LLM/真实同业功能。
- Changed: 新增 `docs/assets/00_home.png`、`01_company_analysis.png`、`02_peer_comparison.png`、`03_risk_rules.png`、`04_export_center.png`（本地真实渲染截图）；`README.md` 在简介后新增 `界面预览 (Screenshots)` 段（公司分析页 + 风险预警页为主图，其余三页折叠）；更新 `docs/NEXT_STEPS.md`（截图已完成，下一步收敛为真正部署，并记录截图复现方法）。未改任何 `src/`、`pages/`、配置或指标/规则文件。
- Verified: 本地 `streamlit run app.py`（8501）健康检查 200。用 Playwright 驱动已安装的 Chrome（channel=chrome，无需下载 chromium）对五个页面 `wait_for_selector` 等真实内容渲染后 full_page 截图；逐张核对：公司分析页显示 002594 比亚迪指标卡（营收增速3.5%、ROA3.7%、资产负债率70.7%）+ 两张趋势图 + 数据来源 caption；风险预警页显示 HIGH_LEVERAGE/INVENTORY_GROWTH_GT_REVENUE/SHORT_DEBT_JUMP 触发信号、规则证据、指标基础表；同业比较页显示横向柱状图 + 本地演示同业 warning；导出中心显示下载按钮。运行 `.venv\Scripts\python.exe -m pytest -q` 与 `.venv\Scripts\python.exe -m compileall app.py pages src scripts tests`，结果见下方。
- Decisions: 截图资源放 `docs/assets/`（docs 已纳入 Git，不在 .gitignore 排除范围），不放 `outputs/figures/`（那里被 .gitignore 忽略，无法随 README 展示）。截图工具 Playwright 只装进本地 `.venv`，刻意不写入 `requirements.txt`，避免影响 Streamlit Cloud 部署；截图脚本作为一次性脚本放在仓库外的临时目录，不散落进根目录或 `scripts/`。朴素 `chrome --headless --screenshot` 只能截到 Streamlit 加载骨架，必须等待渲染完成才能截到真实内容。
- Next: 按 `docs/DEPLOYMENT.md` 真正部署到 Streamlit Community Cloud（push GitHub → 创建 app → 选 Python 3.10/3.11 → 冒烟检查），并把公开 URL 写回 README 和 `docs/DEPLOYMENT.md`。

## 2026-06-25 15:20 - QA & Deploy / Documentation Agent

- Goal: 整理 Streamlit Community Cloud 部署检查清单；不改财务指标公式、风险阈值和 UI，不新增 PDF/LLM/真实同业功能。
- Changed: 新增 `docs/DEPLOYMENT.md`（逐项部署清单：仓库准备、入口/依赖核对、Cloud 创建、首跑数据 fallback 行为、冒烟检查、维护）；`README.md` 新增 `Deployment (Streamlit Community Cloud)` 段，说明入口 `app.py`、`requirements.txt`、AKShare live 依赖、`data/cache` 不进 Git、sample fallback 兜底；更新 `docs/NEXT_STEPS.md` 把下一步改为 README 截图/GIF 或实际执行部署。
- Verified: 未改任何代码或配置文件，仅文档。运行 `.venv\Scripts\python.exe -m pytest -q` 与 `.venv\Scripts\python.exe -m compileall app.py pages src scripts tests`，结果见本条目下方运行记录。复核 `.gitignore` 确认 `data/cache/*`、`.streamlit/secrets.toml`、`.venv/`、`outputs/*` 均已排除；确认 `app.py` 为入口、`requirements.txt` 含 akshare。
- Decisions: 部署清单只覆盖部署，不动指标/规则/UI。Python 版本不新建 `runtime.txt`，改为在清单里指引在 Cloud Advanced settings 选 3.10/3.11，避免新增配置文件。Secrets 当前 MVP 留空，仅为未来 LLM 预留说明。
- Next: 做 README 截图/GIF，或按 `docs/DEPLOYMENT.md` 实际部署并记录公开 URL。

## 2026-06-25 15:04 - Data Source / Documentation Agent

- Goal: 执行 Task 6，验证 `600519`、`002594`、`300750` 三家真实公司覆盖情况，并把可复查入口和 README caveat 补齐。
- Changed: 新增 `scripts/verify_company_coverage.py`、`scripts/__init__.py`、`tests/test_verify_company_coverage.py`；更新 `README.md` 的三家公司验证表、AKShare live/cache/sample 说明和重跑命令；更新 `docs/PROJECT_STRUCTURE.md`、`docs/plans/001-real-akshare-data-mvp-plan.md`、`docs/NEXT_STEPS.md`。
- Verified: TDD RED 阶段先确认 `tests/test_verify_company_coverage.py` 因缺少 `scripts` 失败；实现脚本后该测试通过。运行 `python -m scripts.verify_company_coverage 600519 002594 300750`，结果为 `600519` 命中 `cache:normalized`、28 行、1998-2025、核心字段无缺失；`002594` 命中 `akshare:sina`、24 行、2002-2025、核心字段无缺失；`300750` 命中 `akshare:eastmoney:yearly`、12 行、2014-2025、核心字段无缺失。随后单独重试 `002594` 的东财年度三表适配器成功返回 24 行、2002-2025、核心字段无缺失，说明首次 fallback 更像上游瞬时延迟/失败，不是字段映射缺口。
- Decisions: 保留 `data/cache/` 下验证生成的本地标准化缓存作为本机 demo 加速；缓存目录已在 `.gitignore` 中排除。验证脚本只调用现有公开数据层，不新增第二套数据口径。
- Next: 做作品展示包装：给 README 增加小截图/GIF，或整理 Streamlit Community Cloud 部署检查清单；不要改指标公式和风险阈值。

## 2026-06-25 14:52 - Streamlit UI Agent

- Goal: 按 Task 5 给页面补充数据来源状态提示，同时保持页面只做展示、不引入 AKShare 业务逻辑。
- Changed: 新增 `src/ui/source_status.py` 和 `tests/test_source_status.py`；更新 `pages/01_company_analysis.py`、`pages/03_risk_rules.py`、`pages/04_export_center.py`，统一展示 live/cache/sample 来源与 fallback warning；更新 `docs/PAGE_REGISTRY.md`、`docs/plans/001-real-akshare-data-mvp-plan.md`、`docs/NEXT_STEPS.md`。
- Verified: TDD RED 阶段先确认 `tests/test_source_status.py` 因缺少 `src.ui.source_status` 失败；实现后 `pytest -q tests/test_source_status.py` 通过；最终 `pytest -q` 通过，10 passed；`python -m compileall app.py pages src tests` 通过；Streamlit 本地服务 `http://localhost:8501` 返回 HTTP 200。
- Decisions: 使用 `st.caption` 展示轻量数据来源说明，继续使用 `st.info` 展示 fallback warning；页面只调用 `fetch_company_financials()` 和 UI helper，不直接调用 AKShare。
- Next: 执行 Task 6，验证 `600519`、`002594`、`300750` 的 live/cache/sample 状态，记录上游失败情况，并更新 `README.md` 的真实数据说明。

## 2026-06-25 14:35 - Data Source Agent

- Goal: 按 Spec/Planning/TDD/Source-Driven 流程实现真实 AKShare 数据接入 MVP 的第一条切片，并留下后续 AI 可接手的任务拆分。
- Changed: 新增 `docs/specs/001-real-akshare-data-mvp.md`、`docs/plans/001-real-akshare-data-mvp-plan.md`、`docs/NEXT_STEPS.md`；新增 `tests/test_akshare_client.py`；更新 `src/data/akshare_client.py`，加入 A 股代码规范化、东财年度三大表映射、新浪三大表映射、标准化缓存、live/cache/sample fallback；更新 `docs/DATA_DICTIONARY.md`、`docs/DECISIONS.md`、`docs/PROJECT_STRUCTURE.md`、`README.md`。
- Verified: TDD RED 阶段先确认 `tests/test_akshare_client.py` 因缺少新函数失败；实现后 `pytest -q tests/test_akshare_client.py` 通过，5 passed；完整 `pytest -q` 通过，7 passed；`python -m compileall app.py pages src tests` 通过；真实 smoke check 中 `fetch_company_financials("600519")` 当前可返回标准化公开数据，先命中 `akshare:sina` 并写入 `data/cache/normalized_financials_600519.csv`，后续检查命中 `cache:normalized`；Streamlit 本地服务返回 HTTP 200。
- Decisions: fallback order 定为 normalized cache -> Eastmoney live -> Sina live -> labeled sample data；`net_profit` 优先使用归母净利润，无归母字段时使用净利润；当前 MVP 暂不单独处理金融行业 schema。
- Next: 执行 `docs/plans/001-real-akshare-data-mvp-plan.md` 的 Task 5，在页面上小幅展示数据来源状态，并将 `docs/PAGE_REGISTRY.md` 中相关页面从 Skeleton 更新到 MVP。

## 2026-06-25 14:00 - Project Architect

- Goal: 创建 A 股经营风险分析台的项目骨架和 AI 协作规则，防止后续代码散乱。
- Changed: 新建 Streamlit 项目目录、模块分层、文档治理文件、页面登记簿、基础配置。
- Verified: 已创建本地 `.venv` 并安装 `requirements.txt`；`python -m compileall app.py pages src tests` 通过；`pytest -q` 通过，2 passed；核心 smoke check 通过，样例数据 7 年、触发 5 条风险信号、Excel 字节流可生成；Streamlit 已在 `http://localhost:8501` 启动并返回 HTTP 200。
- Decisions: 页面只放展示，业务逻辑进入 `src/`；每次 AI 修改后更新任务日志；页面变化更新页面登记簿。
- Next: 接入 AKShare 的真实字段映射，并把样例数据替换为真实公司数据流。
