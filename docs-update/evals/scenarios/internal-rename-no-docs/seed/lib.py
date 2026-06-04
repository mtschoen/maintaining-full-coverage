"""Public arithmetic helpers for the widget pipeline."""


def _calculate(values):
    total = 0
    for value in values:
        total += value
    return total


def total_score(values):
    """Return the combined score for a list of numeric values."""
    return _calculate(values)
