"""Streamlit app entry point."""

import streamlit as st

from src.config import DEFAULT_COMPANIES
from src.ui.layout import configure_page, render_app_header


def render() -> None:
    configure_page("首页")
    render_app_header("输入 A 股公司代码，查看财务趋势、风险预警、同业比较和可导出的分析结果。")

    st.subheader("当前产品视图")
    st.write("这个项目骨架已经把页面、数据、指标、风险规则、摘要和导出拆开，后续开发请遵守 `AGENTS.md`。")

    st.subheader("样例公司")
    for symbol, name in DEFAULT_COMPANIES.items():
        st.code(f"{symbol} - {name}", language="text")

    st.subheader("页面导航")
    st.page_link("pages/01_company_analysis.py", label="公司分析")
    st.page_link("pages/02_peer_comparison.py", label="同业比较")
    st.page_link("pages/03_risk_rules.py", label="风险预警")
    st.page_link("pages/04_export_center.py", label="导出中心")


if __name__ == "__main__":
    render()

