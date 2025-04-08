# Using this Dataset
Data for benchmarking machine learning models, taken from
[Train on classical, deploy on quantum: scaling generative quantum machine learning to a thousand qubits](https://arxiv.org/abs/2503.02934).
The Binary Blobs dataset can be seen as a binary version of the [Gaussian blobs](https://scikit-learn.org/stable/modules/generated/sklearn.datasets.make_blobs.html) 
dataset for continuous data. This dataset is the specific dataset that appeared in the above paper; more general datasets can be 
constructed via the [qml_benchmarks](https://github.com/XanaduAI/qml-benchmarks) package. 

**Description of the dataset**

The dataset consists of bit strings of length 16. To generate samples, one of the 8 following patterns
is selected at random (where data has been reshaped to size (4,4))

![patterns](8blobs.png)

Each bit is then flipped with 5% probability. There are 5000 training points and 10000 test points.
If needed, labels that correspond to the 8 patterns can also be accessed. Please see the ``Source code`` tab to check how the data was generated.

**Example usage**

```python
[ds] = qml.data.load("other", name="binary-blobs")

ds.train['inputs']
ds.train['labels']
ds.test['inputs']
ds.test['labels']
```
