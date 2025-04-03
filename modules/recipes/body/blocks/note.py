"""Note"""

import pyghtml as html

from .. import inline


def parse(
    content: str,
    classes: list,
    id_: str,
) -> html.P:
    """Parse note"""

    note = html.P(class_=["note"] + classes, id=id_)

    note += inline.parse(content)

    return note
