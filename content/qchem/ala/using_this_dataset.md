#Reconstructing a PennyLane Hamiltonian from HDF5

This repository contains a Python script that **reconstructs a Hamiltonian** stored in an HDF5 file and rebuilds it using the **PennyLane quantum computing framework**.

## Overview

The script:
- Reads Hamiltonian chunks stored in an HDF5 file
- Parses coefficients and quantum operators
- Reconstructs the full `qml.Hamiltonian` object
- Prints the first terms of the Hamiltonian for validation

---

## How It Works

### 1️⃣ **Read the HDF5 File**
The script opens the HDF5 file and reads the stored Hamiltonian chunks:
```python
with h5py.File(input_file, "r") as f:
    for key in sorted(f.keys()):
        if "hamiltonian" in key:
            hamiltonian_chunks.append(f[key][()].decode("utf-8"))

2️⃣ Combine and Parse Hamiltonian Chunks
Chunks are merged into a single string and parsed line by line:
full_hamiltonian = "\n".join(hamiltonian_chunks)
3️⃣ Convert String Operators to PennyLane Operators
A helper function converts each string-based operator into PennyLane operators (PauliX, PauliY, PauliZ, Identity):
def string_to_operator(op_string):
    # Converts strings like 'Z(0) @ X(1)' into PennyLane operators

Example Usage
input_file = "hd5_files/gly.h5"
hamiltonian = load_hamiltonian_from_hdf5(input_file)

Sample Output
print(hamiltonian.coeffs[:5])   # First 5 coefficients
print(hamiltonian.ops[:5])      # First 5 operators
print(hamiltonian[:20])         # First 20 Hamiltonian terms

🛠 Requirements
pennylane

h5py

Python 3.8+

Install dependencies:
pip install pennylane h5py

Function Reference
load_hamiltonian_from_hdf5(input_file)
Description:
Reconstructs a PennyLane Hamiltonian from an HDF5 file.

Parameters:

input_file (str): Path to the HDF5 file.

Returns:

qml.Hamiltonian: The reconstructed Hamiltonian.

Authors
Developed by Parfait Atchade-Adelomou and Laia Coronas Sala.

Powered by: PennyLane

License
This project is licensed under the MIT License. See the LICENSE file for details.

