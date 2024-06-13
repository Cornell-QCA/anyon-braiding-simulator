from anyon_braiding_simulator import Anyon, Model


class Simulator:
    def __init__(self):
        """
        Creates a the simulator. In order for the simulator to be function, the
        user must first initialize the model and anyons.
        """
        self._anyons = []
        self._model = None

    def update_anyons(self, is_increasing: bool, anyons: list(Anyon)) -> None:
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

    def contains_anyon(self, anyon_name: str) -> bool:
        """
        Check if the anyon is in the simulator.
        """
        return anyon_name in [anyon.name for anyon in self._anyons]

    # waiting on other classes to be implemented
