"""
Quantum Oracle for marking the target node.
The oracle flips the phase of the target state.
"""

from qiskit import QuantumCircuit


class QuantumOracle:
    """Quantum oracle that marks the target node."""
    
    def __init__(self, n_qubits: int, target: int):
        self.n_qubits = n_qubits
        self.target = target
        self.target_bits = format(target, f'0{n_qubits}b')
    
    def construct_oracle(self) -> QuantumCircuit:
        qc = QuantumCircuit(self.n_qubits, name='oracle')
        
        # Apply X gates where target bit is 0
        for i, bit in enumerate(reversed(self.target_bits)):
            if bit == '0':
                qc.x(i)
        
        # Multi-controlled Z
        self._apply_mcz(qc)
        
        # Undo X gates
        for i, bit in enumerate(reversed(self.target_bits)):
            if bit == '0':
                qc.x(i)
        
        return qc
    
    def _apply_mcz(self, qc: QuantumCircuit):
        """Apply multi-controlled Z gate"""
        n = self.n_qubits
        
        if n == 1:
            qc.z(0)
        elif n == 2:
            qc.cz(0, 1)
        elif n == 3:
            qc.ccz(0, 1, 2)
        else:
            # For 4+ qubits
            target = n - 1
            controls = list(range(n - 1))
            
            qc.h(target)
            for i in range(len(controls) - 1):
                qc.cx(controls[i], controls[i + 1])
            qc.cx(controls[-1], target)
            for i in range(len(controls) - 2, -1, -1):
                qc.cx(controls[i], controls[i + 1])
            qc.h(target)


def create_oracle(n_qubits: int, target: int) -> QuantumCircuit:
    oracle = QuantumOracle(n_qubits, target)
    return oracle.construct_oracle()