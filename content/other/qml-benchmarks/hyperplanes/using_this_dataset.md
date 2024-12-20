Data for the benchmarking of machine learning models taken from
[Better than classical? The subtle art of benchmarking quantum machine learning models](https://arxiv.org/abs/2403.07059).
This classification task is designed with a labelling mechanism that requires “global” information
on a set of hyperplanes.

**Description of the dataset**

The datasets in this task are generated by fixing $k$ hyperplanes in a $m$-dimensional space,
sampling input vectors from a Gaussian distribution in that same space and assigning each input $k$
“intermediate labels”. The overall label is determined as the parity of the intermediate labels,
or whether the input vector lies on the “positive side” of an even or odd number of hyperplanes.
This can be seen as using $k$ perceptron models to label the data.

The overall label is determined as the parity of the individual labels.

**Additional details**

- The class labels are defined as -1, 1.
- For each number of hyperplanes, 240 labeled points are provided for training and 60 for testing.
- The datasets are balanced, meaning that they contain the same number of samples for each class.
- Please see the ``Source code`` tab to check how the data was generated.

**Example usage**

```python
[ds] = qml.data.load("other", name="hyperplanes")

ds.diff_train['4']['inputs'] # points in 10-dimensional space for 4 hyperplanes
ds.diff_train['4']['labels'] # labels for the points above
```
