|Name|Type|Description|
|-|-|-|
|img_test|[`pennylane.numpy.tensor`](https://docs.pennylane.ai/en/stable/code/api/pennylane.numpy.tensor.html)|Two hundred 16x16 pixel images given as a PennyLane tensor of shape (200, 16, 16).|
|img_train|[`pennylane.numpy.tensor`](https://docs.pennylane.ai/en/stable/code/api/pennylane.numpy.tensor.html)|One thousand 16x16 pixel images given as a PennyLane tensor of shape (1000, 16, 16).|
|labels_test|numpy.ndarray|Labels corresponding to the images in img_test. 0 corresponds to '-', 1 corresponds to '+', 2 corresponds to '⊢' and 3 corresponds to '⊣'.|
|labels_train|numpy.ndarray|Labels corresponding to the images in img_train. 0 corresponds to '-', 1 corresponds to '+', 2 corresponds to '⊢' and 3 corresponds to '⊣'|