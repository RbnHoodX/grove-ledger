"""Input validation utilities for the grove-ledger system."""

from config import PLOT_KINDS


def validate_plot_name(name):
    """Validate a plot name is non-empty and reasonable.

    Returns (is_valid, error_message) tuple.
    """
    if not name or not name.strip():
        return False, "plot name cannot be empty"
    if len(name) > 100:
        return False, "plot name too long (max 100 characters)"
    if not all(c.isalnum() or c in "-_ " for c in name):
        return False, "plot name contains invalid characters"
    return True, ""


def validate_plot_kind(kind):
    """Validate a plot kind against known types."""
    if kind not in PLOT_KINDS:
        return False, f"unknown plot kind {kind!r}; must be one of {PLOT_KINDS}"
    return True, ""


def validate_amount(amount):
    """Validate an irrigation amount is a positive integer."""
    if not isinstance(amount, int):
        return False, "amount must be an integer"
    if amount <= 0:
        return False, "amount must be positive"
    return True, ""


def validate_memo(memo):
    """Validate a memo string."""
    if not isinstance(memo, str):
        return False, "memo must be a string"
    if len(memo) > 500:
        return False, "memo too long (max 500 characters)"
    return True, ""


def validate_irrigation_params(inflow_name, outflow_name, amount):
    """Validate all irrigation parameters at once.

    Returns (is_valid, error_message) tuple.
    """
    valid, msg = validate_plot_name(inflow_name)
    if not valid:
        return False, f"inflow plot: {msg}"
    valid, msg = validate_plot_name(outflow_name)
    if not valid:
        return False, f"outflow plot: {msg}"
    if inflow_name == outflow_name:
        return False, "inflow and outflow plots must be different"
    valid, msg = validate_amount(amount)
    if not valid:
        return False, msg
    return True, ""
