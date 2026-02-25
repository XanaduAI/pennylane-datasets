This data is accessed via the `mapping` attribute of the dataset.
Choose a `sample_index` from the 2001 available samples and access the data below via
`mapping[sample_index][attribute_name]`

|Name|Type|Description|
|-|-|-|
|`mapping[sample_index]["n_physical_qubits"]`|`pennylane.data.attributes.list.DatasetList`|Number of physical qubits in the hardware|
|`mapping[sample_index]["final_mapping"]`|`pennylane.data.attributes.list.DatasetList`|Optimized mapping logical -> physical qubits (label for a ML model)|