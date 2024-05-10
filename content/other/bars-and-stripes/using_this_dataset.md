Data for benchmarking machine learning models, taken from
[Better than classical? The subtle art of benchmarking quantum machine learning models](https://arxiv.org/abs/2403.07059).
The Bars and Stripes classification task is a simple example for translation-invariant data:
shifting the features does not change the class label. 

**Description of the dataset**

The labels indicate whether an image shows black vertical bars or horizontal stripes.

Gaussian noise with a standard deviation of 0.5 was added to each pixel to determine its final gray-scale value. 

**Additional details**

- The class labels are defined as -1, 1.
- For each grid dimension, 1000 labeled points are provided for training and 200 for testing.
- The datasets are balanced, which means that they contain the same number of samples for each class.
- Please see the ``Source code`` tab to check how the data was generated.

**Example usage**

```python
[ds] = qml.data.load("other", name="bars-and-stripes")

ds.train['4']['inputs'] # vector representations of 4x4 pixel images
ds.train['4']['labels'] # labels for the above images
plt.imshow(np.reshape(ds.training_sets['4']['inputs'][0], (4,4))) # show one of the 4x4 images
```
