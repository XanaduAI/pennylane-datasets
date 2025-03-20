Data for benchmarking machine learning models, generated for an upcoming paper: *Typical Machine Learning Datasets as Low-Depth Quantum Circuits*.

**Description of the dataset**

The [MNIST dataset](https://ieeexplore.ieee.org/document/6296535) has 28x28 grayscale images of 70,000 hand-drawn digits from 0 to 9, totalling 10 categories, with 7,000 images per category. Here, we provide circuit parameters that approximate the [Flexible Representation of Quantum Images (FRQI)](https://link.springer.com/article/10.1007/s11128-010-0177-y) of each image in the MNIST dataset.

**Additional details**

- The class labels are integers from 0 to 9.
- Implementing the circuits in this dataset and obtaining the final state with PennyLane's `qml.state()` outputs a state vector. This state vector must be processed to recover the original image.
- The dataset contains two circuits per image: those with a depth of four, which are shallower, and those with a depth of eight, which provide more accurate approximations of the exact state.

**Example usage**

```python
import pennylane as qml
import jax

ds= qml.data.load("low-depth-mnist")

def get_circuit(circuit_layout):
    dev = qml.device("default.qubit", wires=11)
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