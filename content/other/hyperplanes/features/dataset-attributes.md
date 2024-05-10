|Name|Type|Description|
|-|-|-|
|`diff_test`|`dict`|Diff test sets. These are provided as a dictionary with form ``diff_test[n_hyperplanes]['labels' or 'inputs'][index]`` and contain 60 labeled vectors for each number of hyperplanes (n_hyperplanes) between 2 and 20.|
|`diff_train`|`dict`|Diff training sets. These are provided as a dictionary with form ``diff_train[n_hyperplanes]['labels' or 'inputs'][index]`` and contain 240 labeled vectors for each number of hyperplanes (n_hyperplanes) between 2 and 20.|