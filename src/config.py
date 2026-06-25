"""Project-level configuration."""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
CACHE_DIR = DATA_DIR / "cache"
OUTPUT_DIR = BASE_DIR / "outputs"

APP_TITLE = "A-Share Financial Risk Intelligence Dashboard"
APP_TITLE_CN = "AI上市公司经营风险分析台"

DEFAULT_SYMBOL = "002594"
DEFAULT_COMPANIES = {
    "002594": "比亚迪",
    "300750": "宁德时代",
    "600519": "贵州茅台",
    "000333": "美的集团",
}

YEAR_WINDOW = 8

