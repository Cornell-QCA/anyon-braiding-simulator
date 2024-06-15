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
        # Check if there are fewer than 3 anyons
        if len(anyons) < 3:
            raise ValueError('There must be at least 3 anyons')

        # Check for duplicate anyon names
        names = [anyon.name for anyon in anyons]
        if len(names) != len(set(names)):
            raise ValueError('Duplicate anyon names detected')

        self.anyons = anyons
        self.operations = []
        self.initial_states = []

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
            self.initial_states.append([anyon.name for anyon in self.anyons])  # Record initial state before swap
            self.anyons[index_A], self.anyons[index_B] = self.anyons[index_B], self.anyons[index_A]
            self.operations.append((index_A, index_B))  # Update the operations list
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
        max_rows = len(self.operations) * 5  # Each swap occupies 5 rows
        output = [[' ' for _ in range(num_anyons * 5)] for _ in range(max_rows)]

        spacing = 4  # 3 spaces between cols

        # Add '|' for non-swap columns
        for col in range(num_anyons):
            for step, (index_A, index_B) in enumerate(self.operations):
                base = step * 5
                if col != index_A and col != index_B:
                    for i in range(5):
                        output[base + i][col * spacing + 4] = '|'

        for step, (index_A, index_B) in enumerate(self.operations):
            base = step * 5  # Base for each swap operation
            if index_A < index_B:
                for i in range(3):
                    output[base + i][index_A * spacing + 4 + i * 1] = '\\'
                    output[base + i][index_B * spacing + 4 - i * 1] = '/'
                for i in range(3, 5):
                    output[base + i][index_A * spacing + 4 + (5 - i - 1) * 1] = '/'
                    output[base + i][index_B * spacing + 4 - (5 - i - 1) * 1] = '\\'

            else:
                for i in range(3):
                    output[base + i][index_B * spacing + 4 + i * 1] = '\\'
                    output[base + i][index_A * spacing + 4 - i * 1] = '/'
                for i in range(3, 5):
                    output[base + i][index_B * spacing + 4 + (5 - i - 1) * 1] = '/'
                    output[base + i][index_A * spacing + 4 - (5 - i - 1) * 1] = '\\'

        return '\n'.join([''.join(row) for row in output if any(c != ' ' for c in row)])


# Function to test __str__ after each timestep
def print_anyons_state(braid, swap_number):
    """
    Print the state of anyons before and after a swap

    Parameters:
        braid (Braid): The braid object containing the anyons and operations
        swap_number (int): The swap operation number to print
        initial_anyons (list): The initial state of anyons before any swaps
    """
    if swap_number <= len(braid.initial_states):
        initial_anyons = braid.initial_states[swap_number - 1]
    else:
        initial_anyons = [anyon.name for anyon in braid.anyons]

    print(f"Before swap {swap_number}: [{', '.join(initial_anyons)}]")

    # Perform the swap operation
    if swap_number <= len(braid.operations):
        index_A, index_B = braid.operations[swap_number - 1]
        braid.anyons[index_A], braid.anyons[index_B] = braid.anyons[index_B], braid.anyons[index_A]
        anyon_names = [anyon.name for anyon in braid.anyons]
        print(braid)
        print(f"After swap {swap_number}: [{', '.join(anyon_names)}]")
    else:
        print('Invalid swap number')
