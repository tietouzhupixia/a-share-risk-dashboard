"""Plotly chart builders."""

import pandas as pd
import plotly.express as px


def line_chart(df: pd.DataFrame, y_fields: list[str], title: str):
    """Create a tidy multi-series line chart."""

    chart_df = df.melt(id_vars=["year"], value_vars=y_fields, var_name="metric", value_name="value")
    return px.line(chart_df, x="year", y="value", color="metric", markers=True, title=title)


def peer_bar_chart(df: pd.DataFrame, metric: str, title: str):
    """Create a peer-comparison bar chart."""

    sorted_df = df.sort_values(metric, ascending=False)
    return px.bar(sorted_df, x="company_name", y=metric, color="company_name", title=title)

