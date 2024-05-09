|Name|Type|Description|
|-|-|-|
|`ae`|`dict`|Amplitude Estimation (ae) circuits. The Amplitude Estimation algorithm aims to find an estimation for the amplitude of a certain quantum state. These circuits are given as a dictionary of form ae['n_qubits'].|
|`dj`|`dict`|Deutsch-Jozsa (dj) circuits. The Deutsch-Jozsa algorithm determines whether an unknown oracle mapping input values either to 0 or 1 is constant (always output 1 or always 0) or balanced (both outputs are equally likely). These circuits are given as a dictionary of form `dj['n_qubits']`.|
|`ghz`|`dict`|Greeenberger-Horne-Zeilinger (ghz) state preparation circuits. The Greenberger-Horne-Zeilinger state is an entangled quantum state with a certain type of entanglement. These circuits are given as a dictionary of form `ghz['n_qubits']`.|
|`graphstate`|`dict`|Graph state preparation circuits.  Graph states in quantum computing represent a graph with vertices and edges through a quantum circuit. These circuits are given as a dictionary of form `graphstate['n_qubits']`|
|`groundstate`|`dict`|Ground state preparation circuits. A famous application of quantum computing, specifically of VQE algorithms is the ground state estimation of molecules. Here, we provide two different molecules, H2 (4 qubits) and LiH (12 qubits), and estimate their ground state using VQE with a TwoLocal ansatz. These circuits are given as a dictionary of form `groundstate['n_qubits']`.|
|`grover-noancilla`|`dict`|Grover's algorithm circuits without ancilla. One of the most famous quantum algorithms known so far, Grover's algorithm finds a certain goal quantum state determined by an oracle. In our case, the oracle is implemented by a multi-controlled Toffoli gate over all input qubits. In this no ancilla version, no ancilla qubits are used during its realization. These circuits are given as a dictionary of form `grover_noancilla['n_qubits']`.|
|`grover-v-chain`|`dict`|Grover's algorithm circuits with v-chain ancillary mode. These circuits are given as a dictionary of form `grover_v_chain['n_qubits']`.|
|`portfolioqaoa`|`dict`|QAOA circuits for portfolio optimization. This algorithm solves the mean-variance portfolio optimization problem for different assets. In this case, a QAOA algorithm instance is used. These circuits are given as a dictionary of form `portfolioqaoa['n_qubits']`.|
|`portfoliovqe`|`dict`|VQE circuits for portfolio optimization. This algorithm solves the mean-variance portfolio optimization problem for different assets. In this case, a VQE algorithm instance is used. These circuits are given as a dictionary of form `portfoliovqe['n_qubits']`.|
|`pricingcall`|`dict`|Pricing call option circuits. This algorithm estimates the fair price of a European call option using iterative amplitude estimation. These circuits are given as a dictionary of form `pricingcall['n_qubits']`.|
|`pricingput`|`dict`|Pricing put option circuits.   This algorithm estimates the fair price of a European put option using iterative amplitude estimation. These circuits are given as a dictionary of form `pricingput['n_qubits']`.|
|`qaoa`|`dict`|Quantum Approximate Optimization Algorithm (QAOA) circuits. One of the most famous algorithms from the algorithmic class of variational quantum algorithms. It is a parameterizable quantum algorithm to solve optimization problems. Here, it solves a max-cut problem instance. These circuits are given as a dictionary of form `qaoa['n_qubits']`.|
|`qft`|`dict`|Quantum Fourier Transform (QFT) circuits. QFT embodies the quantum equivalent of the discrete Fourier transform and is a very important building block in many quantum algorithms. These circuits are given as a dictionary of form `qft['n_qubits']`.|
|`qftentangled`|`dict`|Entangled QFT circuits. Applies regular QFT to entangled qubits. These circuits are given as a dictionary of form `qft['n_qubits']`.|
|`qnn`|`dict`|Quantum Neural Network (QNN) circuits. This algorithm class is the quantum equivalent of classical Neural Networks. These circuits are given as a dictionary of form `qnn['n_qubits']`.|
|`qpeexact`|`dict`|Quantum Phase Estimation (QPE) exact circuits. QPE estimates the phase of a quantum operation and is a very important building block in many quantum algorithms. In the exact case, the applied phase is exactly representable by the number of qubits. These circuits are given as a dictionary of form `qpeexact['n_qubits']`.|
|`qpeinexact`|`dict`|Quantum Phase Estimation (QPE) inexact circuits. Similar to QPE exact, with the difference that the applied phase is not exactly representable by the number of qubits. These circuits are given as a dictionary of form `qpeinexact['n_qubits']`.|
|`qwalk-noancilla`|`dict`|Quantum Walk (no ancilla) circuits. Quantum walks are the quantum equivalent of classical random walks. In this no ancilla version, no ancilla qubits are used during its realization. These circuits are given as a dictionary of form `qwalk_noancilla['n_qubits']`|
|`qwalk-v-chain`|`dict`|Quantum Walk (v-chain) circuits. Similar to the Quantum Walk (no ancilla) algorithm, with the difference that the ancillary mode is a v-chain in this algorithm. These circuits are given as a dictionary of form `qwalk_v_chain['n_qubits']`.|
|`random`|`dict`|Random circuits. This benchmark represents a random circuit that is twice as deep as wide. It considers random quantum gates with up to four qubits. These circuits are given as a dictionary of form `random['n_qubits']`.|
|`realamprandom`|`dict`|Real amplitude ansatz circuits with random parameters. VQE ansatz with randomly initialized values. These circuits are given as a dictionary of form `realamprandom['n_qubits']`|
|`routing`|`dict`|Routing circuits. This problem is similar to the travelling salesman problem with the difference, that more than one vehicle may be used to travel between those to be visited points, such that each point is visited at least once. These circuits are given as a dictionary of form `routing['n_qubits']`.|
|`shor`|`dict`|Shor's algorithm circuits. This algorithm is one of the most famous quantum algorithms and is used to find prime factors of integers. Here, we provide quantum algorithms for solving this problem for the integers 9 and 15 using a period of 4. These circuits are given as a dictionary of form `shor['n_factorized']`.|
|`su2random`|`dict`|Efficient SU2 ansatz circuits with random parameters. VQE ansatz with randomly initialized values. These circuits are given as a dictionary of form `su2random['n_qubits']`|
|`tsp`|`dict`|Travelling Salesman circuits.  The travelling salesman problem is a very prominent optimization problem of calculating the shortest path through a number of points to be visited. Here, this is formulated as a quadratic problem and solved using VQE with a TwoLocal ansatz. These circuits are given as a dictionary of form `tsp['n_qubits']`.|
|`twolocalrandom`|`dict`|Two local ansatz circuits with random parameters. VQE ansatz with randomly initialized values. These circuits are given as a dictionary of form `twolocalrandom['n_qubits']`|
|`vqe`|`dict`|Variational Quantum Eigensolver (VQE). VQE is also one of the most famous algorithms from the class of variational quantum algorithms. It is a parameterizable quantum algorithm with different possible choices of an ansatz function. Here, a TwoLocal ansatz is chosen and applied to the same max-cut problem instance as in QAOA. These circuits are given as a dictionary of form `vqe['n_qubits']`.|
|`wstate`|`dict`|W-State preparation circuits. The W state is an entangled quantum state with a certain type of entanglement. These circuits are given as a dictionary of form `wstate['n_qubits']`.|