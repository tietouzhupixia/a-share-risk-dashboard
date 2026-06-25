"""PDF export utilities for one-page company risk reports."""

from __future__ import annotations

from io import BytesIO
from typing import Any
from xml.sax.saxutils import escape

import pandas as pd
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from src.ai.summary import EvidenceLinkedSummary
from src.risk.rules import RiskSignal


PDF_FONT = "STSong-Light"
PDF_TITLE = "A股上市公司经营风险一页报告"
DISCLAIMER = "本报告基于公开年报口径和透明规则自动生成，不构成投资建议。"


def build_company_pdf_report(
    *,
    metrics_df: pd.DataFrame,
    signals: list[RiskSignal],
    summary: EvidenceLinkedSummary,
    data_source: str,
) -> bytes:
    """Return a compact PDF report as bytes.

    The report reuses precomputed metrics, risk signals, and evidence-linked
    summaries. It does not calculate financial ratios or risk rules.
    """

    _register_cjk_font()
    latest = metrics_df.sort_values("year").iloc[-1]

    output = BytesIO()
    doc = SimpleDocTemplate(
        output,
        pagesize=A4,
        leftMargin=14 * mm,
        rightMargin=14 * mm,
        topMargin=12 * mm,
        bottomMargin=12 * mm,
        title=PDF_TITLE,
    )
    styles = _styles()

    story = [
        Paragraph(PDF_TITLE, styles["Title"]),
        Paragraph(
            (
                f"{_text(latest['company_name'])} ({_text(latest['symbol'])}) | "
                f"{int(latest['year'])} | 数据来源: {_text(data_source)}"
            ),
            styles["Meta"],
        ),
        Spacer(1, 5),
        Paragraph("摘要", styles["Section"]),
        Paragraph(_text(summary.narrative), styles["Body"]),
        Spacer(1, 5),
        Paragraph("核心指标", styles["Section"]),
        _metrics_table(latest),
        Spacer(1, 5),
        Paragraph("风险信号", styles["Section"]),
        _risk_table(signals),
        Spacer(1, 5),
        Paragraph("摘要证据表", styles["Section"]),
        _evidence_table(summary.evidence),
        Spacer(1, 5),
        Paragraph(DISCLAIMER, styles["Disclaimer"]),
    ]

    doc.build(story)
    output.seek(0)
    return output.read()


def _register_cjk_font() -> None:
    if PDF_FONT not in pdfmetrics.getRegisteredFontNames():
        pdfmetrics.registerFont(UnicodeCIDFont(PDF_FONT))


def _styles() -> dict[str, ParagraphStyle]:
    base = getSampleStyleSheet()
    return {
        "Title": ParagraphStyle(
            "Title",
            parent=base["Title"],
            fontName=PDF_FONT,
            fontSize=15,
            leading=18,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#1f2937"),
            spaceAfter=4,
        ),
        "Meta": ParagraphStyle(
            "Meta",
            parent=base["Normal"],
            fontName=PDF_FONT,
            fontSize=8,
            leading=10,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#4b5563"),
        ),
        "Section": ParagraphStyle(
            "Section",
            parent=base["Heading2"],
            fontName=PDF_FONT,
            fontSize=10,
            leading=12,
            alignment=TA_LEFT,
            textColor=colors.HexColor("#111827"),
            spaceBefore=2,
            spaceAfter=3,
        ),
        "Body": ParagraphStyle(
            "Body",
            parent=base["BodyText"],
            fontName=PDF_FONT,
            fontSize=8,
            leading=11,
            alignment=TA_LEFT,
            textColor=colors.HexColor("#111827"),
        ),
        "TableCell": ParagraphStyle(
            "TableCell",
            parent=base["BodyText"],
            fontName=PDF_FONT,
            fontSize=7,
            leading=9,
            alignment=TA_LEFT,
        ),
        "TableHeader": ParagraphStyle(
            "TableHeader",
            parent=base["BodyText"],
            fontName=PDF_FONT,
            fontSize=7,
            leading=9,
            alignment=TA_CENTER,
            textColor=colors.white,
        ),
        "Disclaimer": ParagraphStyle(
            "Disclaimer",
            parent=base["BodyText"],
            fontName=PDF_FONT,
            fontSize=7,
            leading=9,
            alignment=TA_LEFT,
            textColor=colors.HexColor("#6b7280"),
        ),
    }


def _metrics_table(latest: pd.Series) -> Table:
    rows = [
        ["指标", "数值", "指标", "数值"],
        ["营业收入增长率", _pct(latest["revenue_growth"]), "净利润增长率", _pct(latest["net_profit_growth"])],
        ["ROA", _pct(latest["roa"]), "资产负债率", _pct(latest["asset_liability_ratio"])],
        ["经营现金流/净利润", _number(latest["ocf_to_profit"]), "应收账款/营收", _pct(latest["ar_to_revenue"])],
        ["存货/营收", _pct(latest["inventory_to_revenue"]), "应收周转天数", f"{_number(latest['ar_turnover_days'])} 天"],
    ]
    return _table(rows, col_widths=[35 * mm, 34 * mm, 35 * mm, 34 * mm])


def _risk_table(signals: list[RiskSignal]) -> Table:
    rows = [["等级", "风险信号", "触发原因"]]
    if not signals:
        rows.append(["-", "未触发明显风险规则", "当前透明规则未发现需要优先解释的异常。"])
    else:
        for signal in signals[:3]:
            rows.append([signal.level, signal.name, signal.reason])
    return _table(rows, col_widths=[17 * mm, 45 * mm, 76 * mm])


def _evidence_table(evidence: pd.DataFrame) -> Table:
    rows = [["编号", "结论", "指标/规则", "数值"]]
    if evidence.empty:
        rows.append(["-", "暂无证据", "-", "-"])
    else:
        for row in evidence.head(6).to_dict(orient="records"):
            rows.append(
                [
                    row.get("id", ""),
                    row.get("conclusion", ""),
                    row.get("metric", ""),
                    row.get("value", ""),
                ]
            )
    return _table(rows, col_widths=[12 * mm, 34 * mm, 55 * mm, 37 * mm])


def _table(rows: list[list[Any]], col_widths: list[float]) -> Table:
    styles = _styles()
    formatted_rows = [
        [
            Paragraph(_text(cell), styles["TableHeader" if row_index == 0 else "TableCell"])
            for cell in row
        ]
        for row_index, row in enumerate(rows)
    ]
    table = Table(formatted_rows, colWidths=col_widths, repeatRows=1)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1f2937")),
                ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#d1d5db")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ]
        )
    )
    return table


def _text(value: Any) -> str:
    if value is None or pd.isna(value):
        return "N/A"
    return escape(str(value))


def _pct(value: Any) -> str:
    if value is None or pd.isna(value):
        return "N/A"
    return f"{float(value):.1%}"


def _number(value: Any) -> str:
    if value is None or pd.isna(value):
        return "N/A"
    return f"{float(value):.2f}"
