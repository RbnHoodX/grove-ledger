"""Integration tests for data pipeline workflows."""

from nursery import Nursery
from scripts.seed_data import create_small_nursery, create_medium_nursery
from reports.statistics import compute_nursery_stats, water_balance_check
from hydrology.schedule import create_rotation_plan, execute_plan, plan_summary
from hydrology.capacity import estimate_capacity, seasonal_capacity


def test_seed_data_small():
    """Small seed nursery is valid and balanced."""
    n = create_small_nursery()
    assert len(n.plots()) == 3
    balanced, _ = water_balance_check(n)
    assert balanced


def test_seed_data_medium():
    """Medium seed nursery is valid and balanced."""
    n = create_medium_nursery()
    assert len(n.plots()) == 6
    balanced, _ = water_balance_check(n)
    assert balanced


def test_stats_on_seeded_nursery():
    """Statistics computed correctly on seeded data."""
    n = create_medium_nursery()
    stats = compute_nursery_stats(n)
    assert stats["plot_count"] == 6
    assert stats["change_count"] > 0
    assert stats["mean_change_amount"] > 0


def test_rotation_plan_execute():
    """Create and execute a rotation plan."""
    n = Nursery()
    n.create_plot("roses", "bed")
    n.create_plot("herbs", "bed")
    n.create_plot("tank", "reservoir")

    plan = create_rotation_plan(n, "tank", ["roses", "herbs"], 50)
    assert plan.step_count() == 2
    results = execute_plan(n, plan)
    assert len(results) == 2
    for i, result in results:
        assert not isinstance(result, Exception)


def test_plan_summary_output():
    """Plan summary generates readable text."""
    n = Nursery()
    n.create_plot("tank", "reservoir")
    plan = create_rotation_plan(n, "tank", ["roses"], 100)
    text = plan_summary(plan)
    assert "rotation" in text
    assert "100" in text


def test_capacity_estimation():
    """Capacity estimation produces reasonable values."""
    bed_cap = estimate_capacity("bed", area_sqm=4.0)
    res_cap = estimate_capacity("reservoir", area_sqm=4.0)
    assert res_cap > bed_cap  # Reservoirs hold more


def test_seasonal_adjustment():
    """Seasonal adjustment changes capacity appropriately."""
    base = 1000
    summer = seasonal_capacity(base, "summer")
    winter = seasonal_capacity(base, "winter")
    assert summer > winter
    assert summer > base  # Summer factor > 1
    assert winter < base  # Winter factor < 1
