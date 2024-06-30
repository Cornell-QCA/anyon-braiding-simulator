from typing import List, Tuple
import numpy as np
from anyon_braiding_simulator import State, Fusion, Model

class Braid:
    def __init__(self, state: State, model: Model):
        """
        Parameters:
        - state (State): The state of the system containing anyons and fusion operations
        - model (Model): Model to use for the braid simulation
        """
        self.state = state
        self.initial_anyons = [anyon.name for anyon in state.anyons]
        self.swaps = []
        self.model = model
        self.fusion = Fusion(state)

        # Check if there are fewer than 3 anyons
        if len(state.anyons) < 3:
            raise ValueError('There must be at least 3 anyons')

        # Check for duplicate anyon names
        names = [anyon.name for anyon in self.state.anyons]
        if len(names) != len(set(names)):
            raise ValueError('Duplicate anyon names detected')

    def swap(self, swaps: List[Tuple[int, int]]) -> None:
        """
        Swaps the positions of anyons in list "anyons" based on provided swaps to occur at the present time

        Parameters:
        - swaps (list): List of tuples where each tuple is a pair of anyon indices to swap

        Swaps only adjacent anyons
        """
        time = len(self.swaps)
        self.swaps.append([])

        # Track used indices directly in the swaps list
        used_indices = set([swap for sublist in self.swaps[:time] for swap in sublist])

        for index_A, index_B in swaps:
            if len(set([index_A, index_B])) != 2:
                print(f'Invalid swap tuple ({index_A}, {index_B}) at time {time}')
                continue

            if abs(index_A - index_B) != 1:
                print(f'The pair ({index_A}, {index_B}) could not be swapped at time {time}')
                continue

            if index_A in used_indices or index_B in used_indices:
                print(f'One or both indices ({index_A}, {index_B}) are already used at time {time}')
                continue

            if len(set([index_A, index_B])) == 2 and abs(index_A - index_B) == 1 and index_A in used_indices or index_B not in used_indices:
                # Perform the swap
                self.state.swap_anyons(index_A, index_B)
                self.swaps[time].append((index_A, index_B))
                used_indices.add(index_A)
                used_indices.add(index_B)

    def swap_to_qubit(self, time: int, swap_index: int) -> int:
        """
        Determines which qubit the swap operation is acting on

        Parameters:
        - time (int): Time step at which the swap(s) are performed
        - swap_index (int): Index of the swap operation in the swaps list
        """
        # Get the swap at the desired time
        swap = self.swaps[time-1] if time > 0 else []

        # Get the indices of the swap anyons
        index_A, index_B = swap[swap_index]

        # Iterate through the qubit encoding to find the matching qubit
        for qubit_index, fusion_pair in enumerate(self.fusion.qubit_enc(self.model.model_type)):
            if {index_A, index_B} == {fusion_pair.anyon_1, fusion_pair.anyon_2}:
                return qubit_index

        # If no matching qubit is found or if indices are out of range
        return None
    
    def generate_swap_matrix(self, time: int, swap_index: int) -> np.ndarray:
        """
        Generates the swap matrix for swapping anyons at given time

        Parameters:
        - time (int): Time step at which the swap(s) are performed
        - swap_index (int): Index of the swap operation in the swaps list

        Returns:
        - np.ndarray: Swap matrix F^{-1}RF or R depending on fusion tree
        """
        # Get the indices of the anyons to swap
        index_A, index_B = self.swaps[time-1][swap_index]
        
        # Check if indices are valid
        if index_A < 0 or index_A >= len(self.state.anyons) or index_B < 0 or index_B >= len(self.state.anyons):
            raise ValueError("Invalid anyon indices")

        # Check if index_A and index_B are adjacent in fusion operations
        if self.is_direct_swap(index_A, index_B):
            # Direct swap using R matrix
            swap_matrix = self.model._r_mtx
        else:
            # Indices not adjacent, need basis transformation
            fusion_operations = self.state.operations()
            
            # Find the fusion pair that affects index_A and index_B
            fusion_pair_operation = None
            for t, operation in fusion_operations:
                if t == time:
                    if (operation.anyon_1() == index_A and operation.anyon_2() == index_B) or \
                    (operation.anyon_1() == index_B and operation.anyon_2() == index_A):
                        fusion_pair_operation = operation
                        break
            
            if fusion_pair_operation:
                # Extract names of the anyons involved
                a_name = self.state.anyons[index_A].name
                b_name = self.state.anyons[index_B].name
                c_name = self.state.anyons[fusion_pair_operation.anyon_1()].name
                d_name = self.state.anyons[fusion_pair_operation.anyon_2()].name
                
                # Call getFInvRF with the names
                swap_matrix = self.model.getFInvRF(a_name, b_name, c_name, d_name)
            else:
                raise ValueError("No valid fusion operation found")
            
        return swap_matrix

    def generate_overall_swap_matrix(self, time: int, swap_index: int) -> np.ndarray:
        """
        Returns the overall swap matrix by appropriately applying the Kroneker product with the identity to the R/FInvRF matrix at the appropriate qubits

        Parameters:
        - time (int): Time step at which the swap(s) are performed
        - swap_index (int): Index of the swap operation in the swaps list

        Returns:
        - np.ndarray: Overall swap matrix for the given time and swap index
        """
        qubit_encoding = self.fusion.qubit_enc(self.model.model_type)
        if qubit_encoding is None:
            raise ValueError("Fusion qubit encoding returned None")

        num_qubits = len(self.fusion.qubit_enc(self.model.model_type))
        overall_swap_matrix = np.eye(2**num_qubits)  # Start with identity matrix of appropriate size

        for i in range(num_qubits):
            swap_qubit_index = self.swap_to_qubit(time, swap_index)
            if i == swap_qubit_index:
                swap_matrix = self.generate_swap_matrix(time, swap_index)
                overall_swap_matrix = np.kron(overall_swap_matrix, swap_matrix)
            else:
                overall_swap_matrix = np.kron(overall_swap_matrix, np.eye(2))  # Kronecker with identity for non-involved qubits

        return overall_swap_matrix

    def is_direct_swap(self, index_A: int, index_B: int) -> bool:
        """
        Checks if two anyons at indices index_A and index_B have a fusion operation at time 1

        Parameters:
        - index_A (int): Index of anyon A
        - index_B (int): Index of anyon B

        Returns:
        - bool: True if index_A and index_B have a fusion operation at time 1, False otherwise
        """
        # Get most recent fusion operation at time step 1
        fusion_operations = self.state.operations

        # Check if anyon indices index_A and index_B are adjacent in fusion operations at time 1
        for fusion in fusion_operations:
            if fusion[0] == 1:
                if {index_A, index_B} == {fusion[1].anyon_1, fusion[1].anyon_2}:
                    return True
        
        # No fusion operation found at time 1 for the given indices
        return False

    def __str__(self) -> str:
        """
        Prints the ASCII representation of the swaps performed and the anyons before and after all swaps
        """
        if not self.swaps:
            print('No swaps to print')
            return ''

        # Initialize the output for each anyon
        num_anyons = len(self.state.anyons)
        max_time = len(self.swaps)  # Max time is now the length of the swaps list
        max_rows = max_time * 5 + 2  # Add extra rows for the names
        output = [[' ' for _ in range(num_anyons * 5)] for _ in range(max_rows)]
        spacing = 4  # 3 spaces between cols

        # Add the anyon names at the top
        for col, anyon in enumerate(self.initial_anyons):
            output[0][col * spacing + 4] = anyon[0]  # Assumes single character names

        # Iterate through each time step
        for time_step in range(1, max_time + 1):
            # Add '|' for non-swap columns
            for col in range(num_anyons):
                base = (time_step - 1) * 5 + 1  # Shift by 1 to account for names
                # Check if the column is not involved in any swap at the current time step
                if not any(col in swap for swap in self.swaps[time_step - 1]):
                    for i in range(5):
                        output[base + i][col * spacing + 4] = '|'

            # Iterate through each swap operation at the current time step
            for index_A, index_B in self.swaps[time_step - 1]:
                base = (time_step - 1) * 5 + 1  # Shift by 1 to account for names
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

        # Add the anyon names at the bottom after the final swaps
        for col, anyon in enumerate(self.state.anyons):
            name = anyon.name
            output[max_rows - 1][col * spacing + 4] = name[0]  # Assumes single character names

        # Convert the output grid to a string and remove trailing empty rows
        return '\n'.join([''.join(row) for row in output if any(c != ' ' for c in row)])