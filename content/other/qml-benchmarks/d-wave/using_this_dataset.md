# Using this Dataset
Data for benchmarking machine learning models, taken from
[Train on classical, deploy on quantum: scaling generative quantum machine learning to a thousand qubits](https://arxiv.org/abs/2503.02934).
This dataset contains bistrings that are sampled from a D-Wave advantage processor, as described in 
[Accelerating equilibrium spin-glass
simulations using quantum annealers via generative deep learning](https://scipost.org/SciPostPhys.15.1.018). This specific dataset is taken from 
a quench of 100  microseconds on 484 of the processor's qubits.

**Description of the dataset**

The dataset consists of bit strings of length 484, that correspond to outcomes of measurements on each of the 484 qubits. 
The qubits are coupled via the processors `pegasus` topology. 
Please see the ``Source code`` tab to check how the data was generated.

**Example usage**

```python
[ds] = qml.data.load("other", name="d-wave)

ds.train['inputs']
ds.test['inputs']
```
