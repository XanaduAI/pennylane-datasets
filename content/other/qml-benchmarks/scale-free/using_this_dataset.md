# Using this Dataset
Data for benchmarking machine learning models, taken from
[Train on classical, deploy on quantum: scaling generative quantum machine learning to a thousand qubits](https://arxiv.org/abs/2503.02934).
This dataset contains bit strings sampled from a thermal distributions of an Ising Hamiltonian
that has a connectivity given by a scale-free network with 1000 nodes. 

**Description of the dataset**

The dataset contains bit strings of length 1000 that correspond to spin configurations of the Ising distribution. 
The graph describing the two-body interactions of the Ising Hamiltonian corresponds to a scale free network, which is 
constructed via the Barabasi-Albert algorithm with connectivity parameter 2. The Ising energy has a local bias that 
is dependent on the degree of the corresponding node, which biases the values of that bit towards zero. 
The data was generated via a Metropolis Hastings algorithm by sampling a million configurations on eight independent 
Markov chains, and then selecting 20000 train and test points randomly from equally spaced points on the chain.

**Example usage**

```python
[ds] = qml.data.load("other", name="scale-free)

ds.train
ds.test
```
