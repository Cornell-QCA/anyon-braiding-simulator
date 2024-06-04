class Simulator:
    def __init__(self):
       '''
       Creates a the simulator. In order for the simulator to be function, the
       user must first initialize the model and anyons.
       '''
       self._anyons = []
       self._model = None

