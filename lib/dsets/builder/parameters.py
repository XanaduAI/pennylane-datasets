from dsets.schemas import Dataset, DatasetFamily, DatasetParameterNode


def build_parameter_tree(family: DatasetFamily):
    partial = family.parameter_tree
    if partial is None:
        partial = DatasetParameterNode(next={})

    for dataset in family.data:
        _build_parameter_tree_dataset(dataset, partial)

    return partial


def _build_parameter_tree_dataset(dataset: Dataset, root: DatasetParameterNode):
    curr = root
    values = list(dataset.parameters.values())

    for value in values[:-1]:
        if (next := curr["next"].get(value)) is None:
            next = DatasetParameterNode(next={})
            curr["next"][value] = next

        curr = next

    curr["next"][values[-1]] = None
