import pytest
from anyon_braiding_simulator import Anyon, IsingTopoCharge


@pytest.mark.anyon
def test_anyon():
    anyon = Anyon('thisisatest', IsingTopoCharge.Psi, (1, 1))
    assert anyon.name == 'thisisatest'
    assert anyon.charge == IsingTopoCharge.Psi
    assert anyon.position == (1, 1)
