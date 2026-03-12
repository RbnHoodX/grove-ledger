class Change:
    """A water movement entry linking two plots."""

    def __init__(self, inflow_plot, outflow_plot, amount, memo=""):
        self._id = 0
        self._inflow_plot = inflow_plot
        self._outflow_plot = outflow_plot
        self._amount = amount
        self._memo = memo

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def inflow_plot(self):
        return self._inflow_plot

    @property
    def outflow_plot(self):
        return self._outflow_plot

    @property
    def amount(self):
        return self._amount

    @property
    def memo(self):
        return self._memo

    def __repr__(self):
        return (f"Change(id={self._id}, inflow={self._inflow_plot.name!r}, "
                f"outflow={self._outflow_plot.name!r}, amount={self._amount})")


class ChangeLog:
    """Append-only log of water movement changes."""

    def __init__(self):
        self._changes = []
        self._counter = 0

    def record(self, change):
        self._counter += 1
        change.id = self._counter
        self._changes.append(change)
        change.inflow_plot._add_change(change)
        change.outflow_plot._add_change(change)
        return change

    def changes(self):
        return list(self._changes)
