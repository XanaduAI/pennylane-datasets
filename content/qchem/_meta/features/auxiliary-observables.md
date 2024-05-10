The supplementary operators required to obtain additional properties of the molecule such as its dipole moment, spin, etc.

| Name            | Type              | Description                                                    |
|-----------------|-------------------|----------------------------------------------------------------|
| `dipole_op`     | [`Hamiltonian`](https://docs.pennylane.ai/en/stable/code/api/pennylane.Hamiltonian.html#pennylane.Hamiltonian) | Qubit dipole moment operators for the chemical system                   |
| `number_op` | [`Hamiltonian`](https://docs.pennylane.ai/en/stable/code/api/pennylane.Hamiltonian.html#pennylane.Hamiltonian)     | Qubit particle number operator for the chemical system |
| `spin2_op` | [`Hamiltonian`](https://docs.pennylane.ai/en/stable/code/api/pennylane.Hamiltonian.html#pennylane.Hamiltonian)     | Qubit operator for computing total spin 𝑆<sup>2</sup> for the chemical system |
| `spinz_op` | [`Hamiltonian`](https://docs.pennylane.ai/en/stable/code/api/pennylane.Hamiltonian.html#pennylane.Hamiltonian)     | Qubit operator for computing total spin’s projection in 𝑍 direction |