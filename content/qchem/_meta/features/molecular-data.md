Information regarding the molecule, including its complete classical description and the Hartree Fock state.

| Name        | Type          | Description                                                                       |
|-------------|---------------|-----------------------------------------------------------------------------------|
| `molecule` | [`Molecule`](https://docs.pennylane.ai/en/stable/code/api/pennylane.qchem.Molecule.html)          | PennyLane Molecule object containing description for the system and basis set |
| `hf_state`  | `numpy.ndarray` | Hartree-Fock state of the chemical system represented by a binary vector                   |
| `initial_state_dets` | `dict({str : numpy.ndarray})` | Slater determinants for initial states of varying quality. The keys of the dictionary denote the overlap with the ground state. The values of the dictionary are arrays of bit strings defining basis states.|
| `initial_state_coeffs` | `dict({str : numpy.ndarray})` | Coefficients of Slater determinants for initial states of varying quality. The keys of the dictionary denote the overlap with the ground state. The values of the dictionary are arrays of coefficients corresponding to the basis states in `initial_state_dets`.|