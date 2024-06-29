import pytest
from anyon_braiding_simulator.anyon_braiding_simulator import Basis, FusionPair


@pytest.fixture
def anyons():
    return 10


@pytest.mark.basis
def test_basis(anyons):
    anyons = 10
    operations = []
    for t in range(1, 10):
        operations.append((t, FusionPair(0, t)))

    assert Basis(operations).verify_basis(anyons)


@pytest.mark.basis
def test_empty_basis(anyons):
    operations = []

    assert not Basis(operations).verify_basis(anyons)


@pytest.mark.basis
def test_swapped_basis(anyons):
    operations = []
    for t in range(1, 10):
        operations.append((t, FusionPair(t, 0)))

    assert not Basis(operations).verify_basis(anyons)


@pytest.mark.basis
def test_invalid_time_basis(anyons):
    operations = []

    for t in range(1, 10):
        operations.append((1, FusionPair(0, t)))

    assert not Basis(operations).verify_basis(anyons)
