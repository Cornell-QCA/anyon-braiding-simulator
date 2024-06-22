import pytest
import os
import sys

# Ensure correct path to import modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'anyon_braiding_simulator')))

from Braiding import Braid
from anyon_braiding_simulator import Anyon, AnyonModel, IsingTopoCharge, State


@pytest.fixture
def setup_state_and_anyons():
    model_type = AnyonModel.Ising  
    state = State()
    anyons = [
        Anyon('A', IsingTopoCharge.Psi, (1, 1)),
        Anyon('B', IsingTopoCharge.Psi, (2, 2)),
        Anyon('C', IsingTopoCharge.Psi, (3, 3)),
        Anyon('D', IsingTopoCharge.Psi, (4, 4))
    ]
    for anyon in anyons:
        state.add_anyon(anyon)
    return state, anyons, model_type

def test_braid_initialization(setup_state_and_anyons):
    state, anyons, model_type = setup_state_and_anyons
    
    # Test with valid anyons
    braid = Braid(state, model_type)
    assert len(braid.anyons) == 4
    assert len(braid.swaps) == 0

    # Test with fewer than 3 anyons
    with pytest.raises(ValueError, match='There must be at least 3 anyons'):
        state_few = State()
        for anyon in anyons[:2]:
            state_few.add_anyon(anyon)
        Braid(state_few, model_type)

    # Test with duplicate anyon names
    state_duplicate = State()
    duplicate_anyons = anyons[:]
    duplicate_anyons[3] = Anyon('A', IsingTopoCharge.Psi, (4, 4))
    for anyon in duplicate_anyons:
        state_duplicate.add_anyon(anyon)
    with pytest.raises(ValueError, match='Duplicate anyon names detected'):
        Braid(state_duplicate, model_type)

def test_braid_swap(setup_state_and_anyons):
    state, anyons, model_type = setup_state_and_anyons
    braid = Braid(state, model_type)

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
    state, anyons, model_type = setup_state_and_anyons
    braid = Braid(state, model_type)
    
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
def test_swap_operations(setup_state_and_anyons, swaps, expected):
    state, anyons, model_type = setup_state_and_anyons
    braid = Braid(state, model_type)
    braid.swap(1, swaps)
    anyon_names = [anyon.name for anyon in braid.anyons]
    assert anyon_names == expected


if __name__ == '__main__':
    pytest.main(['-v', __file__])
