Data for benchmarking machine learning models, taken from
[Train on classical, deploy on quantum: scaling generative quantum machine learning to a thousand qubits](https://arxiv.org/abs/2503.02934).
This dataset contains bistrings that are sampled from a D-Wave advantage processor, as described in 
[Accelerating equilibrium spin-glass
simulations using quantum annealers via generative deep learning](https://scipost.org/SciPostPhys.15.1.018).

**Description of the dataset**

This dataset contains 70,000 bit strings of length 484, that correspond to outcomes of measurements on each of the 484 qubits of the processor. These are divided into 10,000 training samples and 60,000 test samples. 

This specific dataset is taken from 
a quench of 100  microseconds with the qubits coupled via the processor's `pegasus` topology.
Please see the ``Source code`` tab to check how the data was generated.

**Example usage**

```pycon
>>> [ds] = qml.data.load("other", name="d-wave")
>>>
>>> np.shape(ds.train)
(10000, 484)
```
