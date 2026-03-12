"""Integration tests for complete nursery workflows."""

from nursery import Nursery
from storage.serializer import nursery_to_dict
from storage.exporter import export_json_string
from storage.loader import load_json_string
from reports.generator import generate_nursery_report
from scripts.validate_nursery import run_all_checks


def test_full_create_irrigate_report():
    """Full workflow: create plots, irrigate, generate report."""
    n = Nursery()
    n.create_plot("roses", "bed")
    n.create_plot("herbs", "bed")
    n.create_plot("tank", "reservoir")

    n.irrigate("roses", "tank", 500, "morning")
    n.irrigate("herbs", "tank", 300, "morning")

    report = generate_nursery_report(n)
    assert "roses" in report
    assert "herbs" in report
    assert "tank" in report


def test_serialize_roundtrip():
    """Full workflow: create nursery, export JSON, reload, verify."""
    n = Nursery()
    n.create_plot("roses", "bed")
    n.create_plot("tank", "reservoir")
    n.irrigate("roses", "tank", 200, "test")

    json_str = export_json_string(n)
    n2 = load_json_string(json_str)

    assert len(n2.plots()) == len(n.plots())
    assert len(n2.changelog_entries()) == len(n.changelog_entries())
    assert n2.get_plot("roses").water_level == 200


def test_validation_passes_on_normal_nursery():
    """Validation checks pass on a properly constructed nursery."""
    n = Nursery()
    n.create_plot("roses", "bed")
    n.create_plot("herbs", "bed")
    n.create_plot("tank", "reservoir")
    n.irrigate("roses", "tank", 100)
    n.irrigate("herbs", "tank", 50)

    passed, results = run_all_checks(n)
    assert passed, f"Checks failed: {[r for r in results if not r[1]]}"


def test_multiple_irrigations_consistent():
    """Multiple irrigations maintain water balance consistency."""
    n = Nursery()
    n.create_plot("a", "bed")
    n.create_plot("b", "bed")
    n.create_plot("c", "reservoir")

    for i in range(20):
        n.irrigate("a", "c", 10, f"batch-{i}")
        n.irrigate("b", "c", 5, f"batch-{i}")

    assert n.get_plot("a").water_level == 200
    assert n.get_plot("b").water_level == 100
    assert n.get_plot("c").water_level == -300

    inflows, outflows = n.water_balance()
    assert inflows == outflows
