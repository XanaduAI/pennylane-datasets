|Name|Type|Description|
|-|-|-|
|`field_strengths`|`list`|Field strengths used in the transverse-field Ising Hamiltonian. The $i$-th field strength in the list corresponds to the $i$-th qubit.|
|`hamiltonian`|`pennylane.ops.qubit.hamiltonian.Hamiltonian`|Transverse-field Ising Hamiltonian for the problem studied.|
|`shadow_bases`|`list`|Pauli bases for the classical shadow measurements. The list is organized as `shadow_bases[training_state_0_or_1][measurement_instance][qubit]`. E.g. shadow_bases[0][10][3] will tell us whether qubit 3 was measured in X, Y, or Z basis for the 10th shadow measurement applied to the 0th training state.|
|`shadow_meas`|`list`|Results of the classical shadow measurements. The list is organized as `shadow_meas[training_state_0_or_1][measurement_instance][qubit]`. E.g. shadow_meas[1][9][2] tells us the result of measuring qubit 2 during the 9th shadow measurement applied to the 1st training state.|
|`training_circuits`|`list`|List containing two sets of operations. Each set defines a circuit on 16 qubits that generates a state sampled from a Haar random distribution.|
|`training_states`|`list`|List containing two state vectors, one for each training state $\psi$. These should correspond to the output states after simulating `training_circuits`.|