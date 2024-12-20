$$
H = \sum_{p,q}h_{pq}c_p^\dag c_q + \frac{1}{2}\sum_{p,q,r,s}h_{pqrs}c^\dag_pc^\dag_qc_rc_s
$$

Hamiltonian for the molecular system under Jordan-Wigner transformation and its properties.

| Name            | Type              | Description                                                    |
|-----------------|-------------------|----------------------------------------------------------------|
| `hamiltonian`     | [`Hamiltonian`](https://docs.pennylane.ai/en/stable/code/api/pennylane.Hamiltonian.html#pennylane.Hamiltonian) | Hamiltonian of the system in the Pauli basis                   |
| `sparse_hamiltonian` | `scipy.sparse.csr_array`     | Sparse matrix representation of a Hamiltonian in the computational basis |