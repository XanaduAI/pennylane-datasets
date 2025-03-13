Data for benchmarking machine learning models, taken from
[Efficient Quantum Image Representations and Benchmarking of Supervised Quantum Machine Learning Models](https://arxiv.org/abs/2503.xx).

The [CIFAR-10 dataset](https://ieeexplore.ieee.org/document/6296535) consists of 60000 32x32 colour images in 10 classes, with 6000 images per class. We provide circuit parameters that approximates the the [Multi-Channel Representation for images on quantum computers](https://ieeexplore.ieee.org/document/6051718) of the images.

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

ds= qml.data.load("cifar_10")

@qml.qnode(qml.device("default.qubit"))
def circuit(index):
    for op in ds.circuits_d8[index]:
        qml.apply(op)

    return qml.state()

# Get the quantum state that corresponds to the first quanutm ciruit
frqi_state = circuit(index)
```