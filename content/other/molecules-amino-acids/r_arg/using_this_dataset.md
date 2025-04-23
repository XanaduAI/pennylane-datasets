## Molecular data

Basic descriptors provided to understand the Arginine Radical molecule.

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


---

## Resources data

Features to understand the size and complexity of the molecule.

| Name              | Type   | Description                                                                 |
|-------------------|--------|-----------------------------------------------------------------------------|
| `n_atoms`         | `int`  | Total number of atoms in the molecule.                                     |
| `n_electrons`     | `int`  | Number of electrons present in the system.                                 |
| `n_orbitals`      | `int`  | Number of molecular orbitals used in the simulation.                       |
| `n_qubits`        | `int`  | Number of qubits required to simulate the system in quantum computations.  |
| `n_coefficients`  | `int`  | Number of coefficients in the Hamiltonian or wavefunction representation.  |

---

## Hamiltonian data

Hamiltonian for the molecular system under Jordan-Wigner transformation and its properties.

$$
H = \sum_{p,q} h_{pq} \, c_p^\dagger c_q + \frac{1}{2} \sum_{p,q,r,s} h_{pqrs} \, c_p^\dagger c_q^\dagger c_r c_s
$$

| Name            | Type    | Description                                                                 |
|------------------|---------|-----------------------------------------------------------------------------|
| `hamiltonian_n`  | `Hamiltonian`  | Fragment of the total Hamiltonian in the Pauli basis. Each `hamiltonian_n` corresponds to a part of the full operator, which must be concatenated in numerical order (e.g., `hamiltonian`, `hamiltonian_1`, `hamiltonian_2`, ...) to reconstruct the complete Hamiltonian. This splitting is used due to the length of the full expression. |
| `energy`         | `float` | Ground state energy of the system in Hartrees, computed using the Self-Consistent Field (SCF) approach based on the Hartree-Fock method. |


---


# Hamiltonian Loader from HDF5

## Description
Python script to load and reconstruct quantum Hamiltonians from HDF5 files into PennyLane Hamiltonian objects.

## Features
- 🗂️ Reads Hamiltonian data stored in HDF5 chunks  
- 🔗 Reconstructs full Hamiltonian from multiple segments  
- ⚛️ Converts string operators to PennyLane objects (Pauli X/Y/Z, Identity)  
- ⊗ Handles tensor products of operators  
- 🏗️ Builds complete PennyLane Hamiltonian objects  

## Installation
```bash
pip install pennylane h5py
```

## Usage
```python
import pennylane as qml
import h5py

def load_hamiltonian_from_hdf5(input_file):
    # Initialize lists to store coefficients and operators
    coefficients = []
    operators = []
    hamiltonian_chunks = []

    # Open the HDF5 file and retrieve the Hamiltonian chunks
    with h5py.File(input_file, "r") as f:
        for key in sorted(f.keys()):  # Sort the keys to preserve the correct sequence
            if "hamiltonian" in key:
                hamiltonian_chunks.append(f[key][()].decode("utf-8"))  # Decode bytes to string

    # Combine all Hamiltonian chunks into a single string
    full_hamiltonian = "
".join(hamiltonian_chunks)

    # Helper function to convert a string representation into a PennyLane operator
    def string_to_operator(op_string):
        if "Identity" in op_string:
            return qml.Identity(0)  # Identity defaults to acting on qubit 0
        
        terms = op_string.split(" @ ")  # Separate tensor product terms
        ops = []
        
        for term in terms:
            try:
                op, wire = term.split("(")
                wire = int(wire.strip(")"))  # Extract the qubit index
                if op == "X":
                    ops.append(qml.PauliX(wire))
                elif op == "Y":
                    ops.append(qml.PauliY(wire))
                elif op == "Z":
                    ops.append(qml.PauliZ(wire))
            except ValueError:
                continue  # Skip malformed lines
        
        return qml.prod(*ops) if len(ops) > 1 else ops[0]  # Create composite operator if needed

    # Process each line of the combined Hamiltonian string
    for line in full_hamiltonian.split("
"):
        line = line.strip()
        if not line or "Coefficient" in line or "Operators" in line:
            continue  # Skip empty lines or header lines

        parts = line.split()
        
        try:
            coeff = float(parts[0])  # Extract the coefficient
            op_string = " ".join(parts[1:])  # Extract the operators
            coefficients.append(coeff)
            operators.append(string_to_operator(op_string))
        except ValueError:
            continue  # Gracefully handle conversion errors

    # Build the PennyLane Hamiltonian
    hamiltonian = qml.Hamiltonian(coefficients, operators)
    return hamiltonian

# Example usage
input_file = "hd5_files/r_arg.h5"
hamiltonian = load_hamiltonian_from_hdf5(input_file)

# Display results
print("
✅ Extracted coefficients (first 5):")
print(hamiltonian.coeffs[:5])

print("
✅ Extracted operators (first 5):")
print(hamiltonian.ops[:5])

print("
✅ Reconstructed PennyLane Hamiltonian (first 20 terms):")
print(hamiltonian[:20])
```

## API Reference
**load_hamiltonian_from_hdf5(input_file: str) -> qml.Hamiltonian**  
Reconstructs Hamiltonian from HDF5 chunks.

| Parameter   | Type | Description             |
|-------------|------|-------------------------|
| input_file  | str  | Path to HDF5 input file |
| **Returns** |      | qml.Hamiltonian object  |
