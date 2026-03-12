"""Water flow analysis and routing calculations."""

from config import DEFAULT_FLOW_RATE, MAX_IRRIGATION_DURATION


def calculate_flow_duration(amount, flow_rate=DEFAULT_FLOW_RATE):
    """Calculate how long an irrigation takes at a given flow rate.

    Args:
        amount: Volume of water in liters.
        flow_rate: Flow rate in liters per minute.

    Returns:
        Duration in minutes.
    """
    if flow_rate <= 0:
        return 0
    return amount / flow_rate


def is_feasible(amount, flow_rate=DEFAULT_FLOW_RATE,
                max_duration=MAX_IRRIGATION_DURATION):
    """Check if an irrigation amount is feasible within time constraints."""
    duration = calculate_flow_duration(amount, flow_rate)
    return duration <= max_duration


def optimal_flow_rate(amount, target_duration):
    """Calculate the flow rate needed to deliver an amount in a target time.

    Args:
        amount: Volume of water in liters.
        target_duration: Target duration in minutes.

    Returns:
        Required flow rate in liters per minute.
    """
    if target_duration <= 0:
        return 0
    return amount / target_duration


def flow_efficiency(amount_sent, amount_received):
    """Calculate the efficiency of water delivery.

    Accounts for losses due to evaporation, seepage, etc.
    Returns a float between 0.0 and 1.0.
    """
    if amount_sent <= 0:
        return 0.0
    ratio = amount_received / amount_sent
    return min(1.0, max(0.0, ratio))


def split_flow(total_amount, num_destinations):
    """Split a total flow amount evenly across multiple destinations.

    Returns a list of amounts that sum to total_amount. The last
    destination may receive a slightly different amount due to
    integer division.
    """
    if num_destinations <= 0:
        return []
    base = total_amount // num_destinations
    remainder = total_amount % num_destinations
    amounts = [base] * num_destinations
    for i in range(remainder):
        amounts[i] += 1
    return amounts


def merge_flows(amounts):
    """Merge multiple flow amounts into a single total.

    Filters out any non-positive values.
    """
    return sum(a for a in amounts if a > 0)


def cascade_flow(plots, amount, loss_per_hop=0.05):
    """Calculate the water remaining after cascading through plots.

    At each hop, a percentage of the water is lost to absorption.
    Returns a list of (plot_name, received_amount) tuples.
    """
    results = []
    remaining = amount
    for plot in plots:
        received = int(remaining * (1 - loss_per_hop))
        results.append((plot.name, received))
        remaining = received
    return results
