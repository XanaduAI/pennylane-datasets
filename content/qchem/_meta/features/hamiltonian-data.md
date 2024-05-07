Hamiltonian for the molecular system under Jordan-Wigner transformation and its properties.

| Name            | Type              | Description                                                    |
|-----------------|-------------------|----------------------------------------------------------------|
| `hamiltonian`     | [`Hamiltonian`](https://docs.pennylane.ai/en/stable/code/api/pennylane.Hamiltonian.html#pennylane.Hamiltonian) | Hamiltonian of the system in the Pauli basis                   |
| `sparse_hamiltonian` | `scipy.sparse.csr_array`     | Sparse matrix representation of a Hamiltonian in the computational basis |
| `fci_energy`   | `float`     | Ground state energy of the molecule obtained from exact diagonalization          |
| `fci_spectrum`   | `numpy.ndarray`     | First `2 × #qubits` eigenvalues obtained from exact diagonalization          |