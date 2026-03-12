"""Aggregation and statistical utilities for water data."""


def total_water_moved(nursery):
    """Calculate the total volume of water moved across all changes."""
    return sum(c.amount for c in nursery.changelog_entries())


def average_change_amount(nursery):
    """Calculate the average amount per change entry."""
    changes = nursery.changelog_entries()
    if not changes:
        return 0.0
    return sum(c.amount for c in changes) / len(changes)


def max_water_level(nursery):
    """Find the maximum water level among all plots."""
    plots = nursery.plots()
    if not plots:
        return 0
    return max(p.water_level for p in plots)


def min_water_level(nursery):
    """Find the minimum water level among all plots."""
    plots = nursery.plots()
    if not plots:
        return 0
    return min(p.water_level for p in plots)


def water_level_distribution(nursery):
    """Get a mapping of plot names to their water levels."""
    return {p.name: p.water_level for p in nursery.plots()}


def net_flow_per_plot(nursery):
    """Calculate the net flow (inflows minus outflows) for each plot.

    A positive net flow means the plot has received more water than it gave.
    A negative net flow means the plot has given more water than it received.
    """
    net = {}
    for plot in nursery.plots():
        net[plot.name] = 0
    for change in nursery.changelog_entries():
        net[change.inflow_plot.name] = net.get(change.inflow_plot.name, 0) + change.amount
        net[change.outflow_plot.name] = net.get(change.outflow_plot.name, 0) - change.amount
    return net


def water_utilization_rate(nursery):
    """Calculate how actively each plot participates in water movement.

    Returns a dict mapping plot name to the ratio of changes involving
    that plot versus total changes.
    """
    changes = nursery.changelog_entries()
    total = len(changes)
    if total == 0:
        return {p.name: 0.0 for p in nursery.plots()}
    involvement = {}
    for plot in nursery.plots():
        count = sum(
            1 for c in changes
            if c.inflow_plot.name == plot.name or c.outflow_plot.name == plot.name
        )
        involvement[plot.name] = count / total
    return involvement
