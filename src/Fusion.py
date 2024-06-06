from Anyon import Anyon


class FusionPair:
    def __init__(self, anyon1: int, anyon2: int):
        self.first = anyon1
        self.second = anyon2


class Fusion:
    def __init__(self, anyons: list[Anyon], operations: list[list[FusionPair]]):
        """
        Requires: 'anyons' representing a list of 'Anyon' objects
        Requires: 'operations' represeting a list of list of 'FusionPairs' with
        operations[t] indicating the fusions that occur at time step t.
        Constructs: A binary indexed tree 'anyons' represented in a 2D array
        """

        self.anyons = None
        pass

    def _verify_operations(self, anyons: list[Anyon], operations: list[list[FusionPair]]):
        """
        Verifies that the list 'operations' is in fact a valid tree of fusions
        (checks fusions are between adjacent anyons and the anyons exist)
        """
        pass

    def fuse(self, anyon1: int, anyon2: int):
        """
        Fuses anyon1, anyon2
        Returns: All possible outcomes after fusing them, chooses outcome to use
        probabilistically
        """
        pass

    def __str__(self) -> str:
        """
        Returns: Human-readable representation of the fusion diagram
        """
        return ''
        # pass

    def qubit_enc(self):
        """
        Returns: Qubit encoding implied by the current anyon fusions
        """
        pass

    def soft_fuse(self, anyon1: int, anyon2: int):
        """
        Returns: All possible outcomes that could occur after fusing anyon1 and
        anyon2.
        Does not affect current state of anyons
        """
        pass
