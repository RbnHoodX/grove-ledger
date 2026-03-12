"""Populate a nursery with sample data for testing and demos."""

from nursery import Nursery


def create_small_nursery():
    """Create a small nursery with 3 plots and a few irrigations."""
    n = Nursery()
    n.create_plot("roses", "bed")
    n.create_plot("herbs", "bed")
    n.create_plot("main-tank", "reservoir")
    n.irrigate("roses", "main-tank", 200, "initial fill")
    n.irrigate("herbs", "main-tank", 100, "initial fill")
    return n


def create_medium_nursery():
    """Create a medium nursery with 6 plots and multiple irrigations."""
    n = Nursery()
    n.create_plot("roses", "bed")
    n.create_plot("herbs", "bed")
    n.create_plot("vegetables", "bed")
    n.create_plot("main-tank", "reservoir")
    n.create_plot("rain-barrel", "reservoir")
    n.create_plot("north-channel", "channel")

    n.irrigate("roses", "main-tank", 500, "spring planting")
    n.irrigate("herbs", "main-tank", 300, "spring planting")
    n.irrigate("vegetables", "main-tank", 400, "spring planting")
    n.irrigate("roses", "rain-barrel", 100, "supplemental")
    n.irrigate("herbs", "rain-barrel", 50, "supplemental")
    n.irrigate("north-channel", "main-tank", 200, "redistribution")
    return n


def create_large_nursery():
    """Create a large nursery with many plots and extensive history."""
    n = Nursery()
    bed_names = ["roses", "herbs", "vegetables", "perennials",
                 "annuals", "bulbs", "ferns", "succulents"]
    for name in bed_names:
        n.create_plot(name, "bed")
    n.create_plot("main-tank", "reservoir")
    n.create_plot("rain-barrel", "reservoir")
    n.create_plot("pond", "pond")
    n.create_plot("north-channel", "channel")
    n.create_plot("south-channel", "channel")

    for bed in bed_names:
        n.irrigate(bed, "main-tank", 200, "initial fill")
    n.irrigate("pond", "main-tank", 1000, "pond fill")
    for bed in bed_names[:4]:
        n.irrigate(bed, "rain-barrel", 50, "supplemental")
    return n


if __name__ == "__main__":
    nursery = create_medium_nursery()
    print(f"Created nursery with {len(nursery.plots())} plots")
    print(f"Changelog has {len(nursery.changelog_entries())} entries")
    for p in sorted(nursery.plots(), key=lambda x: x.name):
        print(f"  {p.name} ({p.kind}): {p.water_level}")
