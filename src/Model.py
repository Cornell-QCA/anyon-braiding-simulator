# Standard Library
from enum import Enum
import cmath
import numpy as np

class AnyonModel(Enum):
    Ising = 1
    Fibonacci = 2
    Custom = 3


class Model:
    def __init__(self, model_type: AnyonModel, num_fusion_channels=5) -> None:
        """
        Requires: 'model_type' representing the type of model being used

        The Ising model is
        """
        if model_type == AnyonModel.Ising:
            self._r_mtx = []
            self._f_mtx = []
            self._rules = []
        elif model_type == AnyonModel.Fibonacci:
            self._r_mtx = []
            self._f_mtx = np.zeros((2,2,2,2,2,2))
            
            self._r_mtx[1,1,0,1,1,1] = 1
            self._r_mtx[0,1,1,1,1,1] = 1
            self._r_mtx[1,1,1,0,1,1] = 1
            self._r_mtx[1,0,1,1,1,1] = 1
            self._r_mtx[0,0,0,0,0,0] = 1
                            
            golden = (1 + 5 ** 0.5) / 2
            goldenInv = 1/golden
            self._r_mtx[1][1][1][1] = np.array([[goldenInv, np.sqrt(goldenInv)],[np.sqrt(goldenInv), -goldenInv]])
            self._rules = []
        self._num_fusion_channels = num_fusion_channels