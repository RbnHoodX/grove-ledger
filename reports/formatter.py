"""Report formatting utilities for different output targets."""


def format_as_markdown(title, sections):
    """Format report sections as Markdown text.

    Args:
        title: Report title string.
        sections: List of (heading, content_lines) tuples.
    """
    lines = [f"# {title}", ""]
    for heading, content in sections:
        lines.append(f"## {heading}")
        lines.append("")
        for line in content:
            lines.append(line)
        lines.append("")
    return "\n".join(lines)


def format_as_plain_text(title, sections):
    """Format report sections as plain text."""
    lines = [title, "=" * len(title), ""]
    for heading, content in sections:
        lines.append(heading)
        lines.append("-" * len(heading))
        for line in content:
            lines.append(f"  {line}")
        lines.append("")
    return "\n".join(lines)


def format_as_html(title, sections):
    """Format report sections as simple HTML."""
    lines = ["<html><body>", f"<h1>{_escape(title)}</h1>"]
    for heading, content in sections:
        lines.append(f"<h2>{_escape(heading)}</h2>")
        lines.append("<ul>")
        for line in content:
            lines.append(f"  <li>{_escape(line)}</li>")
        lines.append("</ul>")
    lines.append("</body></html>")
    return "\n".join(lines)


def _escape(text):
    """Escape HTML special characters."""
    return (str(text)
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;"))


def build_plot_section(nursery):
    """Build a report section for plot status."""
    content = []
    for p in sorted(nursery.plots(), key=lambda x: x.name):
        content.append(f"{p.name} ({p.kind}): {p.water_level} units")
    return ("Plot Status", content)


def build_change_section(nursery, limit=20):
    """Build a report section for recent changes."""
    changes = nursery.changelog_entries()
    recent = changes[-limit:] if len(changes) > limit else changes
    content = []
    for c in recent:
        content.append(f"#{c.id}: {c.inflow_plot.name} <- {c.outflow_plot.name} "
                       f"({c.amount}) {c.memo}")
    if len(changes) > limit:
        content.append(f"... and {len(changes) - limit} more entries")
    return ("Recent Changes", content)


def build_balance_section(nursery):
    """Build a report section for water balance."""
    inflows, outflows = nursery.water_balance()
    content = [
        f"Total inflows: {inflows}",
        f"Total outflows: {outflows}",
        f"Balanced: {'Yes' if inflows == outflows else 'No'}",
    ]
    return ("Water Balance", content)
