Features based on 𝑍<sub>2</sub> symmetries of the molecular Hamiltonian for performing [tapering](https://docs.pennylane.ai/en/stable/code/api/pennylane.taper.html).

| Name            | Type              | Description                                                    |
|-----------------|-------------------|----------------------------------------------------------------|
| `symmetries`     | list[[`Hamiltonian`](https://docs.pennylane.ai/en/stable/code/api/pennylane.Hamiltonian.html#pennylane.Hamiltonian)] | Symmetries required for tapering molecular Hamiltonian  |
| `paulix_ops` | list[[`PauliX`](https://docs.pennylane.ai/en/stable/code/api/pennylane.PauliX.html#pennylane.PauliX)]     | Supporting PauliX ops required to build Clifford 𝑈 for tapering |
| `optimal_sector` | `numpy.ndarray`     | Eigensector of the tapered qubits that would contain the ground state |