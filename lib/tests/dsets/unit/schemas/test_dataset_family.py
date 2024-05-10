import json

from dsets.lib.doctree import Reference
from dsets.schemas import (
    Dataset,
    DatasetAttribute,
    DatasetClass,
    DatasetFamily,
    DatasetParameter,
)


class TestDatasetFamily:
    """Tests for `DatasetFamily`."""

    JSON = """
    {
      "slug": "h2-molecule",
      "meta": {
        "title": "H2 Molecule",
        "tags": [
          "qchem"
        ],
        "authors": [
          "Author 1"
        ],
        "changelog": ["Initial release"],
        "abstract": "Abstract...",
        "citation": {
          "$path": "citation.txt"
        },
        "usingThisDataset": {
          "$path": "about.md"
        },
        "license": "GPL"
      },
      "class": {
        "slug": "qchem",
        "name": "Qchem",
        "attributeList": [
          {
            "name": "molecule",
            "pythonType": "Molecule",
            "doc": "The molecule"
          },
          {
            "name": "vqe_params",
            "pythonType": "dict[str, Any]",
            "doc": "VQE Parameters",
            "optional": true
          }
        ],
        "parameterList": [
          {
            "name": "molname",
            "title": "Molecule Name",
            "description": "Name of the molecule"
          },
          {
            "name": "bond_length",
            "title": "Bond Length",
            "description": "Bond length",
            "optional": true
          }
        ]
      },
      "data": [
        {
          "dataUrl": "https://pennylane.ai/datasets/h2.h5",
          "parameters": {
            "molname": "h2",
            "bond_length": "0.5"
          }
        }
      ]
    }
    """

    def test_validate_json(self):
        """Test that a family correctly validates from JSON."""
        family = DatasetFamily.model_validate_json(self.JSON)

        assert family.slug == "h2-molecule"
        assert family.class_ == DatasetClass(
            name="Qchem",
            slug="qchem",
            attribute_list=[
                DatasetAttribute(
                    name="molecule",
                    python_type="Molecule",
                    doc="The molecule",
                    optional=False,
                ),
                DatasetAttribute(
                    name="vqe_params",
                    python_type="dict[str, Any]",
                    doc="VQE Parameters",
                    optional=True,
                ),
            ],
            parameter_list=[
                DatasetParameter(
                    name="molname",
                    title="Molecule Name",
                    description="Name of the molecule",
                    optional=False,
                ),
                DatasetParameter(
                    name="bond_length",
                    title="Bond Length",
                    description="Bond length",
                    optional=True,
                ),
            ],
        )

        assert family.data == [
            Dataset(
                data_url="https://pennylane.ai/datasets/h2.h5",
                parameters={"molname": "h2", "bond_length": "0.5"},
            )
        ]
        meta = family.meta
        assert meta.title == "H2 Molecule"
        assert meta.authors == ["Author 1"]
        assert meta.abstract == "Abstract..."
        assert meta.using_this_dataset == Reference(path="about.md")
        assert meta.citation == Reference(path="citation.txt")

    def test_model_dump_round_trip(self):
        """Test that data is preserved when loading and dumping from
        json."""
        assert DatasetFamily.model_validate_json(self.JSON).model_dump(
            mode="json", exclude_unset=True, by_alias=True
        ) == json.loads(self.JSON)
