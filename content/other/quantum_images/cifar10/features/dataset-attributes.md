|Name|Type|Description|
|-|-|-|
|`circuits_d4`|`list`|Circuits defined as lists of operations with a circuit depth of 4. Each list is a circuit that approximates the multi-channel representation for images on quantum computers.|
|`circuits_d8`|`list`|Circuits defined as lists of operations with a circuit depth of 8. Each list is a circuit that approximates the multi-channel representation for images on quantum computers.|
|`labels`|`list`|A list of the correct labels for each image.|
|`target_states`|`list`|A list of numpy arrays. Each numpy array defines a multi-channel representation for images on quantum computers that exactly encodes a CIFAR-10 image.|