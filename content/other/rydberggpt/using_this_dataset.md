This dataset contains the data used to train the RydbergGPT LLM model,
developed and trained by the Perimeter Institute Quantum Intelligence Lab and
collaborators. The full dataset is about 22 GB.
The model trained on this data is a vanilla encoder-decoder transformer architecture, which
generates projective measurement samples of a Rydberg atom array system,
conditioned on the Hamiltonian parameters. For more details on the model and training, please see the [RydbergGPT paper](https://arxiv.org/abs/2405.21052) and the corresponding [GitHub Repository](https://github.com/PIQuIL/RydbergGPT).

**Description of the dataset**
This dataset contains information for 1620 Rydberg atom arrays. These arrays
are governed by the Hamiltonian:

$$\hat{H} = \sum_{i<j} \frac{C_6}{\lvert \mathbf{r}_i - \mathbf{r}_j \rvert^6} \hat{n}_i \hat{n}_j -\delta \sum_{i=1}^N \hat{n}_i - \frac{\Omega}{2} \sum_{i=1}^N \hat{\sigma}^x_i$$

where

$$ C_6 = \Omega \left( \frac{R_b}{a} \right)^6 $$
$$V_{ij} =  \frac{a^6}{\lvert \mathbf{r}_i - \mathbf{r}_j \rvert^6}$$

with $\hat{\sigma}^{x}_{i} = \vert g \rangle_i \langle r\vert_i + \vert r \rangle_i \langle g\vert_i$, the occupation number operator $\hat{n}_i = \frac{1}{2} \left( \hat{\sigma}_{i} + \mathbb{1} \right) =  \vert r\rangle_i \langle r \vert_i$ and $\hat{\sigma}_{i} = \vert r \rangle_i \langle r \vert_i - \vert g \rangle_i \langle g \vert_i$.

Each Rydberg atom array in this dataset is identified by a set of parameters $R_b$, $\delta$, $\beta$, and $L$ that define the array shape and dictate the interactions between the atoms. For each set of parameter values, the dataset contains samples of projective occupation measurements obtained via quantum Monte Carlo simulation. Measurements of the energy and magnetization are also included. These measurements are available for all possible points in the parameter space. Specifically there is one set of measurements for all combinations of the following values:
$$R_b \in {1.05, 1.15, 1.30}$$
$$\delta \in {-0.36, -0.13, 0.93, 1.05, 1.17, 1.29, 1.52, 1.76, 2.94, 3.17}$$
$$\beta \in {0.5, 1.0, 2.0, 4.0, 8.0, 16.0, 32.0, 48.0, 64.0}$$
$$L \in {5, 6, 11, 12, 15, 16}$$

**Additional details**

- Since every Rydberg atom array is square, the number of atoms for an array is the linear system size (length on a side), squared: $L^2$
- The Rabi frequency is fixed to $\Omega=1$ for all lattices.

**Example usage**

```python
import pennylane as qml
import networkx as nx

# Creating a networkx graph using the dataset

[ds] = qml.data.load('other', name='rydberggpt')

new_graph = nx.Graph()

for i in range(len(ds.interaction_graphs[0])):
    for j in range(len(ds.interaction_graphs[0])):
        if ds.interaction_graphs[0][i][j] != 0: 
            new_graph.add_edge(i, j, weight=ds.interaction_graphs[0][i][j])

print(ds.interaction_graphs[0][4][5]) # output: 0.0002035416242621616
print(new_graph.get_edge_data(4,5)) # output: {'weight': 0.0002035416242621616}
```