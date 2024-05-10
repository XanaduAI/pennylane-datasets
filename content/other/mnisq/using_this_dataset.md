
This dataset contains a portion of [MNISQ](https://arxiv.org/abs/2306.16627): a dataset that encodes data from MNIST, Fashion-MNIST, and Kuzushiji-MNIST into quantum circuits.
Here, we have included some of the MNIST training circuits at 90% fidelity, adapted to facilitate use with PennyLane.
The original data can be downloaded from the [authors' source](https://github.com/FujiiLabCollaboration/MNISQ-quantum-circuit-dataset).

**Description of the dataset**

[MNIST](https://en.wikipedia.org/wiki/MNIST_database) contains images of hand-written digits in 28x28 pixel grayscale format and the correct labels identifying the digits.
MNISQ encodes these images into **quantum circuits**. Each circuit [amplitude-encodes](https://docs.pennylane.ai/en/stable/code/api/pennylane.AmplitudeEmbedding.html) an image from MNIST.
This means that the final state of the qubits affected by the circuit can be read to recover the image.

In this dataset, the states are encoded with approximately 90% fidelity.
90% fidelity here means that the circuit implements a state $|\psi\rangle$ and that $\langle\psi_{\text{target}}|\psi\rangle \approx 0.90$,
where $\psi_{\text{target}}$ is a state whose amplitudes exactly encode the pixel values of the image, up to a normalization factor.

**Additional details**

- This dataset contains the first 50,000 images from the training dataset.
- Implementing this circuit and obtaining the final state with PennyLane outputs a state vector.
- Each element of the state vector corresponds to the value of a pixel.
- The first element corresponds to the top left pixel and the final element corresponds to the bottom right pixel.

**Example usage**

```python
import numpy as np
import matplotlib.pyplot as plt
import pennylane as qml

ds= qml.data.load("other", name="mnisq")

@qml.qnode(qml.device("default.qubit"))
def circuit():
    for op in ds.circuits[0]:
        qml.apply(op)

    return qml.state()

image_array = np.reshape(np.abs(circuit()[:784]), [28,28])
#show the encoded image
plt.imshow(image_array)
```
