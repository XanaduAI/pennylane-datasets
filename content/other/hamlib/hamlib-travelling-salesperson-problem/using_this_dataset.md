This dataset contains a portion of [HamLib](https://arxiv.org/abs/2306.13126): a library of Hamiltonians for benchmarking quantum algorithms and hardware.
Here, we have included several examples of the travelling salesperson problem for 4 to 10 cities, adapted to facilitate use with PennyLane.
The original data can be downloaded from the [authors' source](https://portal.nersc.gov/cfs/m888/dcamps/hamlib/discreteoptimization/tsp/).

**Description of the dataset**

Traveling salesperson problems involve finding the shortest path through $N$ locations
and then returning to the first location. 
For example, if you have to visit five stores and then return home,
in what order should you go to the stores to minimize the total trip distance?
This depends on the distances between the locations.

A solution to a traveling salesperson problem can be encoded using a
binary format, for example, `00 10 01 11` (representing a solution where the
salesperson starts at store 0, then travels to store 2, followed by 1, and 3).
This can subsequently be encoded into a quantum state
$|\psi\rangle = |00100111\rangle$. A cost function that measures the distance traveled
can be encoded into a Hamiltonian $H$. This Hamiltonian depends on the distances between the locations.
Then, to compute the distance traveled in a certain solution,
we can take the expectation value of the Hamiltonian with respect to the
encoded quantum state, $\langle H\rangle = \langle \psi | H | \psi \rangle$.

This dataset contains Hamiltonians for several traveling salesperson problems.
Each Hamiltonian acts as the cost function for its corresponding traveling salesperson problem.

**Additional details**

- The problems range from 4 to 10 cities. This corresponds to 8 to 40 qubits. Note that any circuit with 20 or more qubits can be computationally expensive to simulate.
- To facilitate use with PennyLane, we use [big-endian](https://en.wikipedia.org/wiki/Endianness) binary encoding.
  This means that a string of qubits $|00\dots 0\rangle$ is read from left to right,
  i.e., `10` corresponds to 2 in the decimal system.
- Qubits are grouped such that the value of the qubits indicates a city. For example,
  the state `00011011` uses two qubits per city label, `00 01 10 11`. This
  varies as the number of cities increases; in a traveling salesperson problem with five cities, 
  we need to use three qubits per city label,
  for a total of 15 qubits.
- The Hamiltonians do not account for invalid answers. This means that an invalid answer
  of the form `00 00 00 00`, where the salesperson does not leave city `00`, will give
  a cost of 0. This will need to be accounted for when using this dataset.
- The ``distmat`` attribute defines the pairwise distances between the cities. It is an
  array where element $(i,j)$ contains the distance between city $i$ and city $j$.

**Example usage**

```python
[ds] = qml.data.load("other", name="hamlib-tsp")

dev = qml.device("default.qubit", wires = 8)
@qml.qnode(dev)
def circuit(basis_state):
    qml.BasisStatePreparation(basis_state, wires=range(8))
    return qml.expval(ds.hamiltonians[2])

# go to cities in order 00 -> 01 -> 10 -> 11
circuit([0,0,0,1,1,0,1,1]) # output: array(7321.)
# go to cities in order 10 -> 00 -> 01 -> 11
circuit([1,0,0,0,0,1,1,1]) # output: array(5803.)
```
