from datetime import date
from inspect import cleandoc

TEMPLATE = cleandoc(
    """
    @misc{{{key},
        title={{{title}}},
        author={{{authors}}},
        howpublished={{\\url{publication_url}}},
        year={{{year}}}
    }}
"""
)


def generate_bibtex(
    slug: str, title: str, authors: list[str], publication_url: str
) -> str:
    year = str(date.today().year)
    key = f"{authors[0]}{year}{slug.replace('-', '')}"

    authorlist = " and ".join(authors)

    return TEMPLATE.format(
        key=key,
        title=title,
        authors=authorlist,
        year=year,
        publication_url=publication_url,
    )
