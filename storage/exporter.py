"""Export nursery data to various file formats."""

import json
import csv
import io

from storage.serializer import nursery_to_dict, plot_to_dict, change_to_dict


def export_json(nursery, filepath):
    """Export nursery data to a JSON file."""
    data = nursery_to_dict(nursery)
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)


def export_json_string(nursery):
    """Export nursery data as a JSON string."""
    data = nursery_to_dict(nursery)
    return json.dumps(data, indent=2)


def export_plots_csv(nursery, filepath):
    """Export plot data to a CSV file."""
    plots = nursery.plots()
    with open(filepath, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["name", "kind", "water_level", "change_count"])
        for p in sorted(plots, key=lambda x: x.name):
            d = plot_to_dict(p)
            writer.writerow([d["name"], d["kind"], d["water_level"], d["change_count"]])


def export_changes_csv(nursery, filepath):
    """Export change history to a CSV file."""
    changes = nursery.changelog_entries()
    with open(filepath, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "inflow_plot", "outflow_plot", "amount", "memo"])
        for c in changes:
            d = change_to_dict(c)
            writer.writerow([d["id"], d["inflow_plot"], d["outflow_plot"],
                             d["amount"], d["memo"]])


def export_plots_csv_string(nursery):
    """Export plot data as a CSV string."""
    buf = io.StringIO()
    plots = nursery.plots()
    writer = csv.writer(buf)
    writer.writerow(["name", "kind", "water_level", "change_count"])
    for p in sorted(plots, key=lambda x: x.name):
        d = plot_to_dict(p)
        writer.writerow([d["name"], d["kind"], d["water_level"], d["change_count"]])
    return buf.getvalue()


def export_text_summary(nursery):
    """Export nursery as a human-readable text summary."""
    lines = ["Grove Ledger Summary", "=" * 40]
    plots = nursery.plots()
    lines.append(f"Total plots: {len(plots)}")
    for p in sorted(plots, key=lambda x: x.name):
        lines.append(f"  {p.name} ({p.kind}): {p.water_level} units")
    changes = nursery.changelog_entries()
    lines.append(f"\nTotal changes: {len(changes)}")
    for c in changes:
        lines.append(f"  #{c.id}: {c.inflow_plot.name} <- {c.outflow_plot.name} "
                      f"({c.amount}) {c.memo}")
    inflows, outflows = nursery.water_balance()
    lines.append(f"\nWater balance: inflows={inflows}, outflows={outflows}")
    return "\n".join(lines)
