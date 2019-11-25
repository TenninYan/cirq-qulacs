import matplotlib.pyplot as plt
import numpy as np
import csv

cmap = plt.get_cmap("tab10")

def plot(path, name,linestyle,color):
    fin = open(path)
    dat = {}
    reader = csv.reader(fin, delimiter=",")
    next(reader)
    for row in reader:
        n, _, t = row
        n = int(n)
        t = float(t)
        if n not in dat: dat[n] = []
        dat[n].append(t)
    fin.close()
    ns = []
    ts = []
    for key,value in dat.items():
        ns.append(key)
        ts.append(np.mean(value))
    plt.plot(ns,ts,linestyle=linestyle,color=color,marker='.',label=name)

plot("./result_azure_gpu_v0.1.8/benchmark_state_vector_cirq_cpu.csv", name="pure cirq cpu", linestyle='solid', color=cmap(0))
plot("./result_azure_gpu_v0.1.8_old/benchmark_state_vector_qulacs_cpu.csv", name="cirq-qulacs cpu old", linestyle='dotted', color=cmap(1))
plot("./result_azure_gpu_v0.1.8_old/benchmark_state_vector_qulacs_gpu.csv", name="cirq-qulacs gpu old", linestyle='dotted', color=cmap(2))
plot("./result_azure_gpu_v0.1.8/benchmark_state_vector_qulacs_cpu.csv", name="cirq-qulacs cpu new", linestyle='dashed', color=cmap(1))
plot("./result_azure_gpu_v0.1.8/benchmark_state_vector_qulacs_gpu.csv", name="cirq-qulacs gpu new", linestyle='dashed', color=cmap(2))
plot("./result_azure_gpu_v0.1.8_qulacs/benchmark_state_vector_qulacs_cpu.csv", name="pure qulacs cpu", linestyle='solid', color=cmap(1))
plot("./result_azure_gpu_v0.1.8_qulacs/benchmark_state_vector_qulacs_gpu.csv", name="pure qulacs gpu", linestyle='solid', color=cmap(2))
ax = plt.axes()
plt.legend()
plt.title("Bennchmark results for quantum volume circuits (depth=8)")
plt.xlabel("#qubit")
plt.ylabel("time [sec]")
plt.yscale("log")
plt.ylim(1e-5,1e3)
plt.xlim(5,25)
plt.xticks([5,10,15,20,25])
ax.yaxis.grid(color='gray', linestyle=':')
# plt.grid(color='gray', linestyle='--')
plt.savefig("result_state_vector.png")
plt.show()
