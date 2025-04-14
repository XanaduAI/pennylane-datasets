Data for benchmarking machine learning models, taken from
[Train on classical, deploy on quantum: scaling generative quantum machine learning to a thousand qubits](https://arxiv.org/abs/2503.02934).
This dataset contains bit strings sampled from thermal distributions of Ising Hamiltonians
that have a 2D square lattice connectivity.

**Description of the dataset**

The dataset contains data from different lattice sizes. The Hamiltonians for each lattice size
have a 2D square lattice topology with periodic boundary conditions. The couplings are
sampled as random positive numbers in [0,2] and there are no local bias terms. The Metropolis Hastings algorithm
is then used to sample configurations from a thermal distribution with temperature parameter 3.

**Additional information**
- The number of train and test points depends on the lattice size
- The available lattice sizes are (2,4), (2,5), (2,6), (2,7), (2,8), (2,9), (2,10), (3,3), (3,4), (3,6), (3,7), (3,8), (4,4), (4,5), (4,6), (5,5)

**Example usage**

```pycon
>>> [ds] = qml.data.load("other", name="ising")
>>>
>>> np.shape(ds.train['(3,6)']) # 3x6 lattice size
(5000, 18)
>>> ds.train['(3,6)']
array([[0, 0, 0, ..., 1, 0, 0],
       [1, 1, 0, ..., 0, 0, 0],
       [1, 1, 1, ..., 0, 1, 1],
       ...,
       [1, 1, 1, ..., 1, 1, 1],
       [0, 0, 0, ..., 0, 0, 0],
       [0, 0, 0, ..., 0, 0, 0]], dtype=int32)
```
