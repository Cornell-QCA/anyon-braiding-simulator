import numpy as np
from anyon_braiding_simulator import State, Model, AnyonModel

class Braid:
    def __init__(self, state: State, model_type: AnyonModel):
        """
        Parameters:
        state (State): The state of the system containing anyons and fusion operations
        model_type (AnyonModel): Model to use for the braid simulation
        """
        self.state = state
        self.anyons = state.anyons
        self.swaps = []
        self.model = model_type

        # Check if there are fewer than 3 anyons
        if len(state.anyons) < 3:
            raise ValueError('There must be at least 3 anyons')

        # Check for duplicate anyon names
        names = [anyon.name for anyon in self.anyons]
        if len(names) != len(set(names)):
            raise ValueError('Duplicate anyon names detected')

    def swap(self, time: int, swaps: list[tuple[int, int]]) -> None:
        """
        Swaps the positions of anyons in list "anyons" based on provided swaps to occur at a given time

        Parameters:
        time (int): Time step at which the swaps are performed
        swaps (list): List of tuples where each tuple is a pair of anyon indices to swap

        Swaps only adjacent anyons
        """
        used_indices = set()  # Set to keep track of used indices

        # Make sure the swaps list is long enough for the current time
        while len(self.swaps) < time:
            self.swaps.append([])

        for swap in swaps:
            if len(swap) != 2:
                print(f'Invalid swap tuple {swap} at time {time}')
                continue
            
            index_A, index_B = swap

            # Perform the swap if indices are adjacent and not already used
            if abs(index_A - index_B) == 1 and index_A not in used_indices and index_B not in used_indices:
                self.anyons[index_A], self.anyons[index_B] = self.anyons[index_B], self.anyons[index_A]
                self.swaps[time-1].append((index_A, index_B))  # Update the swaps list
                used_indices.add(index_A)
                used_indices.add(index_B)
            else:
                print(f'The pair {swap} could not be swapped at time {time}')

    def generate_swap_matrix(self, time: int, index_A: int, index_B: int) -> np.ndarray:
        """
        Generates the swap matrix for swapping anyons at index_A and index_B at given time

        Parameters:
        - time (int): Time step at which the swap occurs
        - index_A (int): Index of anyon A to swap
        - index_B (int): Index of anyon B to swap

        Returns:
        - np.ndarray: Swap matrix F^{-1}RF or R depending on fusion tree
        """
        # Check if indices are valid
        if index_A < 0 or index_A >= len(self.anyons) or index_B < 0 or index_B >= len(self.anyons):
            raise ValueError("Invalid anyon indices")

        # Get fusion operations up to time step 'time'
        fusion_operations = self.state.operations[:time]

        # Check if index_A and index_B are adjacent in fusion operations
        if self.are_adjacent_in_fusion(fusion_operations, index_A, index_B):
            # Direct swap using R matrix
            swap_matrix = self.model._r_mtx
        else:
            # Indices not adjacent, need basis transformation
            swap_matrix = np.linalg.inv(self.model._f_mtx)
            swap_matrix = np.dot(swap_matrix, self.model._r_mtx)
            swap_matrix = np.dot(swap_matrix, self.model._f_mtx)

        return swap_matrix
    
    def are_adjacent_in_fusion(self, state: State, index_A: int, index_B: int) -> bool:
        """
        Checks if two anyons at indices index_A and index_B are adjacent in fusion operations

        Parameters:
        - fusion_operations (list): List of fusion operations up to current time
        - index_A (int): Index of anyon A
        - index_B (int): Index of anyon B

        Returns:
        - bool: True if index_A and index_B are adjacent, False otherwise
        """
        for operations_at_time in state.operations:
            for fusion_pair in operations_at_time:
                if (fusion_pair[0] == index_A and fusion_pair[1] == index_B) or \
                   (fusion_pair[0] == index_B and fusion_pair[1] == index_A):
                    return True
        return False
    
    def __str__(self) -> str:
        """
        Prints the ASCII representation of the swaps performed.
        """
        if not self.swaps:
            print('No swaps to print')
            return ''

        # Initialize the output for each anyon
        num_anyons = len(self.anyons)
        max_time = len(self.swaps)  # Max time is now the length of the swaps list
        max_rows = max_time * 5
        output = [[' ' for _ in range(num_anyons * 5)] for _ in range(max_rows)]
        spacing = 4  # 3 spaces between cols

        # Iterate through each time step
        for time_step in range(1, max_time + 1):
            # Add '|' for non-swap columns
            for col in range(num_anyons):
                base = (time_step - 1) * 5
                # Check if the column is not involved in any swap at the current time step
                if not any(col in swap for swap in self.swaps[time_step - 1]):
                    for i in range(5):
                        output[base + i][col * spacing + 4] = '|'

            # Iterate through each swap operation at the current time step
            for index_A, index_B in self.swaps[time_step - 1]:
                base = (time_step - 1) * 5  # Base for each swap operation
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
