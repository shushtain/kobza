"""Heading 3"""

import pyghtml as html

from .. import inline


def parse(
    content: str,
    classes: list,
    id_: str,
) -> html.H3:
    """Parse h3"""

    h3 = html.H3(class_=classes, id=id_)

    h3 += inline.parse(content)

    return h3
