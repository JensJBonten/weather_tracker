import pandas as pd

from src.reporting import format_duration


def test_format_duration_formats_timedelta_as_hh_mm_ss():
    """Tester om timedelta blir formatert riktig, altså HH:MM:SS."""

    value = pd.Timedelta(hours=4, minutes=8)
    formatted_duration = format_duration(value)
    assert formatted_duration == "04:08:00"


def test_format_duration_returns_na_for_missing_value():
    """Sjekker at manglende verdi blir vist som N/A."""
    formatted_duration = format_duration(pd.NaT)

    assert formatted_duration == "N/A"
