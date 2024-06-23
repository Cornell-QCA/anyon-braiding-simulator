# Standard Library
from typing import List, Optional, Tuple

class IsingTopoCharge:
    """
    Options for the topological charge for an Ising Model anyon
    """

    Psi: 'IsingTopoCharge'
    Vacuum: 'IsingTopoCharge'
    Sigma: 'IsingTopoCharge'

    def value(self) -> int: ...
    def to_string(self) -> str: ...

class FibonacciTopoCharge:
    """
    Options for the topological charge for a Fibonacci Model anyon
    """

    Tau: 'FibonacciTopoCharge'
    Vacuum: 'FibonacciTopoCharge'

class TopoCharge:
    """
    Options for the topological charge for an anyon.
    Currently only supports Ising and Fibonacci models.
    """

    ising: Optional[IsingTopoCharge]
    fibonacci: Optional[FibonacciTopoCharge]

    def __init__(
        self, ising: Optional[IsingTopoCharge] = ..., fibonacci: Optional[FibonacciTopoCharge] = ...
    ) -> None: ...
    @staticmethod
    def from_ising(ising: IsingTopoCharge) -> 'TopoCharge': ...
    @staticmethod
    def from_fibonacci(fibonacci: FibonacciTopoCharge) -> 'TopoCharge': ...
    def is_ising(self) -> bool: ...
    def is_fibonacci(self) -> bool: ...
    def get_ising(self) -> IsingTopoCharge: ...
    def get_fibonacci(self) -> FibonacciTopoCharge: ...
    def to_string(self) -> str: ...

class Anyon:
    """
    In Topological Quantum Computing, anyons are the fundamental quasiparticles
    which enable the computation. Anyons have an associated topological charge
    given by the model used. This struct represents an anyon with a name,
    charge, and position.
    """

    name: str
    charge: TopoCharge
    position: Tuple[float, float]

    def __init__(self, name: str, charge: TopoCharge, position: Tuple[float, float]) -> None: ...
    def __str__(self) -> str: ...

class AnyonModel:
    """
    Different Anyon models that can be used to simulate the system
    """

    Ising: 'AnyonModel'
    Fibonacci: 'AnyonModel'
    Custom: 'AnyonModel'

    def __init__(self) -> None: ...

class FusionPair:
    """
    Represents a pair of anyons indices that are fused. The indices are derived
    from the relative ordering in the list of anyons stored in State.
    FusionPair is used to represent the fusion events along the fusion tree.

    When two anyons are fused, the resulting anyon carries the lower index. i.e.
    the anyon resulting from the fusion (1,2) is later referenced as 1.
    """

    anyon_1: int
    anyon_2: int

    def __init__(self, anyon_1: int, anyon_2: int) -> None: ...
    def __str__(self) -> str: ...

class Fusion:
    """
    Stores the state of the system and all fusion operations that occur in the
    fusion tree. The vector is 2D, where the outer vector represents the time
    step and the inner vector represents the fusion operations that occur at
    that time step.
    """
    def __init__(self, state: State) -> None: ...
    def verify_basis(self, basis: Basis) -> bool: ...
    def qubit_enc(self, anyon_model: AnyonModel) -> List[FusionPair]: ...
    def __str__(self) -> str: ...
    def apply_fusion(self, anyon_1: List[int], anyon_2: List[int], anyon_model: AnyonModel) -> List[int]: ...
    def verify_fusion_result(self, init_charge: TopoCharge, anyon_model: AnyonModel) -> bool: ...

class State:
    """
    Stores the overall state of the system. Use this struct to keep track of any
    common information throughout the simulation (e.g. anyons, operations,
    statevector).
    """

    anyons: List[Anyon]
    operations: List[Tuple[int, FusionPair]]

    def __init__(self) -> None: ...
    def add_anyon(self, anyon: Anyon) -> bool: ...
    def add_operation(self, time: int, operation: FusionPair) -> bool: ...

class Basis:
    """
    The basis is represented as a vector of tuples (time, FusionPair). In TQC,
    the basis is a sequence of fusion operations that occur in the fusion tree,
    and a different fusion ordering is a different basis.
    """
    def __init__(self, ops: List[Tuple[int, FusionPair]]) -> None: ...
    def verify_basis(self, anyons: int) -> bool: ...
