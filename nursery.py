from plot import Plot
from changelog import Change, ChangeLog


class Nursery:
    """Water management nursery for garden plots.

    Every water movement is a changelog entry that adds water to one plot
    (inflow) and removes it from another (outflow) by the same amount.
    This keeps the total water balanced: total inflows always equal
    total outflows.
    """

    def __init__(self):
        self._plots = {}
        self._changelog = ChangeLog()

    def create_plot(self, name, kind="bed"):
        if name in self._plots:
            raise ValueError(f"plot {name!r} already exists")
        plot = Plot(name, kind)
        self._plots[name] = plot
        return plot

    def get_plot(self, name):
        return self._plots[name]

    def plots(self):
        return list(self._plots.values())

    def irrigate(self, inflow_name, outflow_name, amount, memo=""):
        if amount <= 0:
            raise ValueError("amount must be positive")
        inflow_plot = self._plots[inflow_name]
        outflow_plot = self._plots[outflow_name]
        change = Change(inflow_plot, outflow_plot, amount, memo)
        self._changelog.record(change)
        return change

    def changelog_entries(self):
        return self._changelog.changes()

    def water_balance(self):
        total_inflows = 0
        total_outflows = 0
        for change in self._changelog.changes():
            total_inflows += change.amount
            total_outflows += change.amount
        return total_inflows, total_outflows
