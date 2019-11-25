import cirq
from cirqqulacs import QulacsSimulator
qubits = [cirq.LineQubit(i) for i in range(4)]

circuit = cirq.Circuit()

circuit.append(cirq.ops.X(qubits[0]))
circuit.append(cirq.ops.X(qubits[1]))
circuit.append(cirq.ops.X(qubits[2]))
circuit.append(cirq.ops.X(qubits[3]))
circuit.append(cirq.ops.Y(qubits[0]))

# result = cirq.Simulator().simulate(circuit)
result = QulacsSimulator().simulate(circuit)

print(circuit)
print(result.final_state)
