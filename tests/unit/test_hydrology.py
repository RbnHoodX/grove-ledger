"""Unit tests for hydrology modules."""

from plot import Plot
from hydrology.capacity import (
    estimate_capacity, seasonal_capacity, available_capacity,
    capacity_utilization, is_over_capacity
)
from hydrology.flow import (
    calculate_flow_duration, is_feasible, optimal_flow_rate,
    flow_efficiency, split_flow, merge_flows
)
from hydrology.schedule import IrrigationPlan


def test_estimate_capacity():
    """estimate_capacity returns positive values."""
    cap = estimate_capacity("bed", area_sqm=2.0, depth_cm=30)
    assert cap > 0


def test_seasonal_capacity():
    """seasonal_capacity adjusts by season."""
    summer = seasonal_capacity(1000, "summer")
    winter = seasonal_capacity(1000, "winter")
    assert summer > winter


def test_available_capacity():
    """available_capacity returns non-negative value."""
    p = Plot("test", "bed")
    avail = available_capacity(p)
    assert avail >= 0


def test_capacity_utilization_empty():
    """capacity_utilization is 0 for empty plot."""
    p = Plot("test", "bed")
    assert capacity_utilization(p) == 0.0


def test_is_over_capacity():
    """is_over_capacity returns False for empty plot."""
    p = Plot("test", "bed")
    assert not is_over_capacity(p)


def test_calculate_flow_duration():
    """calculate_flow_duration computes correct time."""
    assert calculate_flow_duration(100, 10) == 10.0


def test_is_feasible():
    """is_feasible checks against max duration."""
    assert is_feasible(100, flow_rate=10)
    assert not is_feasible(100000, flow_rate=1)


def test_optimal_flow_rate():
    """optimal_flow_rate computes correct rate."""
    assert optimal_flow_rate(100, 10) == 10.0


def test_flow_efficiency():
    """flow_efficiency computes correct ratio."""
    assert flow_efficiency(100, 90) == 0.9
    assert flow_efficiency(0, 0) == 0.0


def test_split_flow():
    """split_flow distributes evenly with remainder."""
    amounts = split_flow(100, 3)
    assert sum(amounts) == 100
    assert len(amounts) == 3


def test_merge_flows():
    """merge_flows sums positive values only."""
    assert merge_flows([100, -50, 200, 0]) == 300


def test_irrigation_plan():
    """IrrigationPlan tracks steps."""
    plan = IrrigationPlan("test")
    plan.add_step("roses", "reservoir", 100, "morning")
    plan.add_step("herbs", "reservoir", 50, "morning")
    assert plan.step_count() == 2
    assert plan.total_water() == 150
    assert plan.involves_plot("roses")
    assert not plan.involves_plot("ferns")
