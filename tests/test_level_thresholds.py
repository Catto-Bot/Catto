from events.events import LEVEL_THRESHOLDS


def test_thresholds_strictly_increasing():
    counts = [t[0] for t in LEVEL_THRESHOLDS]
    assert counts == sorted(counts)
    assert len(counts) == len(set(counts))  # no duplicates


def test_levels_strictly_increasing():
    levels = [t[1] for t in LEVEL_THRESHOLDS]
    assert levels == sorted(levels)
    assert len(levels) == len(set(levels))
