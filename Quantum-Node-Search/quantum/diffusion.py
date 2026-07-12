"""
Quantum Diffusion Operator (amplitude amplification).
Core component of Grover's algorithm.
"""

from qiskit import QuantumCircuit


class DiffusionOperator:
    """Implements the diffusion operator for Grover's algorithm."""
    
    def __init__(self, n_qubits: int):
        self.n_qubits = n_qubits
    
    def construct_diffusion_operator(self) -> QuantumCircuit:
        qc = QuantumCircuit(self.n_qubits, name='diffusion')
        
        # Step 1: Hadamard on all qubits
        for i in range(self.n_qubits):
            qc.h(i)
        
        # Step 2: X on all qubits
        for i in range(self.n_qubits):
            qc.x(i)
        
        # Step 3: Multi-controlled Z
        self._apply_mcz(qc)
        
        # Step 4: X on all qubits
        for i in range(self.n_qubits):
            qc.x(i)
        
        # Step 5: Hadamard on all qubits
        for i in range(self.n_qubits):
            qc.h(i)
        
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


def create_diffusion_operator(n_qubits: int) -> QuantumCircuit:
    diffusion = DiffusionOperator(n_qubits)
    return diffusion.construct_diffusion_operator()