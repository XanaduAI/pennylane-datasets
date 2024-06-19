This dataset contains the data used to train RydbergGPT, a generative pre-trained transformer designed to learn the measurement outcomes of a neutral atom array quantum computer. 
The dataset contains measurement samples of square lattice atom arrays, sweeping across temperatures and interacting Hamiltonian parameters. For more details on the model and training, please see the [RydbergGPT paper](https://arxiv.org/abs/2405.21052) and the corresponding [GitHub repository](https://github.com/PIQuIL/RydbergGPT). The full dataset is about 22 GB.

**Description of the dataset**

This dataset contains information for 1620 Rydberg atom arrays. The interacting Hamiltonian that governs these Rydberg atom arrays is:

$$
\hat{H} = \sum_{i<j} \frac{C_6}{\lvert \mathbf{r}_i - \mathbf{r}_j \rvert^6} \hat{n}_i \hat{n}_j -\delta \sum_{i=1}^N \hat{n}_i - \frac{\Omega}{2} \sum_{i=1}^N \hat{\sigma}^x_i
$$

$$
C_6 = \Omega \left( \frac{R_b}{a} \right)^6
$$

$$
V_{ij} =  \frac{a^6}{\lvert \mathbf{r}_i - \mathbf{r}_j \rvert^6}
$$

where $\hat{\sigma}^{x}_{i} = \vert g \rangle_i \langle r\vert_i + \vert r \rangle_i \langle g\vert_i$, the occupation number operator $\hat{n}_i = \frac{1}{2} \left( \hat{\sigma}_{i} + \mathbb{1} \right) =  \vert r\rangle_i \langle r \vert_i$, $\hat{\sigma}_{i} = \vert r \rangle_i \langle r \vert_i - \vert g \rangle_i \langle g \vert_i$, and

- $V_{ij}$ = blockade interaction strength between atoms $i$ and $j$
- $\alpha$ = lattice length scale$
- $R_b$ = blockade radius in units of the lattice spacing
- $\hat{n}_i$ = number operator at ion $i$
- $\bold{r}_i$ = the position of atom $i$ in units of the lattice spacing
- $\delta$ = detuning from resonance
- $\Omega$ = Rabi frequency
- $\beta$ = inverse temperature
- $L$ = linear system size, for a total number of atoms $N= L^2$

Each Rydberg atom array in this dataset is identified by a set of parameters $R_b$, $\delta$, $\beta$, and $L$ that define the array shape and dictate the interactions between the atoms. For each set of parameter values, the dataset contains samples of projective occupation measurements obtained via quantum Monte Carlo simulation. Measurements of the energy, x-magnetization, and staggered-magnetization are also included. These measurements are available for all possible points in the parameter space. Specifically, there are 100000 atom array measurement outcomes for all combinations of the following values:

$$
R_b \in \{1.05, 1.15, 1.30\}
$$

$$
\delta \in \{-0.36, -0.13, 0.93, 1.05, 1.17, 1.29, 1.52, 1.76, 2.94, 3.17\}
$$

$$
\beta \in \{0.5, 1.0, 2.0, 4.0, 8.0, 16.0, 32.0, 48.0, 64.0\}
$$

$$
L \in \{5, 6, 11, 12, 15, 16\}
$$

**Additional details**

- Since every Rydberg atom array is square, the number of atoms for an array is the linear system size (length on a side), squared: $L^2$
- The Hamiltonian is represented by the interaction graph (adjacency matrix) between atoms in the array.
- All datapoints are in scaled, non-dimensional units $R_b / a$, $\delta/\Omega$, and  $\beta \Omega$, with the Rabi frequency and lattice spacing fixed to $\Omega= 1$ and $a=1$ for all lattices.

**Example usage**

```python
import pennylane as qml

# Accessing dataset contents

[ds] = qml.data.load('other', name='rydberggpt')

print(ds.energies[0]) # output: {'mean': 0.15884992225163197, 'std': 0.5228880607553665, 'std_err': 0.0004985542042934183}
print(ds.mags_x[0]) # output: 0.22723665454545455

# Creating a networkx graph using the dataset

import networkx as nx

new_graph = nx.Graph()

for i in range(len(ds.interaction_graphs[0])):
    for j in range(len(ds.interaction_graphs[0])):
        if ds.interaction_graphs[0][i][j] != 0: 
            new_graph.add_edge(i, j, weight=ds.interaction_graphs[0][i][j])

print(ds.interaction_graphs[0][4][5]) # output: 0.0002035416242621616
print(new_graph.get_edge_data(4,5)) # output: {'weight': 0.0002035416242621616}
```