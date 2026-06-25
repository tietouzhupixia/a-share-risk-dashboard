# Data Dictionary

本文件记录标准字段、口径和数据来源。外部数据字段进入指标层前，应先映射为这里的标准字段。

## Standard Annual Financial Columns

| Field | Meaning | Unit | Notes |
|---|---|---|---|
| `symbol` | 股票代码 | text | 6 位 A 股代码 |
| `company_name` | 公司名称 | text | 中文简称或全称 |
| `year` | 财报年度 | integer | 年报口径优先 |
| `revenue` | 营业收入 | CNY | 年度营业收入 |
| `net_profit` | 净利润 | CNY | 优先归母净利润，需在后续版本确认接口口径 |
| `operating_cash_flow` | 经营活动现金流量净额 | CNY | 年度现金流量表 |
| `accounts_receivable` | 应收账款 | CNY | 期末余额 |
| `inventory` | 存货 | CNY | 期末余额 |
| `total_assets` | 总资产 | CNY | 期末余额 |
| `total_liabilities` | 总负债 | CNY | 期末余额 |
| `gross_profit` | 毛利 | CNY | 可由收入和成本计算，或由接口提供 |
| `short_term_borrowing` | 短期借款 | CNY | 期末余额 |

## AKShare Source Mapping

The data layer currently supports two public AKShare paths.

| Source Label | AKShare Function | Role | Notes |
|---|---|---|---|
| `akshare:eastmoney:yearly` | `stock_balance_sheet_by_yearly_em` | 资产负债表 | Primary live source when upstream succeeds |
| `akshare:eastmoney:yearly` | `stock_profit_sheet_by_yearly_em` | 利润表 | Primary live source when upstream succeeds |
| `akshare:eastmoney:yearly` | `stock_cash_flow_sheet_by_yearly_em` | 现金流量表 | Primary live source when upstream succeeds |
| `akshare:sina` | `stock_financial_report_sina(..., "资产负债表")` | 资产负债表 fallback | Uses Sina three-statement endpoint |
| `akshare:sina` | `stock_financial_report_sina(..., "利润表")` | 利润表 fallback | Uses Sina three-statement endpoint |
| `akshare:sina` | `stock_financial_report_sina(..., "现金流量表")` | 现金流量表 fallback | Uses Sina three-statement endpoint |
| `cache:normalized` | Local CSV under `data/cache/` | Normalized cache | Used before live calls when present |
| `sample` | `src/data/sample_data.py` | Demo fallback | Must be labeled as non-live sample data |

## Provider Field Mapping

| Standard Field | Eastmoney Candidates | Sina Candidates |
|---|---|---|
| `company_name` | `SECURITY_NAME_ABBR` | Defaults to configured company name or symbol |
| `year` | `REPORT_DATE` year, annual reports only | `报告日` year, `1231` annual reports only |
| `revenue` | `OPERATE_INCOME`, `TOTAL_OPERATE_INCOME` | `营业收入`, `营业总收入` |
| `net_profit` | `PARENT_NETPROFIT`, `NETPROFIT` | `归属于母公司所有者的净利润`, `净利润` |
| `operating_cash_flow` | `NETCASH_OPERATE`, `NETCASH_OPERATENOTE` | `经营活动产生的现金流量净额`, `经营活动现金流量净额` |
| `accounts_receivable` | `ACCOUNTS_RECE`, `ACCOUNTS_RECEIVABLE`, `ACCOUNT_RECE`, `NOTE_ACCOUNTS_RECE` | `应收账款`, `应收票据及应收账款` |
| `inventory` | `INVENTORY` | `存货` |
| `total_assets` | `TOTAL_ASSETS` | `资产总计` |
| `total_liabilities` | `TOTAL_LIABILITIES` | `负债合计` |
| `gross_profit` | `revenue - OPERATE_COST` | `revenue - 营业成本` |
| `short_term_borrowing` | `SHORT_LOAN`, `SHORTTERM_LOAN`, `SHORT_BORROW` | `短期借款` |

## Derived Metrics

| Metric | Formula | Notes |
|---|---|---|
| `revenue_growth` | `revenue.pct_change()` | 同比增速 |
| `net_profit_growth` | `net_profit.pct_change()` | 同比增速 |
| `roa` | `net_profit / total_assets` | 简化 ROA，后续可改平均资产 |
| `asset_liability_ratio` | `total_liabilities / total_assets` | 资产负债率 |
| `ocf_to_profit` | `operating_cash_flow / net_profit` | 现金流质量 |
| `ar_to_revenue` | `accounts_receivable / revenue` | 应收账款占收入比例 |
| `inventory_to_revenue` | `inventory / revenue` | 存货占收入比例 |
| `ar_turnover_days` | `accounts_receivable / revenue * 365` | 简化应收周转天数 |
| `gross_margin` | `gross_profit / revenue` | 毛利率 |
| `net_margin` | `net_profit / revenue` | 净利率 |

## Data Source Policy

- 第一数据源：AKShare 公开接口，优先东财年度三大表，失败后尝试新浪三大表。
- 本地标准化缓存：`data/cache/normalized_financials_<symbol>.csv`。
- 无网络或接口异常时：使用 `src/data/sample_data.py` 演示数据，并在页面提示。
- 不允许公开 Wind、CSMAR、Choice 等付费数据库原始数据。

## Known Limitations

- 金融行业公司可能需要单独口径，当前 MVP 优先非金融公司。
- AKShare 上游接口可能出现 SSL、限流、字段变动等问题，因此必须保留 fallback。
- 当前 `net_profit` 优先使用归母净利润；无归母字段时使用净利润。
