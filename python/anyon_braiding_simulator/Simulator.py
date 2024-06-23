from Model import Model
from anyon_braiding_simulator import State


class Simulator:
    def __init__(self):
        """
        Creates a the simulator. In order for the simulator to be function, the
        user must first initialize the model and anyons.
        """
        self._anyons = []
        self._braid = None
        self._model = None
        self._dim_of_anyon_pos = 2  # Default is 2D anyon positions

    def update_anyons(self, is_increasing: bool, anyons: list) -> None:
        """
        Update the anyons stored in memory.

        is_increasing: bool - True if the anyons are being added, False if the
        anyons are being removed.
        anyons: list - List of anyons to add or remove.
        """

        if is_increasing:
            # Check if any anyons are being added that are already in the simulator
            for anyon in anyons:
                for anyon_in_sim in self._anyons:
                    if anyon_in_sim.name == anyon.name:
                        raise ValueError('Anyon name is already in simulator')
            self._anyons.extend(anyons)
        else:
            self._anyons = [anyon for anyon in self._anyons if anyon not in anyons]

    def set_model(self, model: Model) -> None:
        """
        Set the model for the simulator.
        """
        self._model = model

    def get_model(self) -> Model:
        """
        Get the model for the simulator.
        """
        if self._model is None:
            raise ValueError('Model has not been set')
        return self._model

    def list_anyons(self) -> list:
        """
        List the anyons currently in the simulator.
        """
        return self._anyons
    
    def get_state(self) -> State:
        """
        Initializes the state of the simulator.
        """
        state = State()
        for anyon in self._anyons:
            state.add_anyon(anyon)
        return state
        
    def get_anyon_index(self, anyon_1: str, anyon_2: str):
        """
        Get the index of two anyons from their names. 
        """
        index_A = -1
        index_B = -1
        for i, anyon in enumerate(self._anyons):
            if anyon.name == anyon_1:
                index_A = i
            if anyon.name == anyon_2:
                index_B = i
        return index_A, index_B

    def get_dim_of_anyon_pos(self) -> int:
        """
        Provides the dimension of anyon positions.
        """
        return self._dim_of_anyon_pos

    def switch_to_1D(self) -> None:
        """
        Sets the dimension of anyon positions to be 1.
        """
        self._dim_of_anyon_pos = 1

    def contains_anyon(self, anyon_name: str) -> bool:
        """
        Check if the anyon is in the simulator.
        """
        return anyon_name in [anyon.name for anyon in self._anyons]

    # waiting on other classes to be implemented
