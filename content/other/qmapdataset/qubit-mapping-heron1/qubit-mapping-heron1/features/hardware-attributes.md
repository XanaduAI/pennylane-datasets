This data is accessed via the `hardware` attribute of the dataset.
Choose a `sample_index` from the 2001 available samples and access the data below via
`hardware[sample_index][attribute_name]`

|Name|Type|Description|
|-|-|-|
|`hardware[sample_index]["basis_gates"]`|`pennylane.data.attributes.list.DatasetList`|List containing the names of the gates of the universal set for the hardware|
|`hardware[sample_index]["coupling_map"]`|`pennylane.data.attributes.list.DatasetList`|List containing the hardware connectivity|
|`hardware[sample_index]["T1"]`|`pennylane.data.attributes.list.DatasetList`|List containing the T1 of each physical qubit|
|`hardware[sample_index]["T2"]`|`pennylane.data.attributes.list.DatasetList`|List containing the T2 of each physical qubit|
|`hardware[sample_index]["readout_error"]`|`pennylane.data.attributes.list.DatasetList`|List containing the readout error of each physical qubit|
|`hardware[sample_index]["rz_error"]`|`pennylane.data.attributes.list.DatasetList`|List containing the errors of RZ gate (for each physical qubit)|
|`hardware[sample_index]["sx_error"]`|`pennylane.data.attributes.list.DatasetList`|List containing the errors of SX gate (for each physical qubit)|
|`hardware[sample_index]["x_error"]`|`pennylane.data.attributes.list.DatasetList`|List containing the errors of X gate (for each physical qubit)|
|`hardware[sample_index]["ecr"]`|`pennylane.data.attributes.list.DatasetList`|List containing the errors of ECR gate (for each connected pair of physical qubits)|