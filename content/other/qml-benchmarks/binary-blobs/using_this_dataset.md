Data for benchmarking machine learning models, taken from
[Train on classical, deploy on quantum: scaling generative quantum machine learning to a thousand qubits](https://arxiv.org/abs/2503.02934).
The Binary Blobs dataset can be seen as a binary version of the [Gaussian blobs](https://scikit-learn.org/stable/modules/generated/sklearn.datasets.make_blobs.html) 
dataset for continuous data. This dataset is the specific dataset that appeared in the above paper; more general datasets can be 
constructed via the [qml_benchmarks](https://github.com/XanaduAI/qml-benchmarks) package. 

**Description of the dataset**

The dataset consists of bit strings of length 16. To generate samples, one of the 8 following patterns
is selected at random (where data has been reshaped to size (4,4))

<p style="text-align: center"><img src="https://assets.cloud.pennylane.ai/datasets/generic/using_this_dataset/8blobs.png" alt="patterns" width="70%"/></p>

Each bit is then flipped with 5% probability. There are 5000 training points and 10000 test points.
If needed, labels that correspond to the 8 patterns can also be accessed. Please see the ``Source code`` tab to check how the data was generated.

**Example usage**

```pycon
>>> [ds] = qml.data.load("other", name="binary-blobs")
>>>
>>> blob_vector = ds.train['inputs'][0]
>>> blob_array = np.reshape(blob_vector, (4,4))
>>> print(blob_array)
[[0. 0. 1. 1.]
 [0. 0. 1. 1.]
 [0. 0. 0. 0.]
 [0. 0. 0. 0.]]
>>> ds.train['labels'][0]
1
>>> blob_vector = ds.test('inputs')[10]
>>> blob_array = np.reshape(blob_vector, (4,4))
>>> print(blob_array)
[[1. 0. 1. 0.]
 [0. 1. 0. 0.]
 [0. 0. 1. 0.]
 [0. 0. 0. 1.]]
>>> ds.test['labels'][10]
5
```
