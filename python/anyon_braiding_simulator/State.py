from Anyon import Anyon
from Fusion import FusionPair


class FusionTree:
    def __init__(self, anyons: list[Anyon], operations: list[FusionPair]):
        self._anyons = anyons
        self._operations = operations


class State:
    def __init__(self, anyons: list[Anyon]):
        self._anyons = anyons
        self._operations = []
        self._fusion_tree = None

    def get_size(self) -> int:
        """
        Returns the number of anyons in the state
        """
        return len(self._anyons)

    def get_state_vec(self):
        """
        Returns the state vector
        """
        pass
