import pytest
from Simulator import Simulator
from anyon_braiding_simulator import Anyon, TopoCharge, IsingTopoCharge, State

@pytest.fixture
def state() -> State:
    return State()

@pytest.mark.simulator
def test_pairs_to_indices(state):
    simulator = Simulator(state)
    anyon1 = Anyon("anyon1", TopoCharge(IsingTopoCharge.Sigma), (1, 2))
    anyon2 = Anyon("anyon2", TopoCharge(IsingTopoCharge.Psi), (3, 4))
    anyon3 = Anyon("anyon3", TopoCharge(IsingTopoCharge.Vacuum), (5, 6))
    simulator.update_anyons(True, [anyon1, anyon2, anyon3])

    pairs = [("anyon1", "anyon2"), ("anyon2", "anyon3")]
    indices = simulator.pairs_to_indices(pairs)

    assert indices == [(0, 1), (1, 2)]