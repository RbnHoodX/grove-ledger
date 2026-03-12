"""Output formatting utilities for water data display."""

from config import REPORT_SEPARATOR, REPORT_HEADER_WIDTH


def format_water_amount(amount, unit="liters"):
    """Format a water amount with unit suffix."""
    if amount >= 1000:
        return f"{amount / 1000:.1f}k {unit}"
    return f"{amount} {unit}"


def format_percentage(value, total):
    """Format a value as a percentage of total."""
    if total == 0:
        return "0.0%"
    pct = (value / total) * 100
    return f"{pct:.1f}%"


def format_table_row(columns, widths):
    """Format a row of data with fixed column widths."""
    parts = []
    for col, width in zip(columns, widths):
        text = str(col)
        if isinstance(col, (int, float)):
            parts.append(text.rjust(width))
        else:
            parts.append(text.ljust(width))
    return " ".join(parts)


def format_header(title, width=REPORT_HEADER_WIDTH):
    """Format a centered header with separators."""
    lines = [
        REPORT_SEPARATOR[:width],
        title.center(width),
        REPORT_SEPARATOR[:width],
    ]
    return "\n".join(lines)


def format_change_summary(change):
    """Format a single change entry as a summary line."""
    inflow_name = change.inflow_plot.name
    outflow_name = change.outflow_plot.name
    return (f"#{change.id}: {inflow_name} <- {outflow_name} "
            f"({change.amount} units) {change.memo}")


def format_plot_status(plot):
    """Format a plot's current status."""
    level = plot.water_level
    indicator = "+" if level > 0 else ("-" if level < 0 else "=")
    return f"[{indicator}] {plot.name} ({plot.kind}): {level} units"


def truncate(text, max_length=40):
    """Truncate text to max length with ellipsis."""
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."
