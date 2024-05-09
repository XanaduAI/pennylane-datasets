|Name|Type|Description|
|-|-|-|
|`diff_test`|`dict`|Diff test sets. These are provided as a dictionary with form ``diff_test[polynomialdegree]['labels' or 'inputs'][index]`` and contain 60 labeled vectors for each polynomial degree between 2 and 20.|
|`diff_train`|`dict`|Diff training sets. These are provided as a dictionary with form ``diff_train[polynomialdegree]['labels' or 'inputs'][index]`` and contain 240 labeled vectors for each polynomial degree between 2 and 20.|
|`test`|`dict`|Test sets. These are provided as a dictionary with form ``test[dimension]['labels' or 'inputs'][index]`` and contain 60 labeled vectors for each dimension between 2 and 20.|
|`train`|`dict`|Training sets. These are provided as a dictionary with form ``train[dimension]['labels' or 'inputs'][index]`` and contain 240 labeled vectors for each dimension between 2 and 20.|