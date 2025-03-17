|Name|Type|Description|
|-|-|-|
|train|dict|BO Train input data and labels. Each input is a binary array of shape (16,) that when reshaped to shape (4,4) gives a 2D image corresponding to one of the 8 patterns. Labels are integers from 0 to 7 specifying the pattern of the corresponding input.|
|test|dict|Test input data and labels. Each input is a binary array of shape (16,) that when reshaped to shape (4,4) gives a 2D image corresponding to one of the 8 patterns. Labels are integers from 0 to 7 specifying the pattern of the corresponding input.|