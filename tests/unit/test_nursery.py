"""Unit tests for the Nursery class."""

from nursery import Nursery


def test_nursery_creation():
    """Nursery can be created empty."""
    n = Nursery()
    assert n.plots() == []
    assert n.changelog_entries() == []


def test_create_plot():
    """Nursery can create plots."""
    n = Nursery()
    p = n.create_plot("roses", "bed")
    assert p.name == "roses"
    assert p.kind == "bed"
    assert len(n.plots()) == 1


def test_create_duplicate_plot():
    """Creating a duplicate plot raises ValueError."""
    n = Nursery()
    n.create_plot("roses")
    try:
        n.create_plot("roses")
        assert False, "should raise ValueError"
    except ValueError:
        pass


def test_get_plot():
    """get_plot retrieves a plot by name."""
    n = Nursery()
    n.create_plot("roses")
    p = n.get_plot("roses")
    assert p.name == "roses"


def test_irrigate():
    """irrigate creates a change and updates water levels."""
    n = Nursery()
    n.create_plot("roses")
    n.create_plot("reservoir", "reservoir")
    c = n.irrigate("roses", "reservoir", 100, "test")
    assert c.amount == 100
    assert n.get_plot("roses").water_level == 100
    assert n.get_plot("reservoir").water_level == -100


def test_irrigate_negative_amount():
    """irrigate rejects non-positive amounts."""
    n = Nursery()
    n.create_plot("roses")
    n.create_plot("reservoir", "reservoir")
    try:
        n.irrigate("roses", "reservoir", 0)
        assert False, "should raise ValueError"
    except ValueError:
        pass


def test_water_balance():
    """water_balance returns equal inflows and outflows."""
    n = Nursery()
    n.create_plot("roses")
    n.create_plot("reservoir", "reservoir")
    n.irrigate("roses", "reservoir", 100)
    n.irrigate("roses", "reservoir", 200)
    inflows, outflows = n.water_balance()
    assert inflows == outflows == 300


def test_changelog_entries():
    """changelog_entries returns all recorded changes."""
    n = Nursery()
    n.create_plot("roses")
    n.create_plot("reservoir", "reservoir")
    n.irrigate("roses", "reservoir", 100)
    n.irrigate("roses", "reservoir", 200)
    assert len(n.changelog_entries()) == 2
