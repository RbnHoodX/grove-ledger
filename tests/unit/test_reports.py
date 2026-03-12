"""Unit tests for report modules."""

from nursery import Nursery
from reports.generator import (
    generate_nursery_report, generate_plot_report, generate_comparison_report
)
from reports.statistics import (
    compute_nursery_stats, find_most_active_plot,
    find_highest_water_plot, find_lowest_water_plot,
    water_balance_check, identify_dry_plots
)
from reports.formatter import (
    format_as_markdown, format_as_plain_text, format_as_html,
    build_plot_section, build_change_section, build_balance_section
)


def test_generate_nursery_report():
    """generate_nursery_report produces text output."""
    n = Nursery()
    n.create_plot("roses")
    n.create_plot("reservoir", "reservoir")
    n.irrigate("roses", "reservoir", 100)
    report = generate_nursery_report(n)
    assert "roses" in report
    assert "PLOTS" in report


def test_generate_plot_report():
    """generate_plot_report shows plot details."""
    n = Nursery()
    n.create_plot("roses")
    n.create_plot("reservoir", "reservoir")
    n.irrigate("roses", "reservoir", 100)
    report = generate_plot_report(n, "roses")
    assert "roses" in report
    assert "bed" in report


def test_generate_comparison_report():
    """generate_comparison_report compares two plots."""
    n = Nursery()
    n.create_plot("roses")
    n.create_plot("herbs")
    report = generate_comparison_report(n, "roses", "herbs")
    assert "roses" in report
    assert "herbs" in report


def test_compute_nursery_stats():
    """compute_nursery_stats returns expected keys."""
    n = Nursery()
    n.create_plot("roses")
    n.create_plot("reservoir", "reservoir")
    n.irrigate("roses", "reservoir", 100)
    stats = compute_nursery_stats(n)
    assert stats["plot_count"] == 2
    assert stats["change_count"] == 1


def test_find_most_active_plot():
    """find_most_active_plot identifies the busiest plot."""
    n = Nursery()
    n.create_plot("roses")
    n.create_plot("herbs")
    n.create_plot("reservoir", "reservoir")
    n.irrigate("roses", "reservoir", 100)
    n.irrigate("herbs", "reservoir", 100)
    result = find_most_active_plot(n)
    assert result == "reservoir"


def test_find_highest_water_plot():
    """find_highest_water_plot finds the wettest plot."""
    n = Nursery()
    n.create_plot("roses")
    n.create_plot("reservoir", "reservoir")
    n.irrigate("roses", "reservoir", 100)
    assert find_highest_water_plot(n) == "roses"


def test_find_lowest_water_plot():
    """find_lowest_water_plot finds the driest plot."""
    n = Nursery()
    n.create_plot("roses")
    n.create_plot("reservoir", "reservoir")
    n.irrigate("roses", "reservoir", 100)
    assert find_lowest_water_plot(n) == "reservoir"


def test_water_balance_check():
    """water_balance_check confirms balance."""
    n = Nursery()
    n.create_plot("roses")
    n.create_plot("reservoir", "reservoir")
    n.irrigate("roses", "reservoir", 100)
    balanced, diff = water_balance_check(n)
    assert balanced
    assert diff == 0


def test_identify_dry_plots():
    """identify_dry_plots finds plots at or below threshold."""
    n = Nursery()
    n.create_plot("roses")
    n.create_plot("herbs")
    dry = identify_dry_plots(n)
    assert "roses" in dry
    assert "herbs" in dry


def test_format_as_markdown():
    """format_as_markdown produces markdown output."""
    md = format_as_markdown("Test", [("Section", ["line1", "line2"])])
    assert "# Test" in md
    assert "## Section" in md


def test_format_as_plain_text():
    """format_as_plain_text produces plain output."""
    text = format_as_plain_text("Test", [("Section", ["line1"])])
    assert "Test" in text
    assert "Section" in text


def test_format_as_html():
    """format_as_html produces HTML output."""
    html = format_as_html("Test", [("Section", ["line1"])])
    assert "<h1>" in html
    assert "<h2>" in html


def test_build_plot_section():
    """build_plot_section returns heading and content."""
    n = Nursery()
    n.create_plot("roses")
    heading, content = build_plot_section(n)
    assert heading == "Plot Status"
    assert len(content) == 1


def test_build_change_section():
    """build_change_section returns heading and content."""
    n = Nursery()
    n.create_plot("roses")
    n.create_plot("reservoir", "reservoir")
    n.irrigate("roses", "reservoir", 100)
    heading, content = build_change_section(n)
    assert heading == "Recent Changes"
    assert len(content) == 1


def test_build_balance_section():
    """build_balance_section returns heading and content."""
    n = Nursery()
    heading, content = build_balance_section(n)
    assert heading == "Water Balance"
    assert "Balanced: Yes" in content[2]
