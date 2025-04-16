A short intro sentence or two. For example: This is data taken from [paper] it can be used for [what it can be used for].

**Description of the dataset**

A more detailed description of the dataset. Can be several sentences.

**Additional details**

Typically very specific details of the dataset, usually as a bulleted list. For example:

- The class labels are defined as -1, 1.
- For each grid dimension, 1000 labeled points are provided for training and 200 for testing.
- The datasets are balanced, which means that they contain the same number of samples for each class.
- Please see the ``Source code`` tab to check how the data was generated.

**Example usage**
Code examples of how to use this dataset


```python
[ds] = qml.data.load("other", name="leucine")

dev = qml.device('default.qubit')
@qml.qnode(dev)
def circuit():
    qml.StatePrep(ds.state)
    return qml.state()

circuit()
```
