"""Curated A-share company universe.

A small, hand-picked set of large-cap, non-financial A-share companies used to
build the committed seed dataset and to group real industry peers. Banks,
insurers, and brokers are intentionally excluded because their three-statement
schema differs from the industrial template the metrics layer expects.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class UniverseCompany:
    """One company in the curated universe."""

    code: str
    name: str
    industry: str


_UNIVERSE: tuple[UniverseCompany, ...] = (
    # 食品饮料
    UniverseCompany("600519", "贵州茅台", "食品饮料"),
    UniverseCompany("000858", "五粮液", "食品饮料"),
    UniverseCompany("600887", "伊利股份", "食品饮料"),
    UniverseCompany("603288", "海天味业", "食品饮料"),
    UniverseCompany("000895", "双汇发展", "食品饮料"),
    # 汽车
    UniverseCompany("002594", "比亚迪", "汽车"),
    UniverseCompany("600104", "上汽集团", "汽车"),
    UniverseCompany("601238", "广汽集团", "汽车"),
    # 电力设备（含锂电/光伏）
    UniverseCompany("300750", "宁德时代", "电力设备"),
    UniverseCompany("600438", "通威股份", "电力设备"),
    UniverseCompany("002074", "国轩高科", "电力设备"),
    # 家用电器
    UniverseCompany("000333", "美的集团", "家用电器"),
    UniverseCompany("000651", "格力电器", "家用电器"),
    UniverseCompany("600690", "海尔智家", "家用电器"),
    # 医药生物
    UniverseCompany("600276", "恒瑞医药", "医药生物"),
    UniverseCompany("300760", "迈瑞医疗", "医药生物"),
    # 电子
    UniverseCompany("002475", "立讯精密", "电子"),
    UniverseCompany("002415", "海康威视", "电子"),
    UniverseCompany("000725", "京东方A", "电子"),
    UniverseCompany("603501", "韦尔股份", "电子"),
    # 机械设备 / 建筑材料
    UniverseCompany("600031", "三一重工", "机械设备"),
    UniverseCompany("600585", "海螺水泥", "建筑材料"),
    # 钢铁 / 基础化工
    UniverseCompany("600019", "宝钢股份", "钢铁"),
    UniverseCompany("600309", "万华化学", "基础化工"),
    # 房地产
    UniverseCompany("000002", "万科A", "房地产"),
    UniverseCompany("600048", "保利发展", "房地产"),
    # 农林牧渔
    UniverseCompany("300498", "温氏股份", "农林牧渔"),
    # 交通运输
    UniverseCompany("600009", "上海机场", "交通运输"),
)


def get_universe() -> tuple[UniverseCompany, ...]:
    """Return the full curated universe."""

    return _UNIVERSE


def universe_codes() -> list[str]:
    """Return all six-digit codes in the universe."""

    return [company.code for company in _UNIVERSE]


def get_company(code: str) -> UniverseCompany | None:
    """Return the company with this exact six-digit code, or None."""

    for company in _UNIVERSE:
        if company.code == code:
            return company
    return None


def industries() -> list[str]:
    """Return the sorted, de-duplicated list of industries in the universe."""

    return sorted({company.industry for company in _UNIVERSE})


def companies_in_industry(industry: str) -> list[UniverseCompany]:
    """Return all universe companies in the given industry."""

    return [company for company in _UNIVERSE if company.industry == industry]
