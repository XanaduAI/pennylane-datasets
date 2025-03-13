Data for benchmarking machine learning models, taken from
[Efficient Quantum Image Representations and Benchmarking of Supervised Quantum Machine Learning Models](https://arxiv.org/abs/2503.xx).

The [Fashion-MNIST dataset](https://arxiv.org/abs/1708.07747) has 28x28 grayscale images of 70,000 fashion products from 10 categories, with 7,000 images per category. We provide circuit parameters that approximates the the [Flexible Representation of Quantum Images (FRQI)](https://link.springer.com/article/10.1007/s11128-010-0177-y) of the images.

**Description of the dataset**

The labels indicate whether an image shows black vertical bars or horizontal stripes.

**Additional details**

- The class labels are integers from 0 to 9.
- Implementing this circuit and obtaining the final state with PennyLane outputs a state vector.
- Check the demo ... [TODO]
- The dataset contains two circuits per image: those with a depth of four, which are shallower, and those with a depth of eight, which provide more accurate approximations of the exact state.

**Example usage**

```python
import numpy as np
import pennylane as qml

ds= qml.data.load("fashion_mnist")

@qml.qnode(qml.device("default.qubit"))
def circuit(index):
    for op in ds.circuits_d8[index]:
        qml.apply(op)

    return qml.state()

# Get the quantum state that corresponds to the first quanutm ciruit
frqi_state = circuit(index)
```
