"""Load nursery data from files and dictionaries."""

import json

from nursery import Nursery


def load_json(filepath):
    """Load nursery data from a JSON file.

    Returns a Nursery populated with plots and irrigation changes
    based on the stored data.
    """
    with open(filepath, "r") as f:
        data = json.load(f)
    return load_from_dict(data)


def load_json_string(json_string):
    """Load nursery data from a JSON string."""
    data = json.loads(json_string)
    return load_from_dict(data)


def load_from_dict(data):
    """Reconstruct a Nursery from a dictionary.

    Note: This recreates the plots and replays the changes to
    rebuild the nursery state. Change IDs in the replayed nursery
    will be assigned sequentially and may differ from the original
    if changes were recorded in a different order.
    """
    nursery = Nursery()
    for plot_data in data.get("plots", []):
        nursery.create_plot(plot_data["name"], plot_data.get("kind", "bed"))
    for change_data in data.get("changes", []):
        nursery.irrigate(
            change_data["inflow_plot"],
            change_data["outflow_plot"],
            change_data["amount"],
            change_data.get("memo", ""),
        )
    return nursery


def validate_json_structure(data):
    """Validate that a dictionary has the expected nursery structure.

    Returns (is_valid, error_message) tuple.
    """
    if not isinstance(data, dict):
        return False, "top-level must be a dictionary"
    if "plots" not in data:
        return False, "missing 'plots' key"
    if not isinstance(data["plots"], list):
        return False, "'plots' must be a list"
    for i, plot in enumerate(data["plots"]):
        if not isinstance(plot, dict):
            return False, f"plot[{i}] must be a dictionary"
        if "name" not in plot:
            return False, f"plot[{i}] missing 'name'"
    for i, change in enumerate(data.get("changes", [])):
        if not isinstance(change, dict):
            return False, f"change[{i}] must be a dictionary"
        for key in ("inflow_plot", "outflow_plot", "amount"):
            if key not in change:
                return False, f"change[{i}] missing '{key}'"
    return True, ""
