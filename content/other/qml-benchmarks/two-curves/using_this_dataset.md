Data for the benchmarking of machine learning models taken from
[Better than classical? The subtle art of benchmarking quantum machine learning models](https://arxiv.org/abs/2403.07059).
This classification task is inspired by Buchanan et al. [1] who show that the difficulty of
distinguishing between two 1-d curves embedded into a high-dimensional space depends on 
the curvature and distance between the curves. 

**Description of the dataset**

For each class, 1-d data is sampled from the interval [0,1] and embedded into a $d$-dimensional 
space by $d$ different functions – one for each dimension. The functions are the same for data
from both classes, with the exception of a shift $\Delta$ that controls the distance between the curves. 
The functions are implemented by low-degree Fourier series, where the degree controls the curvature
of the embedding. Gaussian noise is added to the final $d$-dimensional input vectors.

There are two different dataset collections in this task: 

- ``two_curves`` fixes the degree to $D = 5$, offset to $\Delta = 0.1$ and varies the input vector dimension between $d=2,\ldots,20$.
- ``two_curves_diff`` fixes the dimension $d=10$ and varies the degree $D$ of the polynomial between $D=2,\ldots,20$
  while adapting the offset $\Delta=1/2D$ between the two curves

**Additional details**

- The class labels are defined as -1, 1.
- For each dataset, 240 labeled points are provided for training and 60 for testing.
- The datasets are balanced, meaning that they contain the same number of samples for each class.
- Please see the ``Source code`` tab to check how the data was generated.

**Example usage**

```python
[ds] = qml.data.load("two-curves")

ds.train['4']['inputs'] # points in 4-dimensional space
ds.train['4']['labels'] # labels for the points above

ds.diff_train['5']['inputs'] # points in 10-dimensional space, polynomials of degree 5
ds.diff_train['5']['labels'] # labels for the points above
```

[1] S. Buchanan, D. Gilboa, and J. Wright, Deep networks and the multiple manifold problem, in International Conference on Learning Representations (2021)
