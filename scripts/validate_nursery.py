"""Validation script to check nursery data integrity."""

from nursery import Nursery


def check_water_balance(nursery):
    """Verify that total inflows equal total outflows."""
    inflows, outflows = nursery.water_balance()
    if inflows != outflows:
        return False, f"Water balance mismatch: inflows={inflows}, outflows={outflows}"
    return True, "Water balance OK"


def check_plot_consistency(nursery):
    """Verify that each plot's water level is consistent with its changes."""
    for plot in nursery.plots():
        level = plot.water_level
        computed = 0
        for change in plot.changes():
            if change.inflow_plot is plot:
                computed += change.amount
            elif change.outflow_plot is plot:
                computed -= change.amount
        if level != computed:
            return False, (f"Plot {plot.name!r}: water_level={level} but "
                           f"computed={computed}")
    return True, "Plot consistency OK"


def check_changelog_ids(nursery):
    """Verify that changelog entry IDs are sequential."""
    changes = nursery.changelog_entries()
    for i, change in enumerate(changes):
        expected = i + 1
        if change.id != expected:
            return False, f"Change #{change.id} at position {i} (expected #{expected})"
    return True, "Changelog IDs OK"


def check_no_duplicate_plots(nursery):
    """Verify no duplicate plot names exist."""
    names = [p.name for p in nursery.plots()]
    unique = set(names)
    if len(names) != len(unique):
        duplicates = [n for n in names if names.count(n) > 1]
        return False, f"Duplicate plot names: {set(duplicates)}"
    return True, "No duplicate plots"


def run_all_checks(nursery):
    """Run all validation checks and return results."""
    checks = [
        ("Water balance", check_water_balance),
        ("Plot consistency", check_plot_consistency),
        ("Changelog IDs", check_changelog_ids),
        ("No duplicates", check_no_duplicate_plots),
    ]
    results = []
    all_passed = True
    for name, check_fn in checks:
        passed, message = check_fn(nursery)
        results.append((name, passed, message))
        if not passed:
            all_passed = False
    return all_passed, results


if __name__ == "__main__":
    from scripts.seed_data import create_medium_nursery
    nursery = create_medium_nursery()
    passed, results = run_all_checks(nursery)
    for name, ok, msg in results:
        status = "PASS" if ok else "FAIL"
        print(f"[{status}] {name}: {msg}")
    print(f"\nOverall: {'ALL PASSED' if passed else 'SOME FAILED'}")
