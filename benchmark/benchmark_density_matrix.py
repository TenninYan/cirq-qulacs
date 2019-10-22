import os
import re
import time
import random
import matplotlib.pyplot as plt
import numpy as np

import cirq
from cirqqulacs import QulacsDensityMatrixSimulator


def parse_qasm_to_CirqCircuit(input_filename, cirq_circuit, cirq_qubits):

   with open(input_filename, "r") as ifile:
       lines = ifile.readlines()

       for line in lines:
           s = re.search(r"qreg|cx|u3|u1", line)

           if s is None:
               continue

           elif s.group() == 'qreg':
               match = re.search(r"\d\d*", line)
               continue

           elif s.group() == 'cx':
               match = re.findall(r'\[\d\d*\]', line)
               c_qbit = int(match[0].strip('[]'))
               t_qbit = int(match[1].strip('[]'))
               cirq_circuit.append(cirq.ops.CNOT(cirq_qubits[c_qbit],cirq_qubits[t_qbit]))
               continue

           elif s.group() == 'u3':
               m_r = re.findall(r'[-]?\d\.\d\d*', line)
               m_i = re.findall(r'\[\d\d*\]', line)
               cirq_circuit.append(cirq.circuits.qasm_output.QasmUGate(float(m_r[0]),float(m_r[1]),float(m_r[2])).on(cirq_qubits[int(m_i[0].strip('[]'))]))
               continue

           elif s.group() == 'u1':
               m_r = re.findall(r'[-]?\d\.\d\d*', line)
               m_i = re.findall(r'\[\d\d*\]', line) 
               cirq_circuit.append(cirq.circuits.qasm_output.QasmUGate(float(m_r[0]), 0, 0).on(cirq_qubits[int(m_i[0].strip('[]'))]))
               continue


def main():

    dtype = np.complex128
    folder_path = "./result"
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)

    with open(folder_path+'/benchmark_density_matrix_qulacs_cpu.csv', 'w') as f:
        with open(folder_path+'/benchmark_density_matrix_cirq_cpu.csv', 'w') as h:
            f.write('n_qubits,n_iter,elapsed_time\n')
            h.write('n_qubits,n_iter,elapsed_time\n')
            for niter in range(10):
                for nqubits in range(5,12+1):
                    qubits = [cirq.LineQubit(i) for i in range(nqubits)]
                    circuit = cirq.Circuit()
                    parse_qasm_to_CirqCircuit('quantum_volume/quantum_volume_n{}_d8_0_{}.qasm'.format(nqubits, niter) ,circuit, qubits)

                    sim = QulacsDensityMatrixSimulator(dtype=dtype)
                    start = time.time()
                    _ = sim.simulate(circuit)
                    elapsed_time = time.time() - start
                    f.write('{},{},{}\n'.format(nqubits, niter, elapsed_time))
                    print('cpu  {},{},{}'.format(nqubits, niter, elapsed_time))
                    
                    del sim 

                    sim = cirq.DensityMatrixSimulator(dtype=dtype)
                    start = time.time()
                    _ = sim.simulate(circuit)
                    elapsed_time = time.time() - start
                    h.write('{},{},{}\n'.format(nqubits, niter, elapsed_time))
                    print('cirq {},{},{}'.format(nqubits, niter, elapsed_time))

                    del sim 



if __name__ == '__main__':
   main()
