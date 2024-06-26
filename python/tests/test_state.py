import pytest
from anyon_braiding_simulator.anyon_braiding_simulator import Anyon, FusionPair, IsingTopoCharge, State, TopoCharge


@pytest.fixture
def state() -> State:
    return State()


@pytest.mark.state
def test_add_anyon(state):
    for i in range(100):
        anyon = Anyon(f'{i}', TopoCharge.from_ising(IsingTopoCharge.Sigma), (0, 0))
        state.add_anyon(anyon)

    for anyon in state.anyons:
        assert anyon.name in [f'{i}' for i in range(100)]
        assert anyon.charge.get_ising() == IsingTopoCharge.Sigma
        assert anyon.position == (0, 0)

    assert len(state.anyons) == 100


def test_add_operation(state):
    for i in range(101):
        anyon = Anyon(f'{i}', TopoCharge.from_ising(IsingTopoCharge.Sigma), (0, 0))
        state.add_anyon(anyon)

    assert state.add_operation(1, FusionPair(0, 1))
    assert state.add_operation(1, FusionPair(2, 3))

    assert not state.add_operation(1, FusionPair(1, 2))
    assert not state.add_operation(1, FusionPair(2, 4))

    assert state.add_operation(1, FusionPair(4, 5))
    assert state.add_operation(2, FusionPair(2, 4))
    assert state.add_operation(3, FusionPair(0, 2))
