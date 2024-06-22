# Standard Library
import cmath

import numpy as np
import pytest
from anyon_braiding_simulator.anyon_braiding_simulator import AnyonModel
from Model import Model


@pytest.fixture
def initialize_ising():
    return Model(AnyonModel.Ising)


@pytest.mark.model
def test_r_matrix(initialize_ising):
    isingMat1 = initialize_ising._r_mtx
    isingMat2 = cmath.exp(-1j * np.pi / 8) * np.array([[1, 0], [0, 1j]])
    assert np.equal(isingMat1, isingMat2).all()


@pytest.mark.model
def test_f_matrix(initialize_ising):
    ising = initialize_ising

    # check F with all sigma subscripts yields the desired matrix
    sigma4F1 = ising.getFMatrix('sigma', 'sigma', 'sigma', 'sigma')
    sigma4F2 = 1 / np.sqrt(2) * np.array([[1, 1], [1, -1]])
    assert np.equal(sigma4F1, sigma4F2).all()

    # check other non identity matrices
    assert np.equal(ising.getFMatrix('psi', 'sigma', 'sigma', 'vacuum'), -1 * np.identity(2)).all()
    assert np.equal(ising.getFMatrix('psi', 'psi', 'sigma', 'sigma'), -1 * np.identity(2)).all()
    assert np.equal(ising.getFMatrix('sigma', 'sigma', 'psi', 'psi'), -1 * np.identity(2)).all()
    assert not np.equal(ising.getFMatrix('psi', 'sigma', 'psi', 'vacuum'), np.identity(2)).all()

    # check identity matrices
    assert np.equal(ising.getFMatrix('psi', 'psi', 'psi', 'vacuum'), np.identity(2)).all()
    assert np.equal(ising.getFMatrix('psi', 'vacuum', 'psi', 'psi'), np.identity(2)).all()
    assert np.equal(ising.getFMatrix('psi', 'psi', 'psi', 'psi'), np.identity(2)).all()
