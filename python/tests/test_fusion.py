import pytest
from anyon_braiding_simulator import Anyon, Fusion, FusionPair, IsingTopoCharge, State


@pytest.fixture
def state() -> State:
    state = State()
    for i in range(6):
        state.add_anyon(Anyon(f'{i}', IsingTopoCharge.Sigma, (0, 0)))
    return state


@pytest.mark.fusion
def test_str_1(state):
    state.add_operation(1, FusionPair(0, 1))
    state.add_operation(1, FusionPair(2, 3))
    state.add_operation(1, FusionPair(4, 5))
    state.add_operation(2, FusionPair(2, 4))
    state.add_operation(3, FusionPair(0, 2))

    fusion = Fusion(state)
    expected = '0 1 2 3 4 5 \n| | | | | | \n|─| |─| |─| \n|   |───|   \n|───|       \n|           '

    assert str(fusion) == expected


@pytest.mark.fusion
def test_apply_ising_fusion(state):
    fusion = Fusion(state)

    psi = [1, 0, 0]
    vacuum = [0, 1, 0]
    sigma = [0, 0, 1]

    assert fusion.apply_fusion(psi, psi) == vacuum
    assert fusion.apply_fusion(vacuum, vacuum) == vacuum
    assert fusion.apply_fusion(sigma, sigma) == [psi[i] + vacuum[i] for i in range(3)]

    psi_sigma = [1, 0, 1]
    assert fusion.apply_fusion(psi_sigma, psi_sigma) == [1, 2, 2]
    assert not fusion.apply_fusion(psi_sigma, psi_sigma) == [2, 1, 2]  # get owned rishi


@pytest.mark.fusion
def test_qubit_enc(state):
    state.add_operation(1, FusionPair(0, 1))
    state.add_operation(1, FusionPair(2, 3))
    state.add_operation(1, FusionPair(4, 5))
    state.add_operation(2, FusionPair(2, 4))
    state.add_operation(3, FusionPair(0, 2))

    fusion = Fusion(state)
    correct = [FusionPair(0, 1), FusionPair(2, 4), FusionPair(2, 3)]

    assert set(map(str, fusion.qubit_enc())) == set(map(str, correct))
