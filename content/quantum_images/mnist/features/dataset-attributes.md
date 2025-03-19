|Name|Type|Description|
|-|-|-|
|`circuit_layout_d4`|`list`|Circuits layout defined as lists of operations and wires they act on with a circuit depth of 4.|
|`circuit_layout_d8`|`list`|Circuits layout defined as lists of operations and wires they act on with a circuit depth of 8.|
|`params_d4`|`list`|Circuit parameters as list of RY angles. When plugged in to the circuit layout with a depth of 8, the circuit approximates the flexible representation of quantum images (FRQI).|
|`params_d8`|`list`|Circuit parameters as list of RY angles. When plugged in to the circuit layout with a depth of 8, the circuit approximates the flexible representation of quantum images (FRQI).|
|`labels`|`list`|A list of the correct labels for each image.|
|`exact_state`|`list`|A list of numpy arrays. Each numpy array defines a FRQI state that exactly encodes an MNIST image.|