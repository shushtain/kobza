"""Heading 4"""

import pyghtml as html

from .. import inline


def parse(
    content: str,
    classes: list,
    id_: str,
) -> html.H4:
    """Parse h4"""

    h4 = html.H4(class_=classes, id=id_)
    h4 += inline.parse(content)

    return h4
