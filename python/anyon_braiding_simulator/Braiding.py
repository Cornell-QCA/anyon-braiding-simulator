import numpy as np
from anyon_braiding_simulator import Anyon


def apply_unitary(state, unitary):
    """
    Apply unitary to a given state vector

    Parameters:
        state (numpy.ndarray): State vector to which the unitary matrix will be applied
        unitary (numpy.ndarray): Unitary matrix representing the quantum operation

    Returns:
        numpy.ndarray: Updated state vector after applying the unitary
    """
    return np.dot(unitary, state)


def track_state_history(model, initial_state, operations):
    """
    Track the state history of a state vector under a series of operations

    Parameters:
        model: Instance of the Model class containing the R and F matrices
        initial_state (numpy.ndarray): Initial state vector
        operations (list): List of operations to be applied to the state vector

    Returns:
        list: List containing the state vectors at different time steps during the evolution
    """
    state_history = [initial_state.copy()]
    state = initial_state

    # Iterate through each operation in the sequence
    for operation in operations:
        if operation == 'F':
            state = apply_unitary(state, model.F_matrix)
            state_history.append(state.copy())
        elif operation == 'R':
            state = apply_unitary(state, model.R_matrix)
            state_history.append(state.copy())
        else:
            raise ValueError('Unknown operation')

    return state_history


class Braid:
    def __init__(self, anyons: list[Anyon]):
        """
        Parameters:
        anyons (list): List of Anyon objects
        operations (list): List of operations executed
        """
        self.anyons = anyons
        self.operations = []

    def swap(self, anyon_A, anyon_B):
        """
        Swaps the positions of two adjacent anyons in list "anyons" based on their names

        Parameters:
        anyon_A (str): Name of the first anyon to swap
        anyon_B (str): Name of the second anyon to swap

        Searches for anyon with name `anyon_A` and checks if `anyon_B` is immediately next to it in the list.
        If they are adjacent, it swaps their positions.
        If they are not found or not adjacent, the function prints that the anyons could not be swapped.
        """

        # Find the index of the first anyon with name anyon_A
        index_A = next((i for i, anyon in enumerate(self.anyons) if anyon.name == anyon_A), None)

        if index_A is not None:
            # Check if the next anyon in the list is anyon_B
            if index_A + 1 < len(self.anyons) and self.anyons[index_A + 1].name == anyon_B:
                index_B = index_A + 1
            # Check if the previous anyon in the list is anyon_B
            elif index_A - 1 >= 0 and self.anyons[index_A - 1].name == anyon_B:
                index_B = index_A - 1
            else:
                index_B = None
        else:
            index_B = None

        # Perform the swap if both indices are valid and the anyons are next to each other
        if index_A is not None and index_B is not None:
            self.anyons[index_A], self.anyons[index_B] = self.anyons[index_B], self.anyons[index_A]
        else:
            print('The specified anyons could not be swapped')

    def __str__(self) -> str:
        """
        Prints the ASCII representation of the swaps performed
        """
        if not self.operations:
            print('No operations to print')
            return ''

        # Initialize the output for each anyon
        num_anyons = len(self.anyons)
        output = [['|' for _ in range(num_anyons)] for _ in range(len(self.operations) * 5)]

        # Apply each recorded operation to the output
        for step, (index_A, index_B) in enumerate(self.operations):
            base = step * 5
            if index_A < index_B:
                output[base + 0][index_A] = '\\'
                output[base + 1][index_A + 1] = '\\'
                output[base + 2][index_A + 1] = '\\'
                output[base + 3][index_A + 1] = '/'
                output[base + 4][index_A] = '/'
                output[base + 4][index_B] = '/'
                output[base + 3][index_B - 1] = '/'
                output[base + 2][index_B - 1] = '/'
                output[base + 1][index_B - 1] = '\\'
            else:
                output[base + 0][index_B] = '\\'
                output[base + 1][index_B + 1] = '\\'
                output[base + 2][index_B + 1] = '\\'
                output[base + 3][index_B + 1] = '/'
                output[base + 4][index_B] = '/'
                output[base + 4][index_A] = '/'
                output[base + 3][index_A - 1] = '/'
                output[base + 2][index_A - 1] = '/'
                output[base + 1][index_A - 1] = '\\'

        return '\n'.join([' '.join(row) for row in output])
