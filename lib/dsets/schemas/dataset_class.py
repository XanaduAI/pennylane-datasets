from typing import Self

from pydantic import BaseModel, model_validator

from dsets.lib.doctree import Document
from dsets.lib.pydantic_util import CamelCaseMixin

from .fields import PythonIdentifier


class DatasetAttribute(BaseModel, CamelCaseMixin):
    """Model for a ``DatasetType.attribute_list``.

    Attributes:
        name: Name of the attribute. Must be a legal python
            variable name
        python_type: Python type for this attribute. May
            contain markdown
        doc: Docstring for this attribute
        optional: Whether this attribute can be omitted
            from the dataset instance
    """

    name: PythonIdentifier
    python_type: str
    doc: str
    optional: bool = False


class DatasetParameter(BaseModel, CamelCaseMixin):
    """Model for a dataset parameter.
    Attributes:
        name: Short name for the parameter. Must be a legal
            python variable name
        title: Optional human-readable name for the parameter
        description: Text describing the parameter
        optional: Whether this parameter may be undefined
            for a dataset
    """

    name: PythonIdentifier
    title: str
    description: str | None = None
    optional: bool = False


class DatasetClass(Document, CamelCaseMixin):
    """Model for a class of datasets, e.g 'Qchem', 'Qspin'.

    Attributes:
        name: Unique name for this class
        attribute_list: List of expected attributes on
            a dataset instance that has this class
        parameter_list: List of expected parameters on
            a dataset instance that has this class
    """

    name: PythonIdentifier
    attribute_list: list[DatasetAttribute] = []
    parameter_list: list[DatasetParameter] = []

    @property
    def attributes(self) -> dict[str, DatasetAttribute]:
        return {attribute.name: attribute for attribute in self.attribute_list}

    @property
    def parameters(self) -> dict[str, DatasetParameter]:
        return {parameter.name: parameter for parameter in self.parameter_list}

    @model_validator(mode="after")
    def _validate_attributes_parameters(self: Self) -> Self:
        dupe_attr_names = Counter(self.attribute_list) - Counter(set(self.attribute_list))
        if dupe_attr_names:
            dupe_name = next(iter(dupe_attr_names))
            raise ValueError(f"Duplicate attribute names: {dupe_name}")

        parameter_names = set()
        for parameter in self.parameter_list:
            if parameter.name in parameter_names:
                raise ValueError(f"Duplicate parameter name: {parameter.name}")

            parameter_names.add(parameter.name)

        return self
