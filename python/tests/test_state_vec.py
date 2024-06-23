import numpy as np
import pytest
from anyon_braiding_simulator.anyon_braiding_simulator import StateVec


@pytest.mark.state_vec
def test_state_vec_init():
    test_arr = np.array([1, 0], dtype=complex)
    state = StateVec(1, None)
    for i in range(len(state.vec)):
        assert state.vec[i] == test_arr[i]

    test_arr = np.array([1, 0, 0, 0], dtype=complex)
    state = StateVec(2, None)
    for i in range(len(state.vec)):
        assert state.vec[i] == test_arr[i]


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


@pytest.mark.state_vec
def test_state_vec_str():
    state_vec = StateVec(1, np.array([1, 0], dtype=complex))
    assert str(state_vec) == '[\n\t1.0 + 0.0i\n\t0.0 + 0.0i\n]'
