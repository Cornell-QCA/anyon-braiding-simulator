import numpy as np
import pytest
from anyon_braiding_simulator import StateVec


@pytest.mark.state_vec
def test_state_vec():
    test_arr = np.array([1, 0], dtype=complex)
    state = StateVec(1, test_arr)
    for i in range(len(test_arr)):
        assert state.vec[i] == test_arr[i]


@pytest.mark.state_vec
def test_state_vec_norm():
    test_arr = np.array([1, 0], dtype=complex)
    state = StateVec(1, test_arr)
    assert np.linalg.norm(state.vec) == 1

    test_arr = np.array([1234 + 5j, 6], dtype=complex)
    state = StateVec(1, test_arr)
    assert np.linalg.norm(state.vec) == 1
