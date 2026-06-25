# Deployment Checklist — Streamlit Community Cloud

本文件是把本项目部署到 [Streamlit Community Cloud](https://streamlit.io/cloud) 的逐项检查清单。
目标：让招聘方点开一个公开 URL 就能体验，而不需要本地装环境。

本清单只覆盖部署，不改任何财务指标公式、风险规则阈值或 UI 设计。

## 0. 部署前提速览

| 项目 | 当前值 | 说明 |
|---|---|---|
| 入口文件 | `app.py` | Streamlit Cloud 的 "Main file path" 填这个 |
| 依赖文件 | `requirements.txt` | 已固定最小可运行依赖，含 `akshare` |
| Python 版本 | `requires-python >=3.10`（见 `pyproject.toml`） | Cloud 上在 Advanced settings 里选 3.10/3.11 |
| 主题/服务器配置 | `.streamlit/config.toml` | 已提交，含主题和 `headless=true` |
| 机密文件 | `.streamlit/secrets.toml` | **不提交**，已在 `.gitignore` 排除；当前 MVP 无需任何密钥 |
| 本地缓存 | `data/cache/*` | **不进 Git**，云端首跑会走 live AKShare 或 sample fallback |

## 1. 仓库准备

- [ ] 代码已 push 到一个 Streamlit Cloud 能访问的 Git 仓库（GitHub 公共或授权私有）。
- [ ] 仓库根目录就是本项目根目录（`app.py` 与 `requirements.txt` 同级）。
- [ ] `requirements.txt` 在根目录，且包含运行所需的全部依赖（`streamlit`、`pandas`、`numpy`、`plotly`、`akshare`、`openpyxl`）。
  - 说明：`pytest` 只用于本地测试，云端运行 app 时不会用到，但保留无害。
- [ ] 确认没有把以下内容提交进仓库：
  - `.venv/`（虚拟环境）
  - `.streamlit/secrets.toml`、`.env*`（机密）
  - `data/cache/*`、`data/raw/*`、`data/processed/*`、`outputs/*`（本地产物）
  - 任何 Wind/CSMAR/Choice 付费数据库原始数据
  - 以上均已在 `.gitignore` 中处理，push 前用 `git status` 复核一次即可。

## 2. 入口与依赖核对

- [ ] 入口文件确认为 `app.py`，并且本地 `streamlit run app.py` 能正常打开多页面（`pages/01`~`04`）。
- [ ] `requirements.txt` 的版本下限与本地实测一致（本地用 AKShare 1.18.64 验证过三家公司覆盖）。
- [ ] 本地两条检查命令通过：

  ```bash
  .venv\Scripts\python.exe -m pytest -q
  .venv\Scripts\python.exe -m compileall app.py pages src scripts tests
  ```

## 3. Streamlit Cloud 创建 App

- [ ] 登录 https://share.streamlit.io ，选择 "Create app" / "Deploy a public app from GitHub"。
- [ ] Repository：选择本仓库。
- [ ] Branch：选择要部署的分支（一般是 `main`）。
- [ ] Main file path：填 `app.py`。
- [ ] Advanced settings → Python version：选择 `3.10` 或 `3.11`（与 `requires-python >=3.10` 一致）。
- [ ] Secrets：当前 MVP **无需填任何密钥**。只有未来接入 LLM 润色（`src/ai/`）时，才在此处以 `KEY = "value"` 形式填入，对应云端的 `st.secrets`，仍然不写进仓库。
- [ ] 点击 Deploy，等待首次构建完成。

## 4. 首次部署后的数据行为（重要）

云端是干净环境，没有本地缓存，所以数据来源链路是：

1. `data/cache/normalized_financials_<symbol>.csv`：**云端首跑通常没有**（缓存不进 Git）。
2. AKShare 东财年度三大表（live）。
3. AKShare 新浪三大表（live）。
4. 明确标注的本地样例数据（sample fallback）。

- [ ] 打开公开 URL，输入 `600519`，确认页面顶部数据来源提示显示 `live` 或 `sample`，并能正常出图。
- [ ] 理解并接受：Streamlit Cloud 出网访问 AKShare 上游公开站点，可能比本地慢或偶发失败；此时页面会退回带标注的 sample 数据而不是崩溃，demo 始终可点。
- [ ] 如需让首屏更稳，可在 README/页面里引导招聘方优先试已验证的 `600519` / `002594` / `300750`。

## 5. 部署后冒烟检查

- [ ] 四个页面都能打开：公司分析、同业比较、风险预警、导出中心。
- [ ] 公司分析页：核心指标卡、趋势图、规则摘要、数据来源提示都正常。
- [ ] 风险预警页：能看到透明规则、风险等级和触发证据。
- [ ] 导出中心：能下载 Excel（下载用内存对象，不依赖本地 `outputs/`）。
- [ ] 数据来源提示文案与实际来源（live/cache/sample）一致。

## 6. 维护与更新

- [ ] 后续 push 到部署分支后，Streamlit Cloud 会自动重建；改依赖时同步更新 `requirements.txt`。
- [ ] 若云端 AKShare 频繁失败，先确认是上游瞬时问题还是字段映射变化，再决定是否调整 `src/data/akshare_client.py`（属于数据层任务，不在本部署清单范围）。
- [ ] 任何部署相关改动后，更新 `docs/TASK_LOG.md`。

## 不在本清单范围

- 不改财务指标公式（`src/metrics/`）。
- 不改风险规则阈值（`src/risk/`、`docs/RISK_RULES_SPEC.md`）。
- 不重构 UI。
- 不在部署阶段新增 PDF、LLM、真实行业同业匹配功能。
