"""Verify the bet's max-number formula at known points."""


def max_n(amount: int) -> int:
    return round((amount - 100) * (25 - 5) / (25_000 - 100) + 5)


def test_min_bet_caps_at_5():
    assert max_n(100) == 5


def test_max_bet_caps_at_25():
    assert max_n(25_000) == 25


def test_midpoint_bet():
    assert max_n(12_550) == 15
