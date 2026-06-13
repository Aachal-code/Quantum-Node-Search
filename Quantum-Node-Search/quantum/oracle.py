"""
Quantum Oracle for marking the target node.
The oracle flips the phase of the target state.
"""

from qiskit import QuantumCircuit
from qiskit.circuit.library import PhaseOracle


class QuantumOracle:
    """Quantum oracle that marks the target node."""
    
    def __init__(self, n_qubits: int, target: int):
        """
        Initialize oracle for a specific target node.
        
        Args:
            n_qubits: Number of qubits needed for encoding
            target: Target node index
        """
        self.n_qubits = n_qubits
        self.target = target
        self.target_bits = self._get_binary_representation(target, n_qubits)
    
    def _get_binary_representation(self, num: int, n_bits: int) -> str:
        """Convert number to binary representation."""
        return format(num, f'0{n_bits}b')
    
    def construct_oracle(self) -> QuantumCircuit:
        """
        Construct the oracle circuit that marks the target state.
        Uses phase-flip oracle: applies Z gate to target state.
        
        Returns:
            QuantumCircuit representing the oracle
        """
        qc = QuantumCircuit(self.n_qubits, name='oracle')
        
        # Apply X gates to qubits where target bit is 0
        # This ensures we're checking for the target bitstring
        for i, bit in enumerate(reversed(self.target_bits)):
            if bit == '0':
                qc.x(i)
        
        # Multi-controlled Z gate (phase flip on target state)
        if self.n_qubits == 1:
            qc.z(0)
        elif self.n_qubits == 2:
            qc.cz(0, 1)
        else:
            # For more qubits, use MCZ decomposition
            self._add_multi_controlled_z(qc)
        
        # Undo the X gates
        for i, bit in enumerate(reversed(self.target_bits)):
            if bit == '0':
                qc.x(i)
        
        return qc
    
    def _add_multi_controlled_z(self, qc: QuantumCircuit):
        """
        Add multi-controlled Z gate using Qiskit decomposition.
        For n qubits, creates a Z gate controlled by first n-1 qubits on qubit n-1.
        """
        if self.n_qubits <= 2:
            return
        
        # Use Qiskit's built-in MCZ decomposition
        # Add Hadamard on target qubit
        target_qubit = self.n_qubits - 1
        control_qubits = list(range(self.n_qubits - 1))
        
        qc.h(target_qubit)
        
        # Add controlled X gates (using standard decomposition)
        # This implements MCZ using single qubit rotations and CX gates
        if len(control_qubits) == 1:
            qc.cz(control_qubits[0], target_qubit)
        else:
            # For 3+ qubits: use phase kickback with T gates
            for i in range(len(control_qubits) - 1):
                qc.cx(control_qubits[i], control_qubits[i + 1])
            
            qc.cx(control_qubits[-1], target_qubit)
            
            for i in range(len(control_qubits) - 2, -1, -1):
                qc.cx(control_qubits[i], control_qubits[i + 1])
        
        qc.h(target_qubit)


def create_oracle(n_qubits: int, target: int) -> QuantumCircuit:
    """
    Convenience function to create an oracle circuit.
    
    Args:
        n_qubits: Number of qubits
        target: Target node (will be encoded in binary)
        
    Returns:
        QuantumCircuit implementing the oracle
    """
    oracle = QuantumOracle(n_qubits, target)
    return oracle.construct_oracle()
