from anyon_braiding_simulator import Model


class Simulator:
    def __init__(self):
        """
        Creates a the simulator. In order for the simulator to be function, the
        user must first initialize the model and anyons.
        """
        self._anyons = []
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
            self._anyons.extend(anyons)
        else:
            self._anyons = [anyon for anyon in self._anyons if anyon not in anyons]

    def set_model(self, model: Model) -> None:
        """
        Set the model for the simulator.
        """
        self._model = model

    def list_anyons(self) -> list:
        """
        List the anyons currently in the simulator.
        """
        return self._anyons

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
