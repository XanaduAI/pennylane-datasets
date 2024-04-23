import inspect
import re

import pytest
from dsets.schemas.fields import BibtexStr, PythonIdentifier, Slug
from pydantic import TypeAdapter, ValidationError


@pytest.mark.parametrize("val", ["a", "a_variable", "a1", "A1", "A"])
def test_python_identifier(val):
    """Check that valid python identifiers pass validation."""

    assert TypeAdapter(PythonIdentifier).validate_python(val) == val


@pytest.mark.parametrize(
    "val", ["1", "1a", "kabob-case", "'string?", '"string?', "'string'", "if", "return"]
)
def test_python_identifier_invalid(val):
    """Check that invalid Python identifiers fail validation."""

    with pytest.raises(
        ValidationError,
        match=f".*Not a valid Python identifier: {re.escape(repr(val))}.*",
    ):
        TypeAdapter(PythonIdentifier).validate_python(val)


@pytest.mark.parametrize(
    "val",
    [
        inspect.cleandoc(
            """
            % comment!!
            @misc{bergholm2022pennylane,
            title = {PennyLane: Automatic differentiation of hybrid quantum-classical computations}, 
            author = {Ville Bergholm and Josh Izaac and Maria Schuld and Christian Gogolin and Shahnawaz Ahmed and Vishnu Ajith and M. Sohaib Alam and Guillermo Alonso-Linaje and B. AkashNarayanan and Ali Asadi and Juan Miguel Arrazola and Utkarsh Azad and Sam Banning and Carsten Blank and Thomas R Bromley and Benjamin A. Cordier and Jack Ceroni and Alain Delgado and Olivia Di Matteo and Amintor Dusko and Tanya Garg and Diego Guala and Anthony Hayes and Ryan Hill and Aroosa Ijaz and Theodor Isacsson and David Ittah and Soran Jahangiri and Prateek Jain and Edward Jiang and Ankit Khandelwal and Korbinian Kottmann and Robert A. Lang and Christina Lee and Thomas Loke and Angus Lowe and Keri McKiernan and Johannes Jakob Meyer and J. A. Montañez-Barrera and Romain Moyard and Zeyue Niu and Lee James O'Riordan and Steven Oud and Ashish Panigrahi and Chae-Yeun Park and Daniel Polatajko and Nicolás Quesada and Chase Roberts and Nahum Sá and Isidor Schoch and Borun Shi and Shuli Shu and Sukin Sim and Arshpreet Singh and Ingrid Strandberg and Jay Soni and Antal Száva and Slimane Thabet and Rodrigo A. Vargas-Hernández and Trevor Vincent and Nicola Vitucci and Maurice Weber and David Wierichs and Roeland Wiersema and Moritz Willmann and Vincent Wong and Shaoming Zhang and Nathan Killoran},
            year = {2022},
            eprint = {1811.04968},
            archivePrefix = {arXiv},
            primaryClass = {quant-ph}
            }
            """
        )
    ],
)
def test_bibtex_str_valid(val):
    """Check that a valid bibtex string (with an entry) passes validation."""

    assert TypeAdapter(BibtexStr).validate_python(val) == val


@pytest.mark.parametrize("val", ["implicit comment", "@comment{}"])
def test_bibtex_str_invalid(val):
    """Check that a Bibtex string with no entries fails validation."""

    with pytest.raises(ValidationError, match=r".*Bibtex citation has no entries.*"):
        TypeAdapter(BibtexStr).validate_python(val)


@pytest.mark.parametrize("val", ["x", "1slug", "1x", "x-y", "z-1y-x", "my-slug"])
def test_slug_valid(val):
    """Test that a valid slug passes validation."""
    assert TypeAdapter(Slug).validate_python(val) == val


@pytest.mark.parametrize(
    "val", ["a_z", "A_z", "az-", "-az-x", "A-Z", " x-y", " x", "x ", "x-yand "]
)
def test_slug_invalid(val):
    """Check that an invalid slug fails validation."""

    with pytest.raises(ValidationError, match=r".*String should match pattern.*"):
        TypeAdapter(Slug).validate_python(val)
