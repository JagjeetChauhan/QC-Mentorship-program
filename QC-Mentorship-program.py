from qiskit import QuantumCircuit, Aer, transpile, assemble
from qiskit.visualization import plot_histogram
import numpy as np

def less_than_k(k, list_n):
    # Determine the number of qubits needed to represent the numbers in the list
    num_qubits = int(np.ceil(np.log2(max(list_n)))) + 1
    
    # Initialize a quantum circuit with num_qubits qubits
    qc = QuantumCircuit(num_qubits)
    
    # Encode the number k into binary representation on the first qubits
    binary_k = format(k, '0' + str(num_qubits) + 'b')
    for i, bit in enumerate(binary_k):
        if bit == '1':
            qc.x(i)
    
    # Create a quantum register for the list of numbers
    list_register = QuantumCircuit(num_qubits, name='list_register')
    
    # Encode the numbers from the list into binary representation
    for num in list_n:
        binary_num = format(num, '0' + str(num_qubits) + 'b')
        for i, bit in enumerate(binary_num):
            if bit == '1':
                list_register.x(i)
        list_register = list_register.to_gate()
        
    # Apply the list_register gate to the circuit
    qc.append(list_register, range(num_qubits))
    
    # Apply the quantum comparison operation
    qc.append(compare_gate(num_qubits), range(num_qubits))
    
    # Measure the result
    qc.measure_all()
    
    # Execute the circuit on a simulator
    simulator = Aer.get_backend('qasm_simulator')
    job = assemble(transpile(qc, simulator), shots=1)
    result = simulator.run(job).result()
    counts = result.get_counts()
    
    # Extract the numbers less than k from the measurement results
    less_than_k_numbers = [int(key[::-1], 2) for key in counts.keys() if key[::-1][num_qubits - 1] == '1']
    
    return less_than_k_numbers

def compare_gate(num_qubits):
    # Create a quantum circuit for comparison
    qc = QuantumCircuit(num_qubits)
    
    # Apply X gates to the qubits to flip the comparison result if k is less than the number from the list
    for i in range(num_qubits):
        qc.ccx(i, num_qubits + i, 2 * num_qubits)
        qc.cx(i, num_qubits + i)
    
    return qc.to_gate()


