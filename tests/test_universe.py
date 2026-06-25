"""Tests for the curated A-share company universe registry."""

from src.config import DEFAULT_COMPANIES
from src.data.universe import (
    UniverseCompany,
    companies_in_industry,
    get_company,
    get_universe,
    industries,
    universe_codes,
)

FINANCIAL_SECTORS = {"银行", "保险", "证券", "非银金融"}


def test_universe_is_non_trivial_and_well_formed():
    universe = get_universe()
    assert len(universe) >= 24
    for company in universe:
        assert isinstance(company, UniverseCompany)
        assert company.code.isdigit() and len(company.code) == 6
        assert company.name.strip()
        assert company.industry.strip()


def test_universe_codes_are_unique():
    codes = universe_codes()
    assert len(codes) == len(set(codes))


def test_universe_includes_existing_default_companies():
    codes = set(universe_codes())
    for code in DEFAULT_COMPANIES:
        assert code in codes, f"default company {code} should be in the universe"


def test_universe_excludes_financial_sectors():
    # Banks/insurers/brokers use a different statement schema; keep them out for now.
    for company in get_universe():
        assert company.industry not in FINANCIAL_SECTORS


def test_get_company_lookup():
    assert get_company("600519").name == "贵州茅台"
    assert get_company("SH600519") is None or get_company("SH600519").code == "600519"
    assert get_company("999999") is None


def test_industries_and_membership():
    inds = industries()
    assert inds == sorted(set(inds))  # sorted, de-duplicated
    # at least one industry has 2+ members so peer comparison is meaningful
    assert any(len(companies_in_industry(ind)) >= 2 for ind in inds)
    for company in companies_in_industry(inds[0]):
        assert company.industry == inds[0]
