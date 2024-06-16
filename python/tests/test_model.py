import pytest
from anyon_braiding_simulator import AnyonModel, Model

"""
TODO: Write tests for the Model class
"""


@pytest.fixture
def setup():
    return Model(AnyonModel.Ising)
