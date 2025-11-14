|Name|Type|Description|
|-|-|-|
|`n_logical_qubits`|`pennylane.data.attributes.list.DatasetList`|Number of logical qubits in the quantum circuit|
|`depth`|`pennylane.data.attributes.list.DatasetList`|Depth of the quantum circuit|
|`single_qubit_counts`|`pennylane.data.attributes.list.DatasetList`|Dictionary where the keys are the names of the single-qubit gates and the values are lists containing the counts of the single-qubit gates for each logical qubits|
|`two_qubit_counts`|`pennylane.data.attributes.list.DatasetList`|Dictionary where the keys are the names of the two-qubit gates and the values are lists containing the counts of the two-qubit gates for each logical qubits|
|`basis_gates`|`pennylane.data.attributes.list.DatasetList`|List containing the names of the gates of the universal set for the hardware|
|`coupling_map`|`pennylane.data.attributes.list.DatasetList`|List containing the hardware connectivity|
|`T1`|`pennylane.data.attributes.list.DatasetList`|List containing the T1 of each physical qubit|
|`T2`|`pennylane.data.attributes.list.DatasetList`|List containing the T2 of each physical qubit|
|`readout_error`|`pennylane.data.attributes.list.DatasetList`|List containing the readout error of each physical qubit|
|`rz_error`|`pennylane.data.attributes.list.DatasetList`|List containing the errors of RZ gate (for each physical qubit)|
|`sx_error`|`pennylane.data.attributes.list.DatasetList`|List containing the errors of SX gate (for each physical qubit)|
|`x_error`|`pennylane.data.attributes.list.DatasetList`|List containing the errors of X gate (for each physical qubit)|
|`ecr`|`pennylane.data.attributes.list.DatasetList`|List containing the errors of ECR gate (for each connected pair of physical qubits)|
|`n_physical_qubits`|`pennylane.data.attributes.list.DatasetList`|Number of physical qubits in the hardware|
|`final_mapping`|`pennylane.data.attributes.list.DatasetList`|Optimized mapping logical -> physical qubits (label for a ML model)|