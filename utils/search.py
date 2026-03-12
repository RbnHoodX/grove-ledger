"""Search and filter utilities for nursery data."""


def find_plots_by_kind(nursery, kind):
    """Find all plots of a given kind."""
    return [p for p in nursery.plots() if p.kind == kind]


def find_plots_by_name_prefix(nursery, prefix):
    """Find all plots whose name starts with the given prefix."""
    prefix_lower = prefix.lower()
    return [p for p in nursery.plots()
            if p.name.lower().startswith(prefix_lower)]


def find_plots_above_level(nursery, threshold):
    """Find all plots with water level above a threshold."""
    return [p for p in nursery.plots()
            if p.water_level > threshold]


def find_plots_below_level(nursery, threshold):
    """Find all plots with water level below a threshold."""
    return [p for p in nursery.plots()
            if p.water_level < threshold]


def find_changes_by_memo(nursery, keyword):
    """Find all changes whose memo contains the keyword (case-insensitive)."""
    keyword_lower = keyword.lower()
    return [c for c in nursery.changelog_entries()
            if keyword_lower in c.memo.lower()]


def find_changes_by_amount_range(nursery, min_amount, max_amount):
    """Find all changes with amount in the given range (inclusive)."""
    return [c for c in nursery.changelog_entries()
            if min_amount <= c.amount <= max_amount]


def find_changes_for_plot(nursery, plot_name):
    """Find all changes involving a specific plot (as inflow or outflow)."""
    return [c for c in nursery.changelog_entries()
            if c.inflow_plot.name == plot_name or c.outflow_plot.name == plot_name]


def count_changes_per_plot(nursery):
    """Count the number of changes each plot is involved in."""
    counts = {}
    for plot in nursery.plots():
        counts[plot.name] = 0
    for change in nursery.changelog_entries():
        counts[change.inflow_plot.name] = counts.get(change.inflow_plot.name, 0) + 1
        counts[change.outflow_plot.name] = counts.get(change.outflow_plot.name, 0) + 1
    return counts
