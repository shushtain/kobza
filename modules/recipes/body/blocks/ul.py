"""Unordered List"""

import pyghtml as html

from .. import blocks


def parse(
    content: list,
    classes: list,
    id_: str,
) -> html.Ul:
    """Parse ul"""

    ul = html.Ul(class_=classes, id=id_)

    for item in content:
        li = html.Li()
        ul += li + blocks.parse(item, li)

    return ul
