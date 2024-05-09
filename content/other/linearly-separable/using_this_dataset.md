Data for benchmarking machine learning models, taken from
[Better than classical? The subtle art of benchmarking quantum machine learning models](https://arxiv.org/abs/2403.07059).
The Linearly Separable task can be seen as a ”fruit-fly'' example for classification.
It is straightforward and well-understood in the field.
Even in the early days of artificial intelligence research, investigators already knew
that linearly separable classification tasks can be learned by a simple perceptron model.

**Description of the dataset**

The data collection consists of 19 individual datasets with 300 samples each that vary in
dimension from $d=2$ to $d=20$. The samples are points in $d$-dimensional space and can be separated
into their classes by a hyperplane.

Each dataset is generated by sampling inputs uniformly from a $d$-dimensional hypercube.
The inputs are divided into two classes by the hyperplane orthogonal to the $(1, \ldots, 1)^T$ vector.

There is a data-free margin $\Delta$ around the hyperplane which guarantees that all datapoints
$x$ fulfill $|x w| > \delta$. The size of the margin grows with the dimension as $\Delta = 0.02d$.


**Additional details**

- The class labels are defined as -1, 1.
- For each dataset, 240 labeled points are provided for training and 60 for testing.
- The datasets are balanced, which means that they contain the same number of samples for each class.
- Please see the ``Source code`` tab to check how the data was generated.

**Example usage**

```python
[ds] = qml.data.load("other", name="linearly-separable")

ds.train['4']['inputs'] # points in 4-dimensional space
ds.train['4']['labels'] # labels for the points above
```