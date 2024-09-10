Data for benchmarking machine learning models, taken from
[Better than classical? The subtle art of benchmarking quantum machine learning models](https://arxiv.org/abs/2403.07059). 
The Downscaled MNIST classification task is a simplified version of the famous [MNIST handwritten digits dataset](https://en.wikipedia.org/wiki/MNIST_database).
This version involves distinguishing between digits 3 and 5 rather than the full range 0-9.

**Description of the dataset**

This collection provides 19 datasets that consist of flat input vectors of dimension $d=2,\ldots,20$.
The inputs were produced by fitting a PCA dimensionality reduction model on the original MNIST training sets,
and using the same model to reduce the images from the test set.

**Additional details**

- The class labels are defined as -1, 1.
- For each dimension, 11552 labeled points are provided for training and 1902 for testing.
- Please see the ``Source code`` tab to check how the data was generated.

**Example usage**

```python
[ds] = qml.data.load("other", name="mnist-pca")

ds.train['4']['inputs'] # points in 4-dimensional space
ds.test['4']['labels'] # labels for the points above
```
