Quantum algorithms, represented as quantum circuits, can be used as benchmarks for assessing the performance of quantum systems.
Existing datasets, widely utilized in the field, suffer from limitations in size and versatility, leading researchers to employ randomly generated circuits.
Random circuits are, however, not representative benchmarks as they lack the inherent properties of real quantum algorithms for which the quantum systems are manufactured.
This shortage of 'useful' quantum benchmarks poses a challenge to advancing the development and comparison of quantum compilers and hardware.
This research aims to enhance the existing quantum circuit datasets by generating what is referred to as 'realistic-looking' circuits by employing the Transformer machine learning architecture.
For this purpose, KetGPT is introduced, which is a tool that generates synthetic circuits in OpenQASM language, whose structure is based on quantum circuits derived from existing quantum algorithms and follows the typical patterns of human-written algorithm-based code (e.g., order of gates and qubits).
A three-fold verification process in the research involves manual inspection and Qiskit framework execution, transformer-based classification, and structural analysis.
It demonstrates the efficacy of KetGPT in producing large amounts of additional circuits that closely align with algorithm-based structures.
Beyond benchmarking, KetGPT is envisioned to contribute substantially to AI-driven quantum compilers and systems.

**Description of the dataset**

This dataset contains 1000 output circuits generated in [KetGPT - Dataset Augmentation of Quantum Circuits using Transformers](https://arxiv.org/abs/2402.13352).
They can be used for benchmarking or training AI-driven quantum compilers and systems.

To generate this dataset, KetGPT was trained on 1112 real algorithms.
Circuits for these algorithms come from [MQT Bench](https://www.cda.cit.tum.de/mqtbench/) and can be obtained via the [MQT Bench dataset](https://pennylane.ai/datasets/other/mqt-bench).
Training algorithms include: Amplitude Estimation (AE); Deutsch-Jozsa; Graph State; GHZ State; Grover's (no ancilla); Grover's (v-chain);
Portfolio Optimization with QAOA; Portfolio Optimization with VQE; Quantum Approximation Optimization Algorithm (QAOA);
Quantum Fourier Transformation (QFT); QFT Entangled; Quantum Neural Network (QNN); Quantum Phase Estimation (QPE) exact;
Quantum Phase Estimation (QPE) inexact; Quantum Walk (no ancilla); Quantum Walk (v-chain); Variational Quantum Eigensolver (VQE);
W-State; Ground State; Pricing Call Option; Pricing Put Option.

To generate more synthetic circuits using the pre-trained KetGPT model, or to view the KetGPT tokeniser, a pre-trained classifier model,
KetGPT generated circuits in QASM format, random circuits, and the files used to train KetGPT,
please view additional files on [Kaggle](https://www.kaggle.com/datasets/boranapak/ketgpt-data/).

**Additional details**

- The number of qubits per circuit ranges between 2 and 117 qubits.
- The number of gates per circuit ranges between 6 and 903.

**Example usage**

```python
[ds] = qml.data.load("ketgpt")

@qml.qnode(qml.device('default.qubit'))
def circuit(training_circuit):

    for op in ds.circuits[0]:
        qml.apply(op)

    return qml.expval(qml.PauliZ(wires=3)) #measurement on wire 3

circuit(0) # output: tensor(0.04148455, requires_grad=True)
```
