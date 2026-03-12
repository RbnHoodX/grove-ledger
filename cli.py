"""Command-line interface for the grove-ledger nursery system."""

import sys
from nursery import Nursery
from config import PLOT_KINDS, SEASONAL_FACTORS


def parse_args(args):
    """Parse command-line arguments into a command and parameters."""
    if not args:
        return None, {}
    command = args[0].lower()
    params = {}
    i = 1
    while i < len(args):
        if args[i].startswith("--"):
            key = args[i][2:]
            if i + 1 < len(args) and not args[i + 1].startswith("--"):
                params[key] = args[i + 1]
                i += 2
            else:
                params[key] = True
                i += 1
        else:
            params.setdefault("positional", []).append(args[i])
            i += 1
    return command, params


def cmd_create_plot(nursery, params):
    """Handle plot creation command."""
    name = params.get("name", "")
    kind = params.get("kind", "bed")
    if not name:
        print("Error: --name is required")
        return False
    if kind not in PLOT_KINDS:
        print(f"Error: kind must be one of {PLOT_KINDS}")
        return False
    try:
        plot = nursery.create_plot(name, kind)
        print(f"Created plot '{plot.name}' (kind={plot.kind})")
        return True
    except ValueError as e:
        print(f"Error: {e}")
        return False


def cmd_irrigate(nursery, params):
    """Handle irrigation command."""
    inflow = params.get("inflow", "")
    outflow = params.get("outflow", "")
    amount_str = params.get("amount", "0")
    memo = params.get("memo", "")
    if not inflow or not outflow:
        print("Error: --inflow and --outflow are required")
        return False
    try:
        amount = int(amount_str)
    except ValueError:
        print("Error: --amount must be an integer")
        return False
    try:
        change = nursery.irrigate(inflow, outflow, amount, memo)
        print(f"Irrigated {change.amount} from {inflow} to {outflow} (id={change.id})")
        return True
    except (ValueError, KeyError) as e:
        print(f"Error: {e}")
        return False


def cmd_status(nursery, params):
    """Display nursery status."""
    plots = nursery.plots()
    if not plots:
        print("No plots in nursery.")
        return True
    print(f"{'Name':<20} {'Kind':<12} {'Water Level':>12}")
    print("-" * 44)
    for plot in sorted(plots, key=lambda p: p.name):
        print(f"{plot.name:<20} {plot.kind:<12} {plot.water_level:>12}")
    print("-" * 44)
    inflows, outflows = nursery.water_balance()
    print(f"Water balance: inflows={inflows}, outflows={outflows}")
    return True


def cmd_history(nursery, params):
    """Display change history."""
    changes = nursery.changelog_entries()
    if not changes:
        print("No changes recorded.")
        return True
    limit = int(params.get("limit", "0"))
    if limit > 0:
        changes = changes[-limit:]
    print(f"{'ID':>5} {'Inflow':<15} {'Outflow':<15} {'Amount':>8} {'Memo'}")
    print("-" * 60)
    for c in changes:
        print(f"{c.id:>5} {c.inflow_plot.name:<15} {c.outflow_plot.name:<15} "
              f"{c.amount:>8} {c.memo}")
    return True


def cmd_help(_nursery, _params):
    """Display help information."""
    print("grove-ledger — Water management for garden plots")
    print()
    print("Commands:")
    print("  create-plot  --name NAME [--kind KIND]")
    print("  irrigate     --inflow NAME --outflow NAME --amount N [--memo TEXT]")
    print("  status")
    print("  history      [--limit N]")
    print("  help")
    print()
    print(f"Plot kinds: {', '.join(PLOT_KINDS)}")
    print(f"Seasons: {', '.join(SEASONAL_FACTORS.keys())}")
    return True


COMMANDS = {
    "create-plot": cmd_create_plot,
    "irrigate": cmd_irrigate,
    "status": cmd_status,
    "history": cmd_history,
    "help": cmd_help,
}


def run(args=None):
    """Main entry point for the CLI."""
    if args is None:
        args = sys.argv[1:]
    command, params = parse_args(args)
    if command is None or command not in COMMANDS:
        cmd_help(None, {})
        return 1
    nursery = Nursery()
    handler = COMMANDS[command]
    success = handler(nursery, params)
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(run())
