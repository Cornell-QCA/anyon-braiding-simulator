import pytest
import os
import sys
import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'anyon_braiding_simulator')))

from Braiding import Braid
from Model import Model
from anyon_braiding_simulator import Anyon, AnyonModel, IsingTopoCharge, TopoCharge, State, FusionPair


@pytest.fixture
def setup_state_and_anyons():
    model = Model(AnyonModel.Ising)
    state = State()
    anyons = [
        Anyon('A', TopoCharge.from_ising(IsingTopoCharge.Psi), (1, 1)),
        Anyon('B', TopoCharge.from_ising(IsingTopoCharge.Psi), (2, 2)),
        Anyon('C', TopoCharge.from_ising(IsingTopoCharge.Psi), (3, 3)),
        Anyon('D', TopoCharge.from_ising(IsingTopoCharge.Psi), (4, 4))
    ]
    for anyon in anyons:
        state.add_anyon(anyon)
    return state, anyons, model

def test_braid_initialization(setup_state_and_anyons):
    state, anyons, model = setup_state_and_anyons
    
    # Test with valid anyons
    braid = Braid(state, model)
    assert len(braid.anyons) == 4
    assert len(braid.swaps) == 0

    # Test with fewer than 3 anyons
    with pytest.raises(ValueError, match='There must be at least 3 anyons'):
        state_few = State()
        for anyon in anyons[:2]:
            state_few.add_anyon(anyon)
        Braid(state_few, model)

    # Test with duplicate anyon names
    state_duplicate = State()
    duplicate_anyons = anyons[:]
    duplicate_anyons[3] = Anyon('A', TopoCharge.from_ising(IsingTopoCharge.Psi), (4, 4))
    for anyon in duplicate_anyons:
        state_duplicate.add_anyon(anyon)
    with pytest.raises(ValueError, match='Duplicate anyon names detected'):
        Braid(state_duplicate, model)

def test_braid_swap(setup_state_and_anyons):
    state, _, model = setup_state_and_anyons
    braid = Braid(state, model)

    # Test valid swaps
    braid.swap(1, [(0, 1), (2, 3)])
    assert braid.anyons[0].name == 'B'
    assert braid.anyons[1].name == 'A'
    assert braid.anyons[2].name == 'D'
    assert braid.anyons[3].name == 'C'
    assert len(braid.swaps) == 1
    assert braid.swaps[0] == [(0, 1), (2, 3)]

    # Test non-adjacent swap (should not occur)
    braid.swap(2, [(0, 2)])
    assert braid.anyons[0].name == 'B'
    assert braid.anyons[1].name == 'A'
    assert braid.anyons[2].name == 'D'
    assert braid.anyons[3].name == 'C'
    assert len(braid.swaps) == 2
    assert braid.swaps[1] == []

    # Test adjacent swap with reused indices (should not occur)
    braid.swap(3, [(1, 2), (2, 3)])
    assert braid.anyons[0].name == 'B'
    assert braid.anyons[1].name == 'D'
    assert braid.anyons[2].name == 'A'
    assert braid.anyons[3].name == 'C'
    assert len(braid.swaps) == 3
    assert braid.swaps[2] == [(1, 2)]

def test_braid_str(setup_state_and_anyons):
    state, _, model = setup_state_and_anyons
    braid = Braid(state, model)
    
    # Perform swaps
    braid.swap(1, [(0, 1), (2, 3)])
    braid.swap(2, [(1, 2)])
    braid.swap(3, [(3, 2)])

    expected = [
        '    \\   /   \\   /',
        '    \\ /     \\ /',
        '     \\       \\',
        '    / \\     / \\',
        '   /   \\   /   \\',
        '   |   \\   /   |',
        '   |    \\ /    |',
        '   |     \\     |',
        '   |    / \\    |',
        '   |   /   \\   |',
        '   |   |   \\   /',
        '   |   |    \\ /',
        '   |   |     /',
        '   |   |    / \\ ',
        '   |   |   /   \\'
    ]
    # Get string representation of the braid
    output = str(braid).strip().split('\n')

    # Assert each line matches expected
    for output_line, expected_line in zip(output, expected):
        assert output_line.strip() == expected_line.strip()

@pytest.mark.parametrize("swaps, expected", [
    ([(0, 1)], ['B', 'A', 'C', 'D']),
    ([(1, 2)], ['A', 'C', 'B', 'D']),
    ([(2, 3)], ['A', 'B', 'D', 'C']),
    ([(0, 1), (2, 3)], ['B', 'A', 'D', 'C']),
    ([(1, 2), (2, 3)], ['A', 'C', 'B', 'D']),
    ([(0, 1), (1, 2)], ['B', 'A', 'C', 'D'])
])

def test_parametrized_swaps(swaps, expected, setup_state_and_anyons):
    state, _, model = setup_state_and_anyons
    braid = Braid(state, model)

    # Perform swaps
    braid.swap(1, swaps)

    # Extract the names of anyons after swaps
    resulting_names = [anyon.name for anyon in braid.anyons]

    # Assert the result matches the expected output
    assert resulting_names == expected

@pytest.fixture
def setup_state():
    # Initialize the state with 6 anyons
    state = State()
    for i in range(6):
        state.add_anyon(Anyon(f'{i}', TopoCharge.from_ising(IsingTopoCharge.Sigma), (0, 0)))
    
    # Add fusion operations
    state.add_operation(1, FusionPair(0, 1))
    state.add_operation(1, FusionPair(2, 3))
    state.add_operation(1, FusionPair(4, 5))
    state.add_operation(2, FusionPair(2, 4))
    state.add_operation(3, FusionPair(0, 2))

    # Initialize the braid with the given state and model type
    braid = Braid(state, Model(AnyonModel.Ising))
    
    return braid

def test_qubit_enc(setup_state):
    braid = setup_state

    correct = [FusionPair(0, 1), FusionPair(2, 4), FusionPair(2, 3)]

    # Confirm qubit_enc is working as expected
    assert set(map(str, braid.fusion.qubit_enc(braid.model.model_type))) == set(map(str, correct))

def test_swap_to_qubit(setup_state):
    braid = setup_state

    # Swap (0, 1) 
    braid.swap(1, [(0, 1)])
    assert braid.swap_to_qubit(1, 0) == 0    # Verify the qubit index is 0

    # Swap (2, 3) at time 2
    braid.swap(2, [(2, 3)])
    assert braid.swap_to_qubit(2, 0) == 1    # Verify the qubit index is 1


@pytest.fixture
def setup_braid():
    state = State()
    anyons = [Anyon(f'{i}', TopoCharge.from_ising(IsingTopoCharge.Sigma), (0,0)) for i in range(6)]
    for anyon in anyons:
        state.add_anyon(anyon)
    model = Model(AnyonModel.Ising)

    state.add_operation(1, FusionPair(0, 1))
    state.add_operation(1, FusionPair(2, 3))
    state.add_operation(1, FusionPair(4, 5))
    state.add_operation(2, FusionPair(2, 4))
    state.add_operation(3, FusionPair(0, 2))

    return Braid(state, model)

def test_direct_swap(setup_braid):
    braid = setup_braid

    # Perform valid adjacent swaps
    braid.swap(1, [(0, 1)])
    assert braid.is_direct_swap(0, 1) == True

    # Perform invalid adjacent swaps
    braid.swap(2, [(2, 4)])
    assert braid.is_direct_swap(2, 4) == False

    # Perform valid non-adjacent swaps
    braid.swap(3, [(0, 2)])
    assert braid.is_direct_swap(0, 2) == False

    # Perform invalid non-adjacent swaps
    braid.swap(4, [(0, 3)])
    assert braid.is_direct_swap(0, 3) == False

def test_generate_overall_unitary(setup_braid):
    braid = setup_braid

    # Perform valid adjacent swaps
    braid.swap(1, [(0, 1)])
    unitary = braid.generate_overall_unitary(1, 0)

    # Assert the unitary matrix matches the expected matrix
    assert np.shape(unitary) == (64, 64)


if __name__ == '__main__':
    pytest.main(['-v', __file__])
