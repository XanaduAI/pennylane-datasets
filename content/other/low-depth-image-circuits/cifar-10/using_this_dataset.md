Data for benchmarking machine learning models, as detailed in the paper: *Typical Machine Learning Datasets as Low-Depth Quantum Circuits*.

**Description of the dataset**

The [CIFAR-10 dataset](https://www.cs.toronto.edu/~kriz/learning-features-2009-TR.pdf) contains 60,000 32×32 color images across 10 categories (e.g., airplanes, cars, birds, and cats), with 6,000 images per category. Here, we provide circuit parameters that approximate the [Multi-Channel Representation of Quantum Images (MCRQI)](https://ieeexplore.ieee.org/document/6051718) of each image in the CIFAR-10 dataset.

**Additional details**

- The class labels are integers from 0 to 9.
- Implementing the circuits in this dataset and obtaining the final state with PennyLane's `qml.state()` outputs a state vector. This state vector must be processed to recover the original image.
- The dataset contains two circuits per image: those with a depth of four, which are shallower, and those with a depth of eight, which provide more accurate approximations of the exact state.
- The `exact_state` entry contains a list of numpy arrays representing MCRQI states that exactly encode Imagenette images. This significantly increases the file size and can be omitted during download if not needed.

**Example usage**

```python
import pennylane as qml
import jax

[dataset_params] = qml.data.load("low-depth-cifar-10")

def get_circuit(circuit_layout):
    dev = qml.device("default.qubit", wires=13)
    @jax.jit
    @qml.qnode(dev)
    def circuit(params):
        counter = 0
        for gate, wire in circuit_layout:

            if gate == "RY":
                qml.RY(params[counter], wire)
                counter += 1

            elif gate == "CNOT":
                qml.CNOT(wire)

        return qml.state()

    return circuit

# Example for running the circuit with depth 4
circuit_layout_d4 = dataset_params.circuit_layout_d4
circuit_d4 = get_circuit(circuit_layout_d4)
state_d4 = circuit_d4(dataset_params.params_d4[0])

# Example for running the circuit with depth 8
circuit_layout_d8 = dataset_params.circuit_layout_d8
circuit_d8 = get_circuit(circuit_layout_d8)
state_d8 = circuit_d8(dataset_params.params_d8[0])
```