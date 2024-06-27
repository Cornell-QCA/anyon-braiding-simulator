# Standard Library
import cmath
from itertools import product

import numpy as np
from anyon_braiding_simulator import AnyonModel


class Model:
    def __init__(self, model_type: AnyonModel, num_fusion_channels=5) -> None:
        """
        Requires: 'model_type' representing the type of model being used

        The Ising, Fibonacci, and Custom models correspond to 1, 2, an 3 respectively

        The F matrix is implemented as a 6 dimensional array, with the
        first 3 indexes corresponding to the 3 lower indices of the F matrix
        (which physically correspond to the anyons being fused) and the
        4th index corresponding to the upper index of the F matrix
        (which physically corresponds to the anyon resulting from fusion)

        Indices correspond to anyon types as follows:
            0 = vacuum state/ trivial anyon
            1 = sigma
            2 = psi

        For details on notation, c.f.r. On classification of modular tensor
        categories by Rowell, Stong, and Wang
        https://www.arxiv.org/abs/0712.1377
        """
        self.model_type = model_type

        if model_type == AnyonModel.Ising:
            self._charges = {'vacuum', 'sigma', 'psi'}
            self._r_mtx = cmath.exp(-1j * np.pi / 8) * np.array([[1, 0], [0, 1j]])

            self._f_mtx = np.zeros((3, 3, 3, 3, 2, 2))

            for w, x, y, z in product(range(3), repeat=4):
                self._f_mtx[w][x][y][z] = np.identity(2)

            for i in range(3):
                self._f_mtx[1][1][1][i] = 1 / np.sqrt(2) * np.array([[1, 1], [1, -1]])
                self._f_mtx[2][1][1][i] = self._f_mtx[1][2][1][i] = self._f_mtx[1][1][2][i] = -1 * np.identity(2)
                self._f_mtx[1][2][2][i] = self._f_mtx[2][1][2][i] = self._f_mtx[2][2][1][i] = -1 * np.identity(2)

            self._rules = []

        elif model_type == AnyonModel.Fibonacci:
            self._charges = {'vacuum', 'psi'}
            self._r_mtx = np.array([[cmath.exp(4 * np.pi * 1j / 5), 0], [0, -1 * cmath.exp(2 * np.pi * 1j / 5)]])
            self._f_mtx = []
            self._rules = []
        elif model_type == AnyonModel.Custom:
            raise NotImplementedError('Custom Models not yet implemented')

        else:
            raise ValueError('Model type not recognized')

        self._num_fusion_channels = num_fusion_channels

    def get_model_type(self) -> AnyonModel:
        """
        Provides the model type
        """
        return self.model_type

    def get_charges(self) -> set:
        """
        Provide the charges that are defined in this model.
        """
        return self._charges

    def getFMatrix(self, a: str, b: str, c: str, d: str) -> np.ndarray:
        """
        Parameters
        ----------
        a : str
            name of anyon corresponding to first lower index
        b : str
            name of anyon corresponding to second lower index
        c : str
            name of anyon corresponding to third lower index
        d : str
            name of anyon corresponding to upper index

        Only the following strings are accepted as parameters:
        vacuum, sigma, psi

        Requires that all anyons used as parameters are contained with the
        given model

        For details on notation, c.f.r. On classification of modular tensor
        categories by Rowell, Stong, and Wang
        https://www.arxiv.org/abs/0712.1377

        Returns
        -------
        the F-matrix corresponding to the set of indices in the model
        """

        if self.model_type == AnyonModel.Ising:
            anyondict = {'vacuum': 0, 'sigma': 1, 'psi': 2}

        elif self.model_type == AnyonModel.Fibonacci:
            anyondict = {
                'vacuum': 0,
                'sigma': 1,
            }

        elif self.model_type == AnyonModel.Custom:
            raise NotImplementedError('Custom Models not yet implemented')

        else:
            raise ValueError('Model type not recognized')

        inputs = {a, b, c, d}

        for i in inputs:
            if i not in anyondict:
                raise ValueError('invalid anyon name')

        return self._f_mtx[anyondict[a]][anyondict[b]][anyondict[c]][anyondict[d]]

    def getFInv(self, a: str, b: str, c: str, d: str) -> np.ndarray:
        """
        Parameters
        ----------
        a : str
            name of anyon corresponding to first lower index
        b : str
            name of anyon corresponding to second lower index
        c : str
            name of anyon corresponding to third lower index
        d : str
            name of anyon corresponding to upper index

        Only the following strings are accepted as parameters:
        vacuum, sigma, psi

        Requires that all anyons used as parameters are contained with the
        given model

        For details on notation, c.f.r. On classification of modular tensor
        categories by Rowell, Stong, and Wang
        https://www.arxiv.org/abs/0712.1377

        Returns
        -------
        the Inverse F-matrix corresponding to the set of indices in the model
        """

        return np.linalg.inv(self.getFMatrix(a,b,c,d))

    def getFInvRF(self, a: str, b: str, c: str, d: str) -> np.ndarray:
        """
        Parameters
        ----------
        a : str
            name of anyon corresponding to first lower index
        b : str
            name of anyon corresponding to second lower index
        c : str
            name of anyon corresponding to third lower index
        d : str
            name of anyon corresponding to upper index

        Only the following strings are accepted as parameters:
        vacuum, sigma, psi

        Requires that all anyons used as parameters are contained with the
        given model

        For details on notation, c.f.r. On classification of modular tensor
        categories by Rowell, Stong, and Wang
        https://www.arxiv.org/abs/0712.1377

        Returns
        -------
        the matrix product of (F^-1)RF corresponding to the set of indices in the model
        """

        return self.getFInv(a,b,c,d) @ self._r_mtx @ self.getFMatrix(a,b,c,d)
