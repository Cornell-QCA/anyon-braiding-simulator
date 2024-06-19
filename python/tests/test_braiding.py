# Standard Library
import os
import sys

import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'anyon_braiding_simulator')))

from Braiding import Braid

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'model')))

from anyon_braiding_simulator import Anyon, IsingTopoCharge, TopoCharge


@pytest.fixture
def setup_anyons():
    return [
        Anyon('A', TopoCharge.from_ising(IsingTopoCharge.Psi), (1, 1)),
        Anyon('B', TopoCharge.from_ising(IsingTopoCharge.Psi), (2, 2)),
        Anyon('C', TopoCharge.from_ising(IsingTopoCharge.Psi), (3, 3)),
        Anyon('D', TopoCharge.from_ising(IsingTopoCharge.Psi), (4, 4)),
    ]


@pytest.mark.braiding
def test_braid_initialization(setup_anyons):
    # Test with valid anyons
    braid = Braid(setup_anyons)
    assert len(braid.anyons) == 4
    assert len(braid.swaps) == 0

    # Test with fewer than 3 anyons
    with pytest.raises(ValueError, match='There must be at least 3 anyons'):
        Braid(setup_anyons[:2])

    # Test with duplicate anyon names
    duplicate_anyons = setup_anyons[:]
    duplicate_anyons[3] = Anyon('A', TopoCharge.from_ising(IsingTopoCharge.Psi), (4, 4))
    with pytest.raises(ValueError, match='Duplicate anyon names detected'):
        Braid(duplicate_anyons)


@pytest.mark.braiding
def test_braid_swap(setup_anyons):
    braid = Braid(setup_anyons)

    # Test valid swaps
    braid.swap(1, [(0, 1), (2, 3)])
    assert braid.anyons[0].name == 'B'
    assert braid.anyons[1].name == 'A'
    assert braid.anyons[2].name == 'D'
    assert braid.anyons[3].name == 'C'
    assert len(braid.swaps) == 2

    # Test non-adjacent swap (should not occur)
    braid.swap(2, [(0, 2)])
    assert braid.anyons[0].name == 'B'
    assert braid.anyons[1].name == 'A'
    assert braid.anyons[2].name == 'D'
    assert braid.anyons[3].name == 'C'
    assert len(braid.swaps) == 2

    # Test adjacent swap with reused indices (should not occur)
    braid.swap(3, [(1, 2), (2, 3)])
    assert braid.anyons[0].name == 'B'
    assert braid.anyons[1].name == 'D'
    assert braid.anyons[2].name == 'A'
    assert braid.anyons[3].name == 'C'
    assert len(braid.swaps) == 3


@pytest.mark.braiding
def test_braid_str(setup_anyons):
    braid = Braid(setup_anyons)

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
        '   |   |   /   \\',
    ]
    # Get string representation of the braid
    output = str(braid).strip().split('\n')

    # Assert each line matches expected
    for output_line, expected_line in zip(output, expected):
        assert output_line.strip() == expected_line.strip()


@pytest.mark.parametrize(
    'swaps, expected',
    [
        ([(0, 1)], ['B', 'A', 'C', 'D']),
        ([(1, 2)], ['A', 'C', 'B', 'D']),
        ([(2, 3)], ['A', 'B', 'D', 'C']),
        ([(0, 1), (2, 3)], ['B', 'A', 'D', 'C']),
        ([(1, 2), (2, 3)], ['A', 'C', 'B', 'D']),
        ([(0, 1), (1, 2)], ['B', 'A', 'C', 'D']),
    ],
)
@pytest.mark.braiding
def test_swap_operations(setup_anyons, swaps, expected):
    braid = Braid(setup_anyons)
    braid.swap(1, swaps)
    anyon_names = [anyon.name for anyon in braid.anyons]
    assert anyon_names == expected


"""
Need to test these two functions later (after implementing some FRF stuff)
"""


@pytest.mark.braiding
def test_apply_unitary():
    pass


@pytest.mark.braiding
def test_track_state_history():
    pass


if __name__ == '__main__':
    pytest.main(['-v', __file__])
