"""Shared fixtures for grove-ledger tests."""

import sys
import os
import pytest

# Ensure the project root is on the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from nursery import Nursery


@pytest.fixture
def empty_nursery():
    """An empty nursery with no plots."""
    return Nursery()


@pytest.fixture
def basic_nursery():
    """A nursery with three plots: roses (bed), herbs (bed), reservoir."""
    n = Nursery()
    n.create_plot("roses", "bed")
    n.create_plot("herbs", "bed")
    n.create_plot("reservoir", "reservoir")
    return n


@pytest.fixture
def funded_nursery():
    """A nursery with plots and some initial water movements."""
    n = Nursery()
    n.create_plot("roses", "bed")
    n.create_plot("herbs", "bed")
    n.create_plot("reservoir", "reservoir")
    n.irrigate("roses", "reservoir", 500, "initial fill")
    n.irrigate("herbs", "reservoir", 300, "initial fill")
    return n
