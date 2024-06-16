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

    def swap(self, time, swaps: list[tuple[int, int]]):
        """
        Swaps the positions of anyons in list "anyons" based on provided swaps to occur at a given time

        Parameters:
        time (int): Time step at which the swaps are performed
        swaps (list): List of tuples where each tuple is a pair of anyon indices to swap

        Swaps only adjacent anyons
        """
        used_indices = set()  # Set to keep track of used indices

        for swap in swaps:
            if len(swap) != 2:
                print(f'Invalid swap tuple {swap} at time {time}')
                continue

            index_A, index_B = swap

            # Perform the swap if indices are adjacent and not already used
            if abs(index_A - index_B) == 1 and index_A not in used_indices and index_B not in used_indices:
                self.anyons[index_A], self.anyons[index_B] = self.anyons[index_B], self.anyons[index_A]
                self.operations.append((time, index_A, index_B))  # Update the operations list
                used_indices.add(index_A)
                used_indices.add(index_B)
            else:
                print(f'The pair {swap} could not be swapped at time {time}')

    def __str__(self) -> str:
        """
        Prints the ASCII representation of the swaps performed
        """
        if not self.operations:
            print('No operations to print')
            return ''

        # Initialize the output for each anyon
        num_anyons = len(self.anyons)
        max_time = max([op[0] for op in self.operations])  # Maximum time value
        max_rows = max_time * 5
        output = [[' ' for _ in range(num_anyons * 5)] for _ in range(max_rows)]
        spacing = 4  # 3 spaces between cols

        # Iterate through each time step
        for time_step in range(1, max_time + 1):
            # Add '|' for non-swap columns
            for col in range(num_anyons):
                base = (time_step - 1) * 5
                # Check if the column is not involved in any swap at the current time step
                if not any(col in swap[1:3] and swap[0] == time_step for swap in self.operations):
                    for i in range(5):
                        output[base + i][col * spacing + 4] = '|'

            # Iterate through each swap operation at the current time step
            for time, index_A, index_B in [op for op in self.operations if op[0] == time_step]:
                base = (time - 1) * 5  # Base for each swap operation
                if index_A < index_B:
                    for i in range(3):
                        output[base + i][index_A * spacing + 4 + i] = '\\'
                        output[base + i][index_B * spacing + 4 - i] = '/'
                    for i in range(3, 5):
                        output[base + i][index_A * spacing + 4 + (5 - i - 1)] = '/'
                        output[base + i][index_B * spacing + 4 - (5 - i - 1)] = '\\'
                    output[base + 2][index_A * spacing + 4 + 2] = '\\'

                else:
                    for i in range(3):
                        output[base + i][index_B * spacing + 4 + i] = '\\'
                        output[base + i][index_A * spacing + 4 - i] = '/'
                    for i in range(3, 5):
                        output[base + i][index_B * spacing + 4 + (5 - i - 1)] = '/'
                        output[base + i][index_A * spacing + 4 - (5 - i - 1)] = '\\'

        # Convert the output grid to a string and remove trailing empty rows
        return '\n'.join([''.join(row) for row in output if any(c != ' ' for c in row)])


# Function to test __str__ after each timestep
def print_anyons_state(braid, swap_number):
    """
    Print the state of anyons before and after a swap

    Parameters:
        braid (Braid): The braid object containing the anyons and operations
        swap_number (int): The swap operation number to print
    """
    # Perform the swap operation
    if swap_number <= len(braid.operations):
        print(braid)
        anyon_names = [anyon.name for anyon in braid.anyons]
        print(f"After swap {swap_number}: [{', '.join(anyon_names)}]")
    else:
        print('Invalid swap number')
