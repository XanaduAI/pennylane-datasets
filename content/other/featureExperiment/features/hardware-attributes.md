|Name|Type|Description|
|-|-|-|
|`basis_gates`|`pennylane.data.attributes.list.DatasetList`|List containing the names of the gates of the universal set for the hardware|
|`coupling_map`|`pennylane.data.attributes.list.DatasetList`|List containing the hardware connectivity|
|`T1`|`pennylane.data.attributes.list.DatasetList`|List containing the T1 of each physical qubit|
|`T2`|`pennylane.data.attributes.list.DatasetList`|List containing the T2 of each physical qubit|
|`readout_error`|`pennylane.data.attributes.list.DatasetList`|List containing the readout error of each physical qubit|
|`rz_error`|`pennylane.data.attributes.list.DatasetList`|List containing the errors of RZ gate (for each physical qubit)|
|`sx_error`|`pennylane.data.attributes.list.DatasetList`|List containing the errors of SX gate (for each physical qubit)|
|`x_error`|`pennylane.data.attributes.list.DatasetList`|List containing the errors of X gate (for each physical qubit)|
|`ecr`|`pennylane.data.attributes.list.DatasetList`|List containing the errors of ECR gate (for each connected pair of physical qubits)|