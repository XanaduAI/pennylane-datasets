This dataset contains a portion of [MQT Bench](https://arxiv.org/abs/2204.13719), a set of quantum circuits for
benchmarking quantum software tools. This dataset is provided by the [Munich Quantum Toolkit](https://mqt.readthedocs.io/en/latest/)
and the original data can be downloaded from the [authors' source](https://www.cda.cit.tum.de/mqtbench/).

**Description of the dataset**

Quantum software tools for a wide variety of design tasks on and across different levels of abstraction
are crucial for eventually realizing useful quantum applications.
This requires practical and relevant benchmarks in order for new software
tools or design automation methods to be empirically evaluated and compared
to the current state of the art. Since these tools and methods operate on and
across different levels of abstraction, it is beneficial having benchmarks consistently
available across those levels. The MQT Benchmark Library (MQT Bench) provides a single
benchmark suite which offers the same benchmark algorithms on different levels of abstractions.

This dataset contains quantum circuits for 1,938 benchmark circuits ranging from 2 up to 130 qubits.
The following algorithms are included:

- Amplitude Estimation (AE)
- Deutsch-Jozsa
- GHZ State preparation
- Graph State preparation
- Ground State preparation
- Grover's (no ancilla)
- Grover's (v-chain)
- Portfolio Optimization with QAOA
- Portfolio Optimization with VQE
- Pricing Call Option
- Pricing Put Option
- Quantum Approximation Optimization Algorithm (QAOA)
- Quantum Fourier Transformation (QFT)
- Entangled QFT
- Quantum Neural Network (QNN)
- Quantum Phase Estimation (QPE) exact
- Quantum Phase Estimation (QPE) inexact
- Quantum Walk (no ancilla)
- Quantum Walk (v-chain)
- Random Circuit
- Routing
- Shor's
- Travelling Salesman
- Variational Quantum Eigensolver (VQE)
- Efficient SU2 ansatz with Random Parameters
- Real Amplitudes ansatz with Random Parameters
- Two Local ansatz with random parameters
- W-State preparation

For more information on each, please see the *Data* tab.

**Additional details**

- The circuits for each algorithm are mostly provided in a dictionary with form: `algorithm_name['number_of_qubits']`.
- Shor's algorithm circuits have a different form: `short['number_to_factor']`.
- The available numbers of qubits can be accessed with `dictionary.keys()`.
- Not all algorithms have circuits for qubit ranges of 2 to 130. Some may have a limited number of qubits.
- Circuits with `>=20` qubits or `>=100,000` gates can be computationally expensive
  to simulate.

**Example usage**

```python
qml.data.load('other', name='mqt-bench')

dev = qml.device('default.qubit')

@qml.qnode(dev)
def circuit(ops):
    for op in ops:
        qml.apply(op)
    return qml.state()

def first_10_ae_benchmark():
    for i in range(2,12):
        circuit(temp_ds.ae[str(i)])

timeit.timeit(first_10_ae_benchmark,number=5) # time the simulation: around 2 seconds
```
