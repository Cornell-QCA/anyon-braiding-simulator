# Standard Library
from enum import Enum


class AnyonModel(Enum):
    Ising = 1
    Fibonacci = 2
    Custom = 3


class Model:
    def __init__(self, model_type: AnyonModel, num_fusion_channels=5) -> None:
        """
        Requires: 'model_type' representing the type of model being used

        """
        if model_type == AnyonModel.Ising:
            self._r_mtx = []
            self._f_mtx = []
            self._rules = []
        elif model_type == AnyonModel.Fibonacci:
            self._r_mtx = []
            self._f_mtx = []
            self._rules = []
        self._num_fusion_channels = num_fusion_channels
