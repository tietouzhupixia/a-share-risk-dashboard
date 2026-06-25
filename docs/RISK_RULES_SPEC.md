# Risk Rules Specification

第一版采用透明规则，不采用黑箱评分。每条规则都必须能被用户看到触发依据。

## Risk Levels

| Level | Meaning |
|---|---|
| High | 明显异常，需要优先解释 |
| Medium | 存在压力信号，需要继续观察 |
| Low | 轻微提示或单年波动 |

## Current Rules

| Rule ID | Rule Name | Trigger | Level |
|---|---|---|---|
| `AR_GROWTH_GT_REVENUE_2Y` | 应收账款增速连续高于收入增速 | 最近两年 `accounts_receivable_growth > revenue_growth` | High |
| `OCF_BELOW_PROFIT_2Y` | 经营现金流连续低于净利润 | 最近两年 `operating_cash_flow < net_profit` | High |
| `HIGH_LEVERAGE` | 杠杆偏高 | 最新 `asset_liability_ratio >= 0.70` | Medium |
| `GROSS_MARGIN_DROP` | 毛利率明显下降 | 最近一年毛利率较前一年下降超过 5 个百分点 | Medium |
| `INVENTORY_GROWTH_GT_REVENUE` | 存货增长快于收入 | 最新 `inventory_growth > revenue_growth` 且收入增长为正 | Medium |
| `SHORT_DEBT_JUMP` | 短期借款快速上升 | 最新 `short_term_borrowing_growth >= 0.30` | Medium |
| `GROWTH_WITH_COLLECTION_PRESSURE` | 收入增长但回款效率下降 | 最新收入增长为正且应收周转天数上升 | Medium |

## Rule Output Contract

Every rule returns:

- `rule_id`
- `name`
- `level`
- `reason`
- `evidence`
- `interpretation`

## Interpretation Guardrail

风险提示不是投资建议。页面和导出报告必须使用“可能表明”“需要关注”“建议进一步核查”等表述。

