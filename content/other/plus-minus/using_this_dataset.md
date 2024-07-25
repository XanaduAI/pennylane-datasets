This dataset contains grayscale images from [A Comparative Analysis of Adversarial Robustness for Quantum and Classical Machine Learning Models](https://arxiv.org/abs/2404.16154) by Wendlinger M., Tscharke, K. and Debus, P. It includes four classes of images that allow benchmarking (quantum) machine learning models for classification tasks.

## Description of the dataset

The train (test) dataset consists of 1000 (200) images split into four classes. Each image contains 16x16 pixels showing either a minus sign, a plus sign, or a right (left) half-plus. Gaussian noise and random rotations (up to 10°) are applied to make the dataset more diverse. The idea of the dataset is to define regions in the input that bear (or lack) semantic meaning, e.g. to differentiate between a right half-plus and a plus, the model needs to attend to the absence of high pixel value in the left part of the image. In contrast to this (for the same example), the region on the top and bottom of the image are the same for both classes and should be irrelevant for successful classification. This lets us evaluate models in their ability to recognize important features as done in above paper.

## Additional details

+ The classes of the dataset are balanced, i.e. each class contains 250 train samples and 50 test samples.
+ The value of each pixel is normalized to lie in the domain [0,1].
+ for an extended dataset or different image resolutions, feel free to contact the authors.

## Example usage

```python
ds = qml.data.load("other", name="plus-minus")

X_train, Y_train = ds.img_train, ds.labels_train

X_test, Y_test = ds.img_test, ds.labels_test

dev = qml.device('default.qubit')

@qml.qnode(dev)
def circuit(image, params):
    qml.AmplitudeEmbedding(image.flatten(),normalize=True, wires=range(8))
    for i in range(8):
        qml.RX(params[i], wires=i)
    for i in range(7):
        qml.CNOT(wires=[i,i+1])
    return qml.expval(qml.PauliZ(wires=0))

np.random.seed(0)
params = np.random.random(8)

predictions = [circuit(x,params) for x in X_train]
```