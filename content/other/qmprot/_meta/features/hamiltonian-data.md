Hamiltonian for the molecular system under Jordan-Wigner transformation and its properties.

$$
H = \sum_{p,q} h_{pq} \, c_p^\dagger c_q + \frac{1}{2} \sum_{p,q,r,s} h_{pqrs} \, c_p^\dagger c_q^\dagger c_r c_s
$$

| Name            | Type    | Description                                                                 |
|------------------|---------|-----------------------------------------------------------------------------|
| `hamiltonian_n`  | `Hamiltonian`  | Fragment of the total Hamiltonian in the Pauli basis. Each `hamiltonian_n` corresponds to a part of the full operator, which must be concatenated in numerical order (e.g., `hamiltonian`, `hamiltonian_1`, `hamiltonian_2`, ...) to reconstruct the complete Hamiltonian. This splitting is used due to the length of the full expression. |
| `energy`         | `float` | Ground state energy of the system in Hartrees, computed using the Self-Consistent Field (SCF) approach based on the Hartree-Fock method. |



