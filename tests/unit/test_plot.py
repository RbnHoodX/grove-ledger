"""Unit tests for the Plot class."""

from plot import Plot


def test_plot_creation():
    """Plot can be created with name and kind."""
    p = Plot("roses", "bed")
    assert p.name == "roses"
    assert p.kind == "bed"


def test_plot_default_kind():
    """Plot defaults to kind 'bed'."""
    p = Plot("test")
    assert p.kind == "bed"


def test_plot_initial_water_level():
    """New plot has water level of zero."""
    p = Plot("test")
    assert p.water_level == 0


def test_plot_initial_changes():
    """New plot has no changes."""
    p = Plot("test")
    assert p.changes() == []


def test_plot_repr():
    """Plot repr includes name and kind."""
    p = Plot("roses", "bed")
    r = repr(p)
    assert "roses" in r
    assert "bed" in r
