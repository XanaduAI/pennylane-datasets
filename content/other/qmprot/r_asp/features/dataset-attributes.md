## Molecular data

Basic descriptors provided to understand the aspartic acid radical molecule.

| Name            | Type       | Description                                                                 |
|-----------------|------------|-----------------------------------------------------------------------------|
| `name`          | `string`   | Full name of the molecule.                                                 |
| `mf`            | `string`   | Molecular formula of the compound.                                         |
| `cid`           | `int`    | PubChem Compound ID (CID) for the molecule.                                |
| `spin`          | `int`      | Total spin number of the molecule.                                 |
| `multiplicity`  | `int`      | Spin multiplicity of the molecule (M = 2S+1).                                  |
| `charge`        | `int`      | Electric charge of the molecule.
| `basis`         | `string`   | Basis set used for the quantum chemistry calculations.                     |
| `bond_length`   | `float`    | Specific bond length set from the coordinates in Angstroms.         |
| `symbols`       | `list[str]`| List of atomic symbols (e.g., H, C, N, O) corresponding to each atom.      |
| `coordinates`   | `list[list[float]]` | List of 3D Cartesian coordinates (x, y, z) for each atom.      |



## Resources data

Features to understand the size and complexity of the molecule.

| Name              | Type   | Description                                                                 |
|-------------------|--------|-----------------------------------------------------------------------------|
| `n_atoms`         | `int`  | Total number of atoms in the molecule.                                     |
| `n_electrons`     | `int`  | Number of electrons present in the system.                                 |
| `n_orbitals`      | `int`  | Number of molecular orbitals used in the simulation.                       |
| `n_qubits`        | `int`  | Number of qubits required to simulate the system in quantum computations.  |
| `n_coefficients`  | `int`  | Number of coefficients in the Hamiltonian or wavefunction representation.  |


## Hamiltonian data

Hamiltonian for the molecular system under Jordan-Wigner transformation and its properties.

$$
H = \sum_{p,q} h_{pq} \, c_p^\dagger c_q + \frac{1}{2} \sum_{p,q,r,s} h_{pqrs} \, c_p^\dagger c_q^\dagger c_r c_s
$$

| Name            | Type    | Description                                                                 |
|------------------|---------|-----------------------------------------------------------------------------|
| `hamiltonian_n`  | `Hamiltonian`  | Fragment of the total Hamiltonian in the Pauli basis. Each `hamiltonian_n` corresponds to a part of the full operator, which must be concatenated in numerical order (e.g., `hamiltonian`, `hamiltonian_1`, `hamiltonian_2`, ...) to reconstruct the complete Hamiltonian. This splitting is used due to the length of the full expression. |
| `energy`         | `float` | Ground state energy of the system in Hartrees, computed using the Self-Consistent Field (SCF) approach based on the Hartree-Fock method. |



