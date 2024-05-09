|Name|Type|Description|
|-|-|-|
|`circuits`|`list`|Circuits defined as lists of operations. Each list is a circuit that uses Automatic Quantum Circuit Encoding to embed an image in the complex amplitudes of a quantum state.|
|`fidelity`|`list`|The fidelity between the target state and the state implemented by the circuit.|
|`labels`|`list`|A list of the correct labels for each image.|
|`target_states`|`list`|A list of numpy arrays. Each numpy array defines a quantum state that exactly encodes an MNIST image.|