"""Irrigation scheduling and planning utilities."""

from config import SEASONAL_FACTORS


class IrrigationPlan:
    """A planned sequence of irrigation operations."""

    def __init__(self, name=""):
        self._name = name
        self._steps = []

    @property
    def name(self):
        return self._name

    def add_step(self, inflow_name, outflow_name, amount, memo=""):
        """Add an irrigation step to the plan."""
        self._steps.append({
            "inflow": inflow_name,
            "outflow": outflow_name,
            "amount": amount,
            "memo": memo,
        })

    def steps(self):
        """Return a copy of all planned steps."""
        return list(self._steps)

    def total_water(self):
        """Total water to be moved across all steps."""
        return sum(s["amount"] for s in self._steps)

    def step_count(self):
        """Number of steps in the plan."""
        return len(self._steps)

    def involves_plot(self, plot_name):
        """Check if a plot is involved in any step of the plan."""
        return any(
            s["inflow"] == plot_name or s["outflow"] == plot_name
            for s in self._steps
        )

    def __repr__(self):
        return f"IrrigationPlan(name={self._name!r}, steps={len(self._steps)})"


def create_rotation_plan(nursery, source_name, target_names, amount_each, memo=""):
    """Create a plan to irrigate from one source to multiple targets.

    Distributes water equally from the source to each target.
    """
    plan = IrrigationPlan(name=f"rotation-from-{source_name}")
    for target in target_names:
        plan.add_step(target, source_name, amount_each,
                      memo or f"rotation to {target}")
    return plan


def create_seasonal_plan(nursery, season, base_amount):
    """Create a seasonal irrigation plan adjusting amounts by season.

    Multiplies the base amount by the seasonal factor.
    """
    factor = SEASONAL_FACTORS.get(season, 1.0)
    adjusted = int(base_amount * factor)
    plan = IrrigationPlan(name=f"seasonal-{season}")
    plots = nursery.plots()
    beds = [p for p in plots if p.kind == "bed"]
    reservoirs = [p for p in plots if p.kind == "reservoir"]
    if not reservoirs:
        return plan
    source = reservoirs[0]
    for bed in beds:
        plan.add_step(bed.name, source.name, adjusted,
                      f"{season} watering")
    return plan


def execute_plan(nursery, plan):
    """Execute an irrigation plan against a nursery.

    Returns a list of (step_index, change_or_error) tuples.
    Continues executing even if individual steps fail.
    """
    results = []
    for i, step in enumerate(plan.steps()):
        try:
            change = nursery.irrigate(
                step["inflow"], step["outflow"],
                step["amount"], step["memo"],
            )
            results.append((i, change))
        except (ValueError, KeyError) as e:
            results.append((i, e))
    return results


def plan_summary(plan):
    """Generate a text summary of an irrigation plan."""
    lines = [f"Plan: {plan.name}", f"Steps: {plan.step_count()}",
             f"Total water: {plan.total_water()} units", ""]
    for i, step in enumerate(plan.steps()):
        lines.append(f"  {i + 1}. {step['inflow']} <- {step['outflow']} "
                      f"({step['amount']}) {step['memo']}")
    return "\n".join(lines)
