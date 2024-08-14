This dataset contains a portion of [HamLib](https://arxiv.org/abs/2306.13126): a library of Hamiltonians for benchmarking quantum algorithms and hardware.
The original data can be downloaded from the [authors' source](https://portal.nersc.gov/cfs/m888/dcamps/hamlib/binaryoptimization/maxcut/random/).

**Description of the dataset**

[MaxCut](https://en.wikipedia.org/wiki/Maximum_cut) is an [NP-Hard](https://en.wikipedia.org/wiki/NP-hardness)
graph partitioning problem.
It involves finding how to separate $N$ nodes into two groups to maximize the number of connections
between the groups.

The solutions to MaxCut problems can be encoded in binary format, where
each node has a corresponding bit and the value of that bit determines what group the
node belongs to.
This dataset uses a quantum formulation of the binary representation, assigning one qubit
per node, with state $|\psi\rangle = |0\rangle$
if the node is in group $0$ and a state $|\psi\rangle = |1\rangle$ if the node is in group $1$.
For example, the state $|0001\rangle$ represents a solution where all nodes have been placed in set $0$,
except the last, which is in set $1$. In practice, this problem is equivalent to finding the state that
maximizes the energy of a spin glass with Hamiltonian $H$. The elements in
this Hamiltonian depend on the connections between nodes. Measuring its expectation value
for a candidate solution state gives the number of connections cut in that solution.

This dataset contains Hamiltonians for several MaxCut problems. Specifically:
- 102 [circulant graphs](https://en.wikipedia.org/wiki/Circulant_graph): nodes are connected to adjacent nodes
(nearest neighbors, next-nearest neighbors, or next-next-nearest neighbors).
- 51 [bipartite graphs](https://en.wikipedia.org/wiki/Bipartite_graph): nodes can be separated into two sets where all nodes in one set connect to
all nodes in the other set.
- 51 [star graphs](https://en.wikipedia.org/wiki/Star_(graph_theory)): all nodes connect to a single central node

**Additional details**

- The problems in this dataset have between 2 and 900 nodes, each corresponding to a Hamiltonian
  with 2 to 900 qubits
- The number of edges in the graphs ranges from 1 to 202,500.
- Circuits using Hamiltonians with either `>=20` qubits or `>=100,000` terms can be computationally expensive
  to simulate.

**Example usage**

```python
[ds] = qml.data.load("other", name="hamlib-maxcut")
ham = ds.hamiltonians[4]

dev = qml.device("default.qubit", wires=4)

@qml.qnode(dev)
def circuit(basis_state):
    qml.BasisStatePreparation(basis_state, wires=range(4))
    return qml.expval(ham)

# edges cut when all nodes are in the same set
circuit([0,0,0,0]) # output: array(0.)
# edges cut when some nodes are in separate sets
circuit([0,0,1,1]) # output: array(4.)
```
