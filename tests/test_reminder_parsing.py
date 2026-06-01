from cogs.reminders import parse_duration


def test_seconds():
    assert parse_duration("30s") == 30


def test_minutes():
    assert parse_duration("5m") == 300


def test_hours():
    assert parse_duration("2h") == 7200


def test_days():
    assert parse_duration("1d") == 86_400


def test_case_insensitive():
    assert parse_duration("10M") == 600


def test_whitespace_tolerated():
    assert parse_duration("  5 m ") == 300


def test_invalid_returns_none():
    assert parse_duration("five") is None
    assert parse_duration("10x") is None
    assert parse_duration("") is None
