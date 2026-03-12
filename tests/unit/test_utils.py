"""Unit tests for utility modules."""

from utils.formatting import (
    format_water_amount, format_percentage, format_header, truncate
)
from utils.validation import (
    validate_plot_name, validate_amount, validate_irrigation_params
)
from utils.search import (
    find_plots_by_kind, find_changes_by_memo, count_changes_per_plot
)
from utils.aggregation import (
    total_water_moved, average_change_amount, max_water_level, min_water_level
)


def test_format_water_amount():
    """format_water_amount handles normal and large values."""
    assert format_water_amount(500) == "500 liters"
    assert "k" in format_water_amount(1500)


def test_format_percentage():
    """format_percentage computes correct percentages."""
    assert format_percentage(50, 200) == "25.0%"
    assert format_percentage(0, 0) == "0.0%"


def test_format_header():
    """format_header creates a centered header with separators."""
    h = format_header("Test")
    assert "Test" in h
    assert "-" in h


def test_truncate():
    """truncate shortens long text with ellipsis."""
    assert truncate("short", 40) == "short"
    assert truncate("a" * 50, 10) == "aaaaaaa..."


def test_validate_plot_name():
    """validate_plot_name rejects empty and invalid names."""
    ok, _ = validate_plot_name("")
    assert not ok
    ok, _ = validate_plot_name("roses")
    assert ok
    ok, _ = validate_plot_name("a" * 101)
    assert not ok


def test_validate_amount():
    """validate_amount rejects non-positive values."""
    ok, _ = validate_amount(100)
    assert ok
    ok, _ = validate_amount(0)
    assert not ok
    ok, _ = validate_amount(-5)
    assert not ok


def test_validate_irrigation_params():
    """validate_irrigation_params rejects same source and destination."""
    ok, _ = validate_irrigation_params("roses", "roses", 100)
    assert not ok
    ok, _ = validate_irrigation_params("roses", "herbs", 100)
    assert ok


def test_find_plots_by_kind(funded_nursery):
    """find_plots_by_kind filters correctly."""
    beds = find_plots_by_kind(funded_nursery, "bed")
    assert len(beds) == 2
    reservoirs = find_plots_by_kind(funded_nursery, "reservoir")
    assert len(reservoirs) == 1


def test_find_changes_by_memo(funded_nursery):
    """find_changes_by_memo searches case-insensitively."""
    results = find_changes_by_memo(funded_nursery, "initial")
    assert len(results) == 2


def test_count_changes_per_plot(funded_nursery):
    """count_changes_per_plot counts correctly."""
    counts = count_changes_per_plot(funded_nursery)
    assert counts["reservoir"] == 2
    assert counts["roses"] == 1
    assert counts["herbs"] == 1


def test_total_water_moved(funded_nursery):
    """total_water_moved sums all change amounts."""
    assert total_water_moved(funded_nursery) == 800


def test_average_change_amount(funded_nursery):
    """average_change_amount computes correct average."""
    assert average_change_amount(funded_nursery) == 400.0


def test_max_water_level(funded_nursery):
    """max_water_level finds the highest level."""
    assert max_water_level(funded_nursery) == 500


def test_min_water_level(funded_nursery):
    """min_water_level finds the lowest level."""
    assert min_water_level(funded_nursery) == -800
