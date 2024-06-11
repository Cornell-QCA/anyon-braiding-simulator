# Standard Library
from enum import Enum
import cmath
import numpy as np

class AnyonModel(Enum):
    Ising = 1
    Fibonacci = 2
    Custom = 3


class Model:
    def __init__(self, model_type: AnyonModel, num_fusion_channels=5) -> None:
        """
        Requires: 'model_type' representing the type of model being used

        The Ising, Fibonacci, and Custom models correspond to 1, 2, an 3 respectively
        
        The R matrix is implemented as a 6 dimensional array, with the 
        first 3 indexes corresponding to the 3 lower indices of the R matrix
        (which physically correspond to the anyons being fused) and the 
        4th index corresponding to the upper index of the R matrix
        (which physically corresponds to the anyon resulting from fusion)
        
        Indices correspond to anyon types as follows:
            0 = vacuum state/ trivial anyon
            1 = sigma
            2 = psi
            
        For details on notation, c.f.r. On classification of modular tensor
        categories by Rowell, Stong, and Wang
        """
        if model_type == AnyonModel.Ising:
            self._r_mtx = cmath.exp(-1j*np.pi/8)*np.array([[1,0],[0,1j]])
            
            self._f_mtx = np.zeroes(3,3,3,3,2,2)
            
            for i in range(3):
                for j in range(3):
                    for k in range(3):
                        for l in range(3):
                            self._f_mtx[i][j][k][l] = np.identity(2)
            
            for i in range(3):
                self._f_mtx[1][1][1][i] = 1/np.sqrt(2)*np.array([[1,1],[1,-1]])
                self._f_mtx[2][1][1][i] = self._f_mtx[1][2][1][i] = self._f_mtx[1][1][2][i] = -1*np.identity(2)
                self._f_mtx[1][2][2][i] = self._f_mtx[2][1][2][i] = self._f_mtx[2][2][1][i] = -1*np.identity(2)
            
            self._rules = []
        elif model_type == AnyonModel.Fibonacci:
            self._r_mtx = np.array([[cmath.exp(4*np.pi*1j/5), 0],[0, -1*cmath.exp(2*np.pi*1j/5)]])
            self._f_mtx = []
            self._rules = []
        self._num_fusion_channels = num_fusion_channels