class FusionPair:
    def __init__(self, anyon1:int, anyon2:int):
        self.first = anyon1
        self.second = anyon2

class Fusion:
    '''
    Requires: 'anyons' representing a list of 'Anyon' objects
    Requires: 'operations' represeting a list of list of 'FusionPairs' with operations[t] indicating the fusions that occur at time step t.
    Constructs: A binary indexed tree 'anyons' represented in a 2D array  
    '''
    def __init__(self: Fusion, anyons:list[Anyon], operations: list[list[FusionPair]]):
        
        self.anyons = None
        pass
    '''
    Verifies that the list 'operations' is in fact a valid tree of fusions (checks fusions are between adjacent anyons and the anyons exist)
    '''
    def _verify_operations(self, anyons:list[Anyon], operations: list[list[FusionPair]]):
        pass

    '''
    Fuses anyon1, anyon2
    Returns: All possible outcomes after fusing them, chooses outcome to use probabilistically
    '''
    def fuse(self:Fusion, anyon1: int, anyon2: int):
        pass
    
    '''
    Returns: Human-readable representation of the fusion diagram
    '''
    def __str__(self: Fusion):
        pass
    '''
    Returns: Qubit encoding implied by the current anyon fusions
    '''
    def qubit_enc(self: Fusion):
        pass
    '''
    Returns: All possible outcomes that could occur after fusing anyon1 and anyon2.
    Does not affect current state of anyons
    '''
    def soft_fuse(self:  Fusion, anyon1: int, anyon2: int):
        pass
    
    
