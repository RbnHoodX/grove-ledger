"""Unit tests for the ChangeLog and Change classes."""

from plot import Plot
from changelog import Change, ChangeLog


def test_change_creation():
    """Change stores inflow, outflow, amount, and memo."""
    a = Plot("roses")
    b = Plot("reservoir", "reservoir")
    c = Change(a, b, 100, "test")
    assert c.inflow_plot is a
    assert c.outflow_plot is b
    assert c.amount == 100
    assert c.memo == "test"


def test_change_default_memo():
    """Change memo defaults to empty string."""
    a = Plot("roses")
    b = Plot("reservoir", "reservoir")
    c = Change(a, b, 50)
    assert c.memo == ""


def test_change_initial_id():
    """Change starts with id 0 before recording."""
    a = Plot("roses")
    b = Plot("reservoir", "reservoir")
    c = Change(a, b, 100)
    assert c.id == 0


def test_changelog_empty():
    """New changelog has no changes."""
    cl = ChangeLog()
    assert cl.changes() == []


def test_changelog_record():
    """Recording a change assigns an id and adds it to the log."""
    a = Plot("roses")
    b = Plot("reservoir", "reservoir")
    cl = ChangeLog()
    c = Change(a, b, 100)
    result = cl.record(c)
    assert result.id == 1
    assert len(cl.changes()) == 1


def test_changelog_sequential_ids():
    """Recorded changes get sequential IDs."""
    a = Plot("roses")
    b = Plot("reservoir", "reservoir")
    cl = ChangeLog()
    c1 = cl.record(Change(a, b, 100))
    c2 = cl.record(Change(a, b, 200))
    c3 = cl.record(Change(a, b, 300))
    assert c1.id == 1
    assert c2.id == 2
    assert c3.id == 3


def test_changelog_returns_copy():
    """changes() returns a copy of the internal list."""
    cl = ChangeLog()
    a = Plot("roses")
    b = Plot("reservoir", "reservoir")
    cl.record(Change(a, b, 100))
    changes = cl.changes()
    changes.clear()
    assert len(cl.changes()) == 1
