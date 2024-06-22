import pytest
from anyon_braiding_simulator import Anyon, IsingTopoCharge, TopoCharge


@pytest.mark.anyon
def test_anyon():
    anyon = Anyon('thisisatest', TopoCharge.from_ising(IsingTopoCharge.Psi), (1, 1))
    assert anyon.name == 'thisisatest'
    assert anyon.charge.get_ising() == IsingTopoCharge.Psi
    assert anyon.position == (1, 1)
