class Plot:
    """A garden plot that tracks its water level from changelog entries.

    The water level is always computed from changes -- never stored directly.
    This guarantees the level is always consistent with the changelog.
    """

    def __init__(self, name, kind="bed"):
        self._name = name
        self._kind = kind
        self._changes = []

    @property
    def name(self):
        return self._name

    @property
    def kind(self):
        return self._kind

    @property
    def water_level(self):
        total = 0
        for change in self._changes:
            if change.inflow_plot is self:
                total += change.amount
            elif change.outflow_plot is self:
                total -= change.amount
        return total

    def _add_change(self, change):
        self._changes.append(change)

    def changes(self):
        return list(self._changes)

    def __repr__(self):
        return f"Plot(name={self._name!r}, kind={self._kind!r})"
