"""Water capacity estimation and management for garden plots."""

from config import MOISTURE_RETENTION, SEASONAL_FACTORS


# Typical water capacity by plot kind (in liters)
BASE_CAPACITY = {
    "bed": 200,
    "reservoir": 5000,
    "channel": 50,
    "pond": 10000,
    "raised": 150,
}


def estimate_capacity(plot_kind, area_sqm=1.0, depth_cm=30):
    """Estimate the water-holding capacity of a plot.

    Args:
        plot_kind: The kind of plot (bed, reservoir, etc.)
        area_sqm: Area in square meters.
        depth_cm: Soil depth in centimeters.

    Returns:
        Estimated capacity in liters.
    """
    base = BASE_CAPACITY.get(plot_kind, 100)
    retention = MOISTURE_RETENTION.get(plot_kind, 0.5)
    raw_volume = area_sqm * (depth_cm / 100) * 1000  # liters
    return int(raw_volume * retention + base)


def seasonal_capacity(base_capacity, season):
    """Adjust capacity based on seasonal factors.

    In summer, evaporation reduces effective capacity.
    In winter, frozen ground reduces absorption.
    """
    factor = SEASONAL_FACTORS.get(season, 1.0)
    return int(base_capacity * factor)


def available_capacity(plot):
    """Calculate remaining capacity for a plot.

    Returns how much additional water the plot can receive
    before reaching its estimated capacity based on kind.
    """
    max_cap = BASE_CAPACITY.get(plot.kind, 200)
    current = plot.water_level
    return max(0, max_cap - current)


def capacity_utilization(plot):
    """Calculate what percentage of capacity is currently used.

    Returns a float between 0.0 and 1.0 (can exceed 1.0 if over-capacity).
    """
    max_cap = BASE_CAPACITY.get(plot.kind, 200)
    if max_cap <= 0:
        return 0.0
    return plot.water_level / max_cap


def is_over_capacity(plot):
    """Check if a plot exceeds its estimated water capacity."""
    max_cap = BASE_CAPACITY.get(plot.kind, 200)
    return plot.water_level > max_cap


def recommended_irrigation_amount(source_plot, dest_plot, season="summer"):
    """Calculate recommended irrigation amount between two plots.

    Takes into account the source's available water and the
    destination's remaining capacity.
    """
    source_available = source_plot.water_level
    dest_remaining = available_capacity(dest_plot)
    factor = SEASONAL_FACTORS.get(season, 1.0)
    recommended = int(min(source_available, dest_remaining) * factor)
    return max(0, recommended)
