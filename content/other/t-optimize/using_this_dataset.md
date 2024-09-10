Benchmark circuits for T-gate optimization

**Description of the dataset**

A collection of circuits typically encountered in literature for methods that aim at optimizing the T-gate count.
Some examples

- "Polynomial-time T-depth Optimization of Clifford+T circuits via Matroid Partitioning", Matthew Amy, Dmitri Maslov, Michele Mosca, [arXiv:1303.2042](https://arxiv.org/abs/1303.2042), 2013
- "An Efficient Quantum Compiler that reduces T count", Luke Heyfron, Earl T. Campbell, [arXiv:1712.01557](https://arxiv.org/abs/1712.01557), 2017
- "Reducing T-count with the ZX-calculus", Aleks Kissinger, John van de Wetering, [arXiv:1903.10477](https://arxiv.org/abs/1903.10477), 2019
- "Quantum Circuit Optimization with AlphaTensor", Francisco J. R. Ruiz, Tuomas Laakkonen, Johannes Bausch et al, [arXiv:2402.14396](https://arxiv.org/abs/2402.14396), 2024
- "Qubit-count optimization using ZX-calculus", Vivien Vandaele, [arXiv:2407.10171](https://arxiv.org/abs/2407.10171), 2024

**Example usage**

Basic properties of the dataset:

```python
>>> [ds] = qml.data.load("other", name="opTimize")

>>> # ordered list of circuits as QuantumScript objects
>>> ds.circuits
[<QuantumScript: wires=[4, 3, 0, 2, 1], params=0>, <QuantumScript: wires=[3, 6, 9, 2, 5, 8, 1, 4, 7, 0], params=0>,..]

>>> # ordered list of names of different circuits
>>> ds.circuit_names
['mod5_4', 'vbe_adder_3', 'csla_mux_3_original', .. ]

>>> # qubit counts
>>> ds.n_wires
[5, 10, 15, 30, 24, 26, 36, 24, 14, 11, 9, 5, 7, 9, 19, 12, 15, 18, 21, 24, 27, 30, 48]

>>> # Inspect properties of circuits
>>> qscript = ds.circuits[0]
>>> qscript.specs["resources"]
wires: 5
gates: 63
depth: 48
shots: Shots(total=None)
gate_types:
{'PauliX': 1, 'Hadamard': 6, 'CNOT': 28, 'Adjoint(T)': 12, 'T': 16}
gate_sizes:
{1: 35, 2: 28}
```

Plot the circuits:

```python
>>> print(qml.drawer.tape_text(ds.circuits[0]))
4: ──X──H─╭X──T†─╭X──T─╭X──T†─╭X──T────────╭X──T†─╭X──T─╭X──T†─╭X──T──H─────╭X──H─╭X──T†─╭X──T─╭X
3: ───────╰●─────│─────╰●──T──│──╭X──T†─╭X─╰●─────│─────╰●──T──│──╭X──T†─╭X─╰●────│──────│─────│─
0: ──────────────╰●───────────╰●─╰●──T──╰●────────│────────────│──│──────│────────│──────│─────│─
2: ───────────────────────────────────────────────╰●───────────╰●─╰●──T──╰●───────╰●─────│─────╰●
1: ──────────────────────────────────────────────────────────────────────────────────────╰●──────

───T†─╭X──T──H─────╭X──H─╭X──T†─╭X──T─╭X──T†─╭X──T──H─────╭X─╭X─┤  
──────│────────────│─────│──────│─────│──────│────────────│──│──┤  
──────│────────────│─────│──────╰●────│──────╰●─╭●──T──╭●─│──╰●─┤  
───T──│──╭X──T†─╭X─╰●────│────────────│─────────│──────│──│─────┤  
──────╰●─╰●──T──╰●───────╰●───────────╰●──T─────╰X──T†─╰X─╰●────┤  
```

Retrieve gates in circuits:

```python
>>> qscript = ds.circuits[0]
>>> qscript.operations
[X(4),
 Hadamard(wires=[4]),
 CNOT(wires=[3, 4]),
 Adjoint(T(wires=[4])),
 CNOT(wires=[0, 4]),
 T(wires=[4]),
 CNOT(wires=[3, 4]),
 ...
]
```

Manipulate circuit using a [transform](https://docs.pennylane.ai/en/stable/code/qml_transforms.html)

```python
>>> [new_qscript], _ = qml.transforms.single_qubit_fusion(qscript)
>>> print(qml.drawer.tape_text(new_qscript))
4: ──Rot─╭X──Rot─╭X──Rot─╭X──Rot─╭X──Rot─────────╭X──Rot─╭X──Rot─╭X──Rot─╭X──Rot─────────╭X──Rot─╭X
3: ──────╰●──────│───────╰●──Rot─│──╭X────Rot─╭X─╰●──────│───────╰●──Rot─│──╭X────Rot─╭X─╰●──────│─
0: ──────────────╰●──────────────╰●─╰●────Rot─╰●─────────│───────────────│──│─────────│──────────│─
2: ──────────────────────────────────────────────────────╰●──────────────╰●─╰●────Rot─╰●─────────╰●
1: ────────────────────────────────────────────────────────────────────────────────────────────────

───Rot─╭X──Rot─╭X──Rot─╭X──Rot─────────╭X──Rot─╭X──Rot─╭X──Rot─╭X──Rot─╭X──Rot─────────╭X─╭X─┤  
───────│───────│───────│───────────────│───────│───────│───────│───────│───────────────│──│──┤  
───────│───────│───────│───────────────│───────│───────╰●──────│───────╰●─╭●────Rot─╭●─│──╰●─┤  
───────│───────╰●──Rot─│──╭X────Rot─╭X─╰●──────│───────────────│──────────│─────────│──│─────┤  
───────╰●──────────────╰●─╰●────Rot─╰●─────────╰●──────────────╰●──Rot────╰X────Rot─╰X─╰●────┤  
```
