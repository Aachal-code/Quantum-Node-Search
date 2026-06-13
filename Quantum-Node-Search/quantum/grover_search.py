"""
Grover's Algorithm Implementation for quantum search.
Demonstrates quadratic speedup for unstructured search.
"""

import math
from typing import Tuple, Dict, Any
import time

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator
from qiskit.primitives import Sampler

from .oracle import QuantumOracle
from .diffusion import DiffusionOperator


class GroverSearch:
    """Implements Grover's quantum search algorithm."""
    
    def __init__(self, n_nodes: int, target: int, seed: int = 42):
        """
        Initialize Grover's algorithm.
        
        Args:
            n_nodes: Total number of nodes (N)
            target: Target node to search for
            seed: Random seed for reproducibility
        """
        self.n_nodes = n_nodes
        self.target = target
        self.seed = seed
        
        # Calculate number of qubits needed
        self.n_qubits = math.ceil(math.log2(n_nodes))
        
        # Ensure target is valid
        if target >= n_nodes:
            raise ValueError(f"Target {target} >= number of nodes {n_nodes}")
        
        # Calculate optimal number of iterations
        self.iterations = self._calculate_iterations()
    
    def _calculate_iterations(self) -> int:
        """
        Calculate optimal number of Grover iterations.
        k ≈ π/4 * √N
        
        Returns:
            Number of iterations
        """
        return round(math.pi / 4 * math.sqrt(self.n_nodes))
    
    def construct_grover_circuit(self) -> QuantumCircuit:
        """
        Construct the complete Grover circuit.
        
        Steps:
        1. Initialization: Create uniform superposition with Hadamard
        2. Apply Grover operator k times:
           a. Apply oracle (marks target state)
           b. Apply diffusion operator (amplifies amplitude)
        3. Measurement
        
        Returns:
            QuantumCircuit implementing Grover's algorithm
        """
        qc = QuantumCircuit(self.n_qubits, self.n_qubits, name='Grover')
        
        # Step 1: Initialize uniform superposition
        for i in range(self.n_qubits):
            qc.h(i)
        
        # Step 2: Apply Grover iterations
        for iteration in range(self.iterations):
            # Apply oracle - decompose it instead of appending as gate
            oracle = QuantumOracle(self.n_qubits, self.target)
            oracle_circuit = oracle.construct_oracle()
            # Decompose and append instructions directly
            for instruction in oracle_circuit.data:
                qc.append(instruction)
            
            # Apply diffusion operator - decompose it instead of appending as gate
            diffusion = DiffusionOperator(self.n_qubits)
            diffusion_circuit = diffusion.construct_diffusion_operator()
            # Decompose and append instructions directly
            for instruction in diffusion_circuit.data:
                qc.append(instruction)
        
        # Step 3: Measurement
        qc.measure(range(self.n_qubits), range(self.n_qubits))
        
        return qc
    
    def search(self, shots: int = 1000) -> Tuple[bool, int, float, Dict[str, Any]]:
        """
        Execute Grover's algorithm and return results.
        
        Args:
            shots: Number of measurement shots
            
        Returns:
            (found, measured_node, execution_time, detailed_results)
        """
        start_time = time.time()
        
        # Construct circuit
        qc = self.construct_grover_circuit()
        
        # Execute on simulator
        simulator = AerSimulator(seed_simulator=self.seed)
        job = simulator.run(qc, shots=shots)
        result = job.result()
        counts = result.get_counts(qc)
        
        execution_time = time.time() - start_time
        
        # Find most common measurement result
        most_common_bitstring = max(counts, key=counts.get)
        measured_node = int(most_common_bitstring, 2)
        
        # Calculate success probability
        success_count = counts.get(self._get_binary_representation(self.target), 0)
        success_probability = (success_count / shots) * 100
        
        # Check if target was found in top measurement
        found = measured_node == self.target
        
        details = {
            'iterations': self.iterations,
            'shots': shots,
            'success_probability': success_probability,
            'success_count': success_count,
            'all_counts': counts,
            'n_qubits': self.n_qubits,
            'complexity': f'O(√N) = O(√{self.n_nodes})'
        }
        
        return found, measured_node, execution_time, details
    
    def _get_binary_representation(self, num: int) -> str:
        """Convert number to binary representation."""
        return format(num, f'0{self.n_qubits}b')


def run_grover_search(n_nodes: int, target: int, shots: int = 1000) -> dict:
    """
    Convenience function to run Grover's algorithm.
    
    Args:
        n_nodes: Total number of nodes
        target: Target node to find
        shots: Number of measurement shots
        
    Returns:
        Dictionary with search results
    """
    grover = GroverSearch(n_nodes, target)
    found, measured, time_taken, details = grover.search(shots=shots)
    
    return {
        'found': found,
        'measured_node': measured,
        'execution_time': time_taken,
        'nodes_checked': 1,  # Quantum: conceptually checks all at once
        'grover_iterations': details['iterations'],
        'success_probability': details['success_probability'],
        'complexity': details['complexity'],
        'all_details': details
    }
