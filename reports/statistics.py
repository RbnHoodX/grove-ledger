"""Statistical analysis of nursery water data."""

from utils.aggregation import (
    net_flow_per_plot,
    water_level_distribution,
    water_utilization_rate,
)


def compute_nursery_stats(nursery):
    """Compute comprehensive statistics for the nursery.

    Returns a dictionary of computed statistics.
    """
    plots = nursery.plots()
    changes = nursery.changelog_entries()
    levels = water_level_distribution(nursery)
    flows = net_flow_per_plot(nursery)
    utilization = water_utilization_rate(nursery)

    level_values = list(levels.values())
    if level_values:
        mean_level = sum(level_values) / len(level_values)
        variance = sum((v - mean_level) ** 2 for v in level_values) / len(level_values)
    else:
        mean_level = 0.0
        variance = 0.0

    amounts = [c.amount for c in changes]
    if amounts:
        mean_amount = sum(amounts) / len(amounts)
        max_amount = max(amounts)
        min_amount = min(amounts)
    else:
        mean_amount = 0.0
        max_amount = 0
        min_amount = 0

    return {
        "plot_count": len(plots),
        "change_count": len(changes),
        "mean_water_level": mean_level,
        "water_level_variance": variance,
        "mean_change_amount": mean_amount,
        "max_change_amount": max_amount,
        "min_change_amount": min_amount,
        "net_flows": flows,
        "utilization_rates": utilization,
    }


def find_most_active_plot(nursery):
    """Find the plot with the highest utilization rate."""
    rates = water_utilization_rate(nursery)
    if not rates:
        return None
    return max(rates, key=rates.get)


def find_highest_water_plot(nursery):
    """Find the plot with the highest water level."""
    levels = water_level_distribution(nursery)
    if not levels:
        return None
    return max(levels, key=levels.get)


def find_lowest_water_plot(nursery):
    """Find the plot with the lowest water level."""
    levels = water_level_distribution(nursery)
    if not levels:
        return None
    return min(levels, key=levels.get)


def water_balance_check(nursery):
    """Verify that total inflows equal total outflows.

    Returns (is_balanced, difference) tuple.
    """
    inflows, outflows = nursery.water_balance()
    return inflows == outflows, inflows - outflows


def identify_dry_plots(nursery, threshold=0):
    """Identify plots with water level at or below the threshold."""
    return [
        p.name for p in nursery.plots()
        if p.water_level <= threshold
    ]


def identify_saturated_plots(nursery, threshold=1000):
    """Identify plots with water level above the threshold."""
    return [
        p.name for p in nursery.plots()
        if p.water_level > threshold
    ]
