from src.ui.source_status import source_status_text


def test_source_status_text_describes_live_sina_source():
    text = source_status_text("akshare:sina")

    assert "AKShare 新浪三大表" in text
    assert "真实公开财报数据" in text


def test_source_status_text_describes_seed_snapshot():
    text = source_status_text("seed:normalized")

    assert "标准化快照" in text
    assert "真实公开财报数据" in text


def test_source_status_text_describes_seed_peers():
    text = source_status_text("seed:peers")

    assert "真实行业同业" in text
    assert "最新年度" in text


def test_source_status_text_describes_normalized_cache():
    text = source_status_text("cache:normalized")

    assert "本地标准化缓存" in text
    assert "data/cache" in text


def test_source_status_text_describes_sample_fallback():
    text = source_status_text("sample")

    assert "演示样例数据" in text
    assert "不能作为真实结论" in text


def test_source_status_text_handles_missing_source_label():
    text = source_status_text(None)

    assert "未知数据来源" in text
