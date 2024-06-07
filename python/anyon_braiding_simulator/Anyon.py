class Anyon:
    def __init__(self, topo_charge, name: str, position):
        """
        Parameters:
        topo_charge (String) name of topological charge of anyon
        name (String) name of anyon
        position (Double) cartesian coordinate representation of anyon's position
        """
        self.topo_charge = topo_charge
        self.name = name
        self.position = position
