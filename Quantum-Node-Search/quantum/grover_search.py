"""
Grover's Algorithm Implementation for quantum search.
Demonstrates quadratic speedup for unstructured search.
"""

import math
from typing import Tuple, Dict, Any
import time

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

from .oracle import QuantumOracle
from .diffusion import DiffusionOperator


class GroverSearch:
    """Implements Grover's quantum search algorithm."""
    
    def __init__(self, n_nodes: int, target: int, seed: int = 42):
        self.n_nodes = n_nodes
        self.target = target
        self.seed = seed
        self.n_qubits = math.ceil(math.log2(n_nodes))
        
        if target >= n_nodes:
            raise ValueError(f"Target {target} >= number of nodes {n_nodes}")
        
        self.iterations = self._calculate_iterations()
    
    def _calculate_iterations(self) -> int:
        """Calculate optimal number of Grover iterations."""
        # Use actual quantum search space size (2^n_qubits), not n_nodes
        search_space_size = 2 ** self.n_qubits
        return round(math.pi / 4 * math.sqrt(search_space_size))

    def construct_grover_circuit(self) -> QuantumCircuit:
        """Construct the complete Grover circuit."""
        qc = QuantumCircuit(self.n_qubits, self.n_qubits, name='Grover')
        
        # Step 1: Initialize uniform superposition
        for i in range(self.n_qubits):
            qc.h(i)
        
        # Step 2: Apply Grover iterations
        for iteration in range(self.iterations):
            # Apply oracle
            oracle = QuantumOracle(self.n_qubits, self.target)
            oracle_circuit = oracle.construct_oracle()
            qc.compose(oracle_circuit, inplace=True)
            
            # Apply diffusion
            diffusion = DiffusionOperator(self.n_qubits)
            diffusion_circuit = diffusion.construct_diffusion_operator()
            qc.compose(diffusion_circuit, inplace=True)
        
        # Step 3: Measurement
        qc.measure(range(self.n_qubits), range(self.n_qubits))
        
        return qc
    
    def search(self, shots: int = 10) -> Tuple[bool, int, float, Dict[str, Any]]:
        """Execute Grover's algorithm and return results."""
        start_time = time.time()
        
        # Construct circuit
        qc = self.construct_grover_circuit()
        
        # Execute on simulator
        simulator = AerSimulator(seed_simulator=self.seed)
        job = simulator.run(qc, shots=shots)
        result = job.result()
        counts = result.get_counts(qc)
        
        execution_time = time.time() - start_time
        
        # Filter to only valid nodes (within n_nodes range)
        valid_counts = {}
        for bitstring, count in counts.items():
            node_value = int(bitstring, 2)
            if node_value < self.n_nodes:  # Only keep valid nodes
                valid_counts[bitstring] = count
        
        # Find most common VALID measurement result
        if valid_counts:
            most_common_bitstring = max(valid_counts, key=valid_counts.get)
            measured_node = int(most_common_bitstring, 2)
        else:
            # Fallback: find any valid result
            for bitstring, count in sorted(counts.items(), key=lambda x: x[1], reverse=True):
                node_value = int(bitstring, 2)
                if node_value < self.n_nodes:
                    measured_node = node_value
                    most_common_bitstring = bitstring
                    break
            else:
                # Last resort: return 0
                measured_node = 0
                most_common_bitstring = format(0, f'0{self.n_qubits}b')
        
        # Calculate success probability (only for valid nodes)
        target_bitstring = format(self.target, f'0{self.n_qubits}b')
        success_count = valid_counts.get(target_bitstring, 0)
        total_valid = sum(valid_counts.values()) if valid_counts else 1
        success_probability = (success_count / total_valid) * 100 if total_valid > 0 else 0
        
        # Check if target was found
        found = measured_node == self.target
        
        details = {
            'iterations': self.iterations,
            'shots': shots,
            'success_probability': success_probability,
            'success_count': success_count,
            'valid_measurements': len(valid_counts),
            'all_counts': counts,
            'valid_counts': valid_counts,
            'n_qubits': self.n_qubits,
            'complexity': f'O(√N) = O(√{self.n_nodes})'
        }
        
        return found, measured_node, execution_time, details


def run_grover_search(n_nodes: int, target: int, shots: int = 10) -> dict:
    """Convenience function to run Grover's algorithm."""
    grover = GroverSearch(n_nodes, target)
    found, measured, time_taken, details = grover.search(shots=shots)
    
    return {
        'found': found,
        'measured_node': measured,
        'execution_time': time_taken,
        'nodes_checked': 1,
        'grover_iterations': details['iterations'],
        'success_probability': details['success_probability'],
        'complexity': details['complexity'],
        'all_details': details
    }