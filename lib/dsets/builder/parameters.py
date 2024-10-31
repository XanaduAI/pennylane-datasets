from dsets.schemas import Dataset, DatasetFamily, DatasetParameterNode


def build_parameter_tree(family: DatasetFamily):
    partial = family.parameter_tree
    if partial is None:
        partial = DatasetParameterNode(next={})

    if not family.class_.parameter_list:
        return partial

    parameter_names = [parameter.name for parameter in family.class_.parameter_list]

    for dataset in family.data:
        _build_parameter_tree_dataset(parameter_names, dataset, partial)

    return partial


def _build_parameter_tree_dataset(
    parameter_names: list[str], dataset: Dataset, root: DatasetParameterNode
):
    curr = root
    values = [dataset.parameters[name] for name in parameter_names]

    for value in values[:-1]:
        if (next := curr["next"].get(value)) is None:
            next = DatasetParameterNode(next={})
            curr["next"][value] = next

        curr = next

    curr["next"][values[-1]] = None
