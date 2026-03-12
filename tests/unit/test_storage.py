"""Unit tests for storage modules."""

from nursery import Nursery
from storage.serializer import plot_to_dict, change_to_dict, nursery_to_dict, nursery_summary
from storage.exporter import export_json_string, export_plots_csv_string, export_text_summary
from storage.loader import load_json_string, validate_json_structure


def test_plot_to_dict():
    """plot_to_dict returns correct keys."""
    n = Nursery()
    p = n.create_plot("roses")
    d = plot_to_dict(p)
    assert d["name"] == "roses"
    assert d["kind"] == "bed"
    assert d["water_level"] == 0


def test_change_to_dict():
    """change_to_dict returns correct keys."""
    n = Nursery()
    n.create_plot("roses")
    n.create_plot("reservoir", "reservoir")
    c = n.irrigate("roses", "reservoir", 100, "test")
    d = change_to_dict(c)
    assert d["id"] == 1
    assert d["amount"] == 100


def test_nursery_to_dict():
    """nursery_to_dict includes plots and changes."""
    n = Nursery()
    n.create_plot("roses")
    n.create_plot("reservoir", "reservoir")
    n.irrigate("roses", "reservoir", 100)
    d = nursery_to_dict(n)
    assert len(d["plots"]) == 2
    assert len(d["changes"]) == 1


def test_nursery_summary():
    """nursery_summary returns correct counts."""
    n = Nursery()
    n.create_plot("roses")
    n.create_plot("reservoir", "reservoir")
    n.irrigate("roses", "reservoir", 100)
    s = nursery_summary(n)
    assert s["total_plots"] == 2
    assert s["total_changes"] == 1


def test_export_json_roundtrip():
    """JSON export and import preserves plot data."""
    n = Nursery()
    n.create_plot("roses")
    n.create_plot("reservoir", "reservoir")
    n.irrigate("roses", "reservoir", 100, "test")
    json_str = export_json_string(n)
    n2 = load_json_string(json_str)
    assert len(n2.plots()) == 2
    assert len(n2.changelog_entries()) == 1


def test_export_csv_string():
    """CSV export produces correct header and rows."""
    n = Nursery()
    n.create_plot("roses")
    csv_str = export_plots_csv_string(n)
    assert "name" in csv_str
    assert "roses" in csv_str


def test_export_text_summary():
    """Text summary contains key information."""
    n = Nursery()
    n.create_plot("roses")
    text = export_text_summary(n)
    assert "roses" in text
    assert "Summary" in text


def test_validate_json_structure():
    """validate_json_structure checks required keys."""
    ok, _ = validate_json_structure({"plots": []})
    assert ok
    ok, _ = validate_json_structure({})
    assert not ok
    ok, _ = validate_json_structure({"plots": "wrong"})
    assert not ok
