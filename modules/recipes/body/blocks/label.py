"""Label"""

import pyghtml as html

from .. import inline


def parse(
    content: str,
    classes: list,
    id_: str,
) -> html.P:
    """Parse label"""

    label = html.P(class_=["label"] + classes, id=id_)

    label += inline.parse(content)

    return label
