Threonine (*C₄H₉NO₃*) is one of the 20 essential amino acids that make up all proteins in living organisms. It is classified as a **polar** amino acid and is characterized by its **hydroxyl group** in the side chain, which enables it to form **hydrogen bonds** and participate in **protein-protein interactions**. Threonine is important for maintaining the **structural integrity** of proteins, especially in the context of **protein folding** and **enzyme activity**. It also plays a key role in the **synthesis of glycine**, **serine**, and **phospholipids**, contributing to **cellular metabolism** and **membrane function**. Additionally, threonine is involved in the **phosphorylation** of proteins, a critical regulatory mechanism for many cellular processes such as **signal transduction** and **metabolism**.

**Description of the dataset**

This dataset contains various quantum properties that represent and describe the threonine amino acid under certain conditions.  The dataset includes molecular geometries, the Hamiltonian, energies, and other descriptors that can be used to analyze the molecule’s behavior and build longer peptides.

Key features include:

- Molecular information (name, molecular formula, charge, spin, geometry, etc.)
- Resource estimation (number of atoms, electrons, orbitals, qubits and Hamiltonian coefficients to represent the molecule)
- Jordan-Wigner Hamiltonian representation
- Approximations to the ground state energy

This dataset is intended to:

- Facilitate research on relevant organic molecules by providing crucial yet computationally expensive properties—such as ground state energy and the molecular Hamiltonian—thereby accelerating advancements in quantum simulations of biomolecules.

- Enhance the characterization of larger biomolecular systems by bridging the gap between existing datasets, which are primarily focused on small molecules, and the needs of researchers working on peptides and proteins.

- Support hybrid QM/ML approaches, allowing researchers to train models that accurately and efficiently predict the properties of larger and more complex systems.

- Accelerate drug discovery and biomolecular research, as proteins are central to numerous biological and therapeutic processes.

- Enable the study of fragmentation and reassembly techniques by proposing new chemical corrections for bond formation and ensuring accurate reconstruction of molecular properties after simulation, in line with the results obtained in our latest work.


**Example Usage**

To save space, the Hamiltonian in this dataset is broken up into parts and stored as a string. In
the following example, we reconstruct a PennyLane Hamiltonian from these parts. 

```python
import pennylane as qml
coefficients = []
operators = []
hamiltonian_chunks = []

# Download the dataset and retrieve the Hamiltonian chunks
ds = qml.data.load('other', name='thr')
for key in ds.list_attributes():  # Sort the keys to preserve the correct sequence
    if "hamiltonian" in key:
        hamiltonian_chunks.append(getattr(ds, key))  # Decode bytes to string

# Combine all Hamiltonian chunks into a single string
full_hamiltonian = "".join(hamiltonian_chunks)

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
for line in full_hamiltonian.split("\n"):
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
```