"""Report generation for nursery water management."""

from utils.formatting import format_header, format_table_row, format_change_summary
from utils.aggregation import total_water_moved, average_change_amount


def generate_nursery_report(nursery):
    """Generate a comprehensive nursery report.

    Includes plot status, change history summary, and water balance.
    """
    lines = [format_header("Nursery Water Report")]
    lines.append("")

    # Plot status section
    lines.append("PLOTS")
    lines.append("-" * 50)
    plots = sorted(nursery.plots(), key=lambda p: p.name)
    widths = [20, 12, 12]
    lines.append(format_table_row(["Name", "Kind", "Water"], widths))
    lines.append(format_table_row(["----", "----", "-----"], widths))
    for p in plots:
        lines.append(format_table_row([p.name, p.kind, p.water_level], widths))
    lines.append("")

    # Change history section
    changes = nursery.changelog_entries()
    lines.append(f"CHANGES ({len(changes)} total)")
    lines.append("-" * 50)
    for c in changes[-10:]:  # Last 10 changes
        lines.append(format_change_summary(c))
    if len(changes) > 10:
        lines.append(f"  ... and {len(changes) - 10} more")
    lines.append("")

    # Statistics section
    lines.append("STATISTICS")
    lines.append("-" * 50)
    lines.append(f"  Total water moved: {total_water_moved(nursery)}")
    lines.append(f"  Average per change: {average_change_amount(nursery):.1f}")
    inflows, outflows = nursery.water_balance()
    lines.append(f"  Water balance: inflows={inflows}, outflows={outflows}")
    lines.append("")

    return "\n".join(lines)


def generate_plot_report(nursery, plot_name):
    """Generate a detailed report for a single plot."""
    plot = nursery.get_plot(plot_name)
    lines = [format_header(f"Plot Report: {plot.name}")]
    lines.append("")
    lines.append(f"  Kind: {plot.kind}")
    lines.append(f"  Water level: {plot.water_level}")
    lines.append("")

    changes = plot.changes()
    lines.append(f"  Changes ({len(changes)} total):")
    for c in changes:
        direction = "IN" if c.inflow_plot.name == plot_name else "OUT"
        other = c.outflow_plot.name if direction == "IN" else c.inflow_plot.name
        lines.append(f"    #{c.id} {direction} {c.amount} ({other}) {c.memo}")

    return "\n".join(lines)


def generate_comparison_report(nursery, plot_name_a, plot_name_b):
    """Generate a comparison report between two plots."""
    plot_a = nursery.get_plot(plot_name_a)
    plot_b = nursery.get_plot(plot_name_b)
    lines = [format_header(f"Comparison: {plot_a.name} vs {plot_b.name}")]
    lines.append("")
    widths = [20, 15, 15]
    lines.append(format_table_row(["Metric", plot_a.name, plot_b.name], widths))
    lines.append(format_table_row(["------", "-----", "-----"], widths))
    lines.append(format_table_row(["Kind", plot_a.kind, plot_b.kind], widths))
    lines.append(format_table_row(["Water level", plot_a.water_level, plot_b.water_level], widths))
    lines.append(format_table_row(["Changes", len(plot_a.changes()), len(plot_b.changes())], widths))
    return "\n".join(lines)
