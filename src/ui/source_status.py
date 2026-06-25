"""Data source status display helpers."""

import streamlit as st


SOURCE_LABELS = {
    "seed:normalized": "已提交的标准化快照 data/seed",
    "seed:peers": "真实行业同业（基于已提交快照）",
    "akshare:eastmoney:yearly": "AKShare 东财年度三大表",
    "akshare:sina": "AKShare 新浪三大表",
    "cache:normalized": "本地标准化缓存 data/cache",
    "sample": "演示样例数据",
}


def source_status_text(source: str | None) -> str:
    """Return a reader-facing explanation for a data source label."""

    normalized_source = source or ""
    label = SOURCE_LABELS.get(normalized_source, normalized_source or "未知数据来源")
    if normalized_source == "sample":
        return f"数据来源：{label}。这不是实时公开财报数据，不能作为真实结论。"
    if normalized_source == "seed:normalized":
        return f"数据来源：{label}。这是随仓库提交的真实公开财报数据快照，云端无需联网即可展示。"
    if normalized_source == "seed:peers":
        return f"数据来源：{label}，取各同业公司最新年度指标，使用真实公开财报数据。"
    if normalized_source == "cache:normalized":
        return f"数据来源：{label}。缓存来自先前成功获取并标准化的公开财报数据。"
    if normalized_source.startswith("akshare:"):
        return f"数据来源：{label}。当前页面使用真实公开财报数据。"
    return f"数据来源：{label}。"


def render_data_source_status(source: str | None, warning: str | None = None) -> None:
    """Render a compact, consistent Streamlit data-source status block."""

    if warning:
        st.info(warning)
    st.caption(source_status_text(source))
