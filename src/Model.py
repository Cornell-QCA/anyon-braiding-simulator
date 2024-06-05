from enum import Enum
import numpy as np
import numpy.typing as npt

class AnyonModel(Enum):
    Ising = 1
    Fibonacci = 2
    Custom = 3

class Model:
    def __init__(self, r_mtx: npt.ArrayLike, f_mtx: npt.ArrayLike, rules, num_fusion_channels=5) -> None:
        '''
        
        '''
        self._r_mtx = r_mtx
        self._f_mtx = f_mtx
        self._rules = rules
        self._num_fusion_channels = num_fusion_channels
    



    