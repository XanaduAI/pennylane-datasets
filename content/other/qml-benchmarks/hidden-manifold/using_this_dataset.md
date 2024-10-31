Data for the benchmarking of machine learning models taken from
[Better than classical? The subtle art of benchmarking quantum machine learning models](https://arxiv.org/abs/2403.07059).
Proposed by Goldt et al. (2021) [1], this classification task mimics the idea that data is labeled on a
“hidden” manifold that is embedded into a space of different dimensionality. 
A machine learning model has to find the manifold to solve the problem.
It is conjectured that the size of the manifold controls the difficulty of the problem.

**Description of the dataset**

Input vectors of m dimensions are sampled from a normal distribution in a
low-dimensional space and labeled by a single-layer neural network initialised at random.
The inputs are then projected to the final d-dimensional space. 

There are two different dataset collections in this task:

- ``hidden_manifold`` varies only the dimension of the input vectors between $d=2,\ldots,20$ and
  keeps the dimension of the hidden manifold constant at $m=6$.
- `hidden_manifold_diff`` keeps the dimension constant at $d=10$ and varies the 
  dimensionality $m$ of the manifold between $m=2,\ldots,20$

**Additional details**

- The class labels are defined as -1, 1.
- For each space, 240 labeled points are provided for training and 60 for testing.
- The datasets are balanced, meaning that they contain the same number of samples for each class.
- Please see the ``Source code`` tab to check how the data was generated.

**Example usage**

```python
[ds] = qml.data.load("hidden-manifold")

ds.train['4']['inputs'] # points in 4-dimensional space
ds.train['4']['labels'] # labels for the points above

ds.diff_train['5']['inputs'] # points in 10-dimensional space, projected from a 5-dimensional manifold
ds.diff_train['5']['labels'] # labels for the points above
```

[1] S. Goldt, M. Mezard, F. Krzakala, and L. Zdeborova, Modeling the influence of data structure on learning in neural networks: The hidden manifold model, Physical Review X 10, 041044 (2020).
