import json
from datetime import datetime

from dsets.lib.json_ref import DocumentRef
from dsets.lib.time import utcnow
from dsets.schemas import DatasetFamily, DatasetType


class TestDatasetFamily:
    """Tests for `DatasetFamily`."""

    JSON = """
    {
      "title": "H2 Molecule",
      "slug": "h2-molecule",
      "tags": [
        "qchem"
      ],
      "authors": [
        "Author 1"
      ],
      "dateOfPublication": "2024-02-29T16:54:15.783903Z",
      "dateOfLastModification": "2024-02-29T16:54:15.783903Z",
      "citation": {
        "$ref": "citation.txt"
      },
      "about": {
        "$ref": "about.md"
      },
      "type": {
        "name": "qchem",
        "attributeList": [],
        "parameterLabels": ["molname", "basis", "bondlength"]},
      "data": []
    }
    """

    def test_validate_json(self):
        dataset = DatasetFamily.model_validate_json(self.JSON)

        assert dataset.title == "H2 Molecule"
        assert dataset.slug == "h2-molecule"
        assert dataset.authors == ["Author 1"]
        assert dataset.date_of_publication == datetime.fromisoformat(
            "2024-02-29T16:54:15.783903Z"
        )
        assert dataset.date_of_last_modification == datetime.fromisoformat(
            "2024-02-29T16:54:15.783903Z"
        )
        assert dataset.about == DocumentRef(ref="about.md")
        assert dataset.citation == DocumentRef(ref="citation.txt")
        assert dataset.data == []

    def test_init(self):
        DatasetFamily(
            title="title",
            slug="slug",
            authors=["author"],
            tags=["tag"],
            citation=DocumentRef[str](ref="citatation.txt"),
            about=DocumentRef[str](ref="about.md"),
            type_=DatasetType(name="type", attribute_list=[]),
            date_of_publication=utcnow(),
            date_of_last_modification=utcnow(),
            parameter_labels=["param1", "param2", "param3"],
            parameter_defaults={"val1": "val2", "val1,val2": "val3"},
            data=[],
        )

    def test_model_dump(self):
        assert DatasetFamily.model_validate_json(self.JSON).model_dump(
            mode="json", exclude_unset=True, by_alias=True
        ) == json.loads(self.JSON)
