"""Shared Streamlit layout helpers."""

import streamlit as st

from src.config import APP_TITLE, APP_TITLE_CN


def configure_page(page_title: str) -> None:
    """Apply a consistent Streamlit page configuration."""

    st.set_page_config(
        page_title=f"{page_title} | {APP_TITLE}",
        layout="wide",
    )


def render_app_header(subtitle: str | None = None) -> None:
    """Render the app title."""

    st.title(APP_TITLE_CN)
    st.caption(APP_TITLE)
    if subtitle:
        st.write(subtitle)


def format_percent(value: float) -> str:
    if value is None or value != value:
        return "N/A"
    return f"{value:.1%}"


def format_number(value: float) -> str:
    if value is None or value != value:
        return "N/A"
    abs_value = abs(value)
    if abs_value >= 100_000_000:
        return f"{value / 100_000_000:.1f}亿"
    if abs_value >= 10_000:
        return f"{value / 10_000:.1f}万"
    return f"{value:,.0f}"
