|Name|Type|Description|
|-|-|-|
|`diff_test`|`dict`|Diff test sets. These are provided as a dictionary with form ``diff_test[n_manifolds]['labels' or 'inputs'][index]`` and contain 60 labeled vectors for each number of manifolds (n_manifolds) between 2 and 20.|
|`diff_train`|`dict`|Diff training sets. These are provided as a dictionary with form ``diff_train[n_manifolds]['labels' or 'inputs'][index]`` and contain 240 labeled vectors for each number of manifolds (n_manifolds) between 2 and 20.|
|`test`|`dict`|Test sets. These are provided as a dictionary with form ``test[dimensions]['labels' or 'inputs'][index]`` and contain 60 labeled vectors for each number of dimensions between 2 and 20.|
|`train`|`dict`|Training sets. These are provided as a dictionary with form ``train[dimensions]['labels' or 'inputs'][index]`` and contain 240 labeled vectors for each number of dimensions between 2 and 20.|