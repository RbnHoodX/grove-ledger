"""Serialization of nursery data to and from dictionaries."""


def plot_to_dict(plot):
    """Convert a Plot to a dictionary representation."""
    return {
        "name": plot.name,
        "kind": plot.kind,
        "water_level": plot.water_level,
        "change_count": len(plot.changes()),
    }


def change_to_dict(change):
    """Convert a Change to a dictionary representation."""
    return {
        "id": change.id,
        "inflow_plot": change.inflow_plot.name,
        "outflow_plot": change.outflow_plot.name,
        "amount": change.amount,
        "memo": change.memo,
    }


def nursery_to_dict(nursery):
    """Convert a Nursery to a complete dictionary representation."""
    return {
        "plots": [plot_to_dict(p) for p in nursery.plots()],
        "changes": [change_to_dict(c) for c in nursery.changelog_entries()],
        "water_balance": {
            "inflows": nursery.water_balance()[0],
            "outflows": nursery.water_balance()[1],
        },
    }


def nursery_summary(nursery):
    """Generate a summary dict of the nursery state."""
    plots = nursery.plots()
    changes = nursery.changelog_entries()
    return {
        "total_plots": len(plots),
        "total_changes": len(changes),
        "plot_kinds": list(set(p.kind for p in plots)),
        "total_water_moved": sum(c.amount for c in changes),
    }
