|Name|Type|Description|
|-|-|-|
|basis_rot_samples|list[dict]|List of samples for each grouping of the basis-rotated Hamiltonian terms|
|basis_rot_groupings|tuple[list[tensor_like], list[list[[Operation](https://docs.pennylane.ai/en/stable/code/api/pennylane.operation.Operation.html#pennylane.operation.Operation)], list[tensor_like]]]|List of grouped Hamiltonian terms obtained using [`qml.qchem.basis_rotation`](https://docs.pennylane.ai/en/stable/code/api/pennylane.qchem.basis_rotation.html)|
|dipole_op|[Hamiltonian](https://docs.pennylane.ai/en/stable/code/api/pennylane.Hamiltonian.html#pennylane.Hamiltonian)|Qubit dipole moment operators for the chemical system|
|fci_energy|float|Ground state energy of the molecule obtained from exact diagonalization|
|fci_spectrum|numpy.ndarray|First `2 × #qubits` eigenvalues obtained from exact diagonalization|
|hamiltonian|[Hamiltonian](https://docs.pennylane.ai/en/stable/code/api/pennylane.Hamiltonian.html#pennylane.Hamiltonian)|Hamiltonian of the system in the Pauli basis|
|hf_state|numpy.ndarray|Hartree-Fock state of the chemical system represented by a binary vector|
|initial_state_dets|dict|Slater determinants for initial states of varying quality|
|initial_state_coeffs|dict|Coefficients of Slater determinants for initial states of varying quality|
|molecule|[Molecule](https://docs.pennylane.ai/en/stable/code/api/pennylane.qchem.Molecule.html)|PennyLane Molecule object containing description for the system and basis set|
|number_op|[Hamiltonian](https://docs.pennylane.ai/en/stable/code/api/pennylane.Hamiltonian.html#pennylane.Hamiltonian)|Qubit operator for computing total spin 𝑆<sup>2</sup> for the chemical system|
|optimal_sector|numpy.ndarray|Eigensector of the tapered qubits that would contain the ground state|
|paulix_ops|list[[PauliX](https://docs.pennylane.ai/en/stable/code/api/pennylane.PauliX.html#pennylane.PauliX)]|Supporting PauliX ops required to build Clifford 𝑈 for tapering|
|qwc_groupings|tuple[list[tensor_like], list[list[[Operation](https://docs.pennylane.ai/en/stable/code/api/pennylane.operation.Operation.html#pennylane.operation.Operation)], list[tensor_like]]]|List of grouped qubit-wise commuting Hamiltonian terms obtained using [`qml.pauli.optimize_measurements`](https://docs.pennylane.ai/en/stable/code/api/pennylane.pauli.optimize_measurements.html)|
|qwc_samples|list[dict]|List of samples for each grouping of the qubit-wise commuting Hamiltonian terms|
|sparse_hamiltonian|scipy.sparse.csr_array|Sparse matrix representation of a Hamiltonian in the computational basis|
|spin2_op|[Hamiltonian](https://docs.pennylane.ai/en/stable/code/api/pennylane.Hamiltonian.html#pennylane.Hamiltonian)|Qubit operator for computing total spin 𝑆<sup>2</sup> for the chemical system|
|spinz_op|[Hamiltonian](https://docs.pennylane.ai/en/stable/code/api/pennylane.Hamiltonian.html#pennylane.Hamiltonian)|Qubit operator for computing total spin’s projection in 𝑍 direction|
|symmetries|list[[Hamiltonian](https://docs.pennylane.ai/en/stable/code/api/pennylane.Hamiltonian.html#pennylane.Hamiltonian)]|Symmetries required for tapering molecular Hamiltonian|
|tapered_dipole_op|[Hamiltonian](https://docs.pennylane.ai/en/stable/code/api/pennylane.Hamiltonian.html#pennylane.Hamiltonian)|Tapered dipole moment operator|
|tapered_hamiltonian|[Hamiltonian](https://docs.pennylane.ai/en/stable/code/api/pennylane.Hamiltonian.html#pennylane.Hamiltonian)|Tapered Hamiltonia|
|tapered_hf_state|numpy.ndarray|Tapered Hartree-Fock state of the molecule|
|tapered_num_op|[Hamiltonian](https://docs.pennylane.ai/en/stable/code/api/pennylane.Hamiltonian.html#pennylane.Hamiltonian)|Tapered number operator|
|tapered_spin2_op|[Hamiltonian](https://docs.pennylane.ai/en/stable/code/api/pennylane.Hamiltonian.html#pennylane.Hamiltonian)|Tapered total spin operator|
|tapered_spinz_op|[Hamiltonian](https://docs.pennylane.ai/en/stable/code/api/pennylane.Hamiltonian.html#pennylane.Hamiltonian)|Tapered spin projection operator|
|vqe_energy|float|Energy obtained from the state prepared by the optimized circuit|
|vqe_gates|list[[Operation](https://docs.pennylane.ai/en/stable/code/api/pennylane.operation.Operation.html#pennylane.operation.Operation)]|[`SingleExcitation`](https://docs.pennylane.ai/en/stable/code/api/pennylane.SingleExcitation.html#pennylane.SingleExcitation) and [`DoubleExcitation`](https://docs.pennylane.ai/en/stable/code/api/pennylane.DoubleExcitation.html#pennylane.DoubleExcitation) gates for the optimized circuit|
|vqe_params|numpy.ndarray|Optimal parameters for the gates that prepares ground state|