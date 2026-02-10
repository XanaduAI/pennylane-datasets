This data is accessed via the `circuit` attribute of the dataset.
Choose a `sample_index` from the 2001 available samples and access the data below via
`circuit[sample_index][attribute_name]`

|Name|Type|Description|
|-|-|-|
|`circuit["n_logical_qubits"]`|`pennylane.data.attributes.list.DatasetList`|Number of logical qubits in the quantum circuit|
|`circuit["depth"]`|`pennylane.data.attributes.list.DatasetList`|Depth of the quantum circuit|
|`circuit["single_qubit_counts"]`|`pennylane.data.attributes.list.DatasetList`|Dictionary where the keys are the names of the single-qubit gates and the values are lists containing the counts of the single-qubit gates for each logical qubits|
|`circuit["two_qubit_counts"]`|`pennylane.data.attributes.list.DatasetList`|Dictionary where the keys are the names of the two-qubit gates and the values are lists containing the counts of the two-qubit gates for each logical qubits|