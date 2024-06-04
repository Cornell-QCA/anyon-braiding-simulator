class Simulator:
    def __init__(self):
       '''
       Creates a the simulator. In order for the simulator to be function, the
       user must first initialize the model and anyons.
       '''
       self._anyons = []
       self._model = None

    def update_anyons(self, is_increasing: bool, anyons) -> None:
        '''
        Update the anyons stored in memory.

        is_increasing: bool - True if the anyons are being added, False if the anyons are being removed.
        anyons: list - List of anyons to add or remove.
        '''
        if is_increasing:
            self._anyons.extend(anyons)
        else:
            self._anyons = [anyon for anyon in self._anyons if anyon not in anyons]

    def set_model(self, model) -> None:
        '''
        Set the model for the simulation.

        model: Model - The model to set.
        '''
        self._model = model

    # waiting on other classes to be implemented
