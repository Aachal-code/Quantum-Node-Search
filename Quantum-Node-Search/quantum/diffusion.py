"""
Quantum Diffusion Operator (amplitude amplification).
Core component of Grover's algorithm.
"""

from qiskit import QuantumCircuit


class DiffusionOperator:
    """Implements the diffusion operator for Grover's algorithm."""
    
    def __init__(self, n_qubits: int):
        """
        Initialize diffusion operator.
        
        Args:
            n_qubits: Number of qubits
        """
        self.n_qubits = n_qubits
    
    def construct_diffusion_operator(self) -> QuantumCircuit:
        """
        Construct the diffusion operator D = 2|s><s| - I
        where |s> is the uniform superposition state.
        
        Decomposition:
        1. Apply Hadamard gates (H gates) to all qubits
        2. Apply X gates to all qubits (convert 0 to 1 and vice versa)
        3. Multi-controlled Z gate (phase flip on |0...0>)
        4. Apply X gates to all qubits (undo step 2)
        5. Apply Hadamard gates (undo step 1)
        
        Returns:
            QuantumCircuit representing the diffusion operator
        """
        qc = QuantumCircuit(self.n_qubits, name='diffusion')
        
        # Step 1: Hadamard on all qubits
        for i in range(self.n_qubits):
            qc.h(i)
        
        # Step 2: X on all qubits
        for i in range(self.n_qubits):
            qc.x(i)
        
        # Step 3: Multi-controlled Z gate
        self._add_multi_controlled_z(qc)
        
        # Step 4: X on all qubits (undo)
        for i in range(self.n_qubits):
            qc.x(i)
        
        # Step 5: Hadamard on all qubits (undo)
        for i in range(self.n_qubits):
            qc.h(i)
        
        return qc
    
    def _add_multi_controlled_z(self, qc: QuantumCircuit):
        """
        Add multi-controlled Z gate.
        MCZ(q0, q1, ..., q_n-1) flips phase if all qubits are 1.
        """
        if self.n_qubits == 1:
            qc.z(0)
        elif self.n_qubits == 2:
            qc.cz(0, 1)
        else:
            # For more qubits, use Hadamard-controlled X decomposition
            target_qubit = self.n_qubits - 1
            qc.h(target_qubit)
            
            # Add CX ladder
            control_qubits = list(range(self.n_qubits - 1))
            for i in range(len(control_qubits) - 1):
                qc.cx(control_qubits[i], control_qubits[i + 1])
            
            qc.cx(control_qubits[-1], target_qubit)
            
            for i in range(len(control_qubits) - 2, -1, -1):
                qc.cx(control_qubits[i], control_qubits[i + 1])
            
            qc.h(target_qubit)


def create_diffusion_operator(n_qubits: int) -> QuantumCircuit:
    """
    Convenience function to create diffusion operator.
    
    Args:
        n_qubits: Number of qubits
        
    Returns:
        QuantumCircuit implementing the diffusion operator
    """
    diffusion = DiffusionOperator(n_qubits)
    return diffusion.construct_diffusion_operator()
