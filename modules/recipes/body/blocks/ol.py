"""Ordered List"""

import pyghtml as html

from .. import blocks


def parse(
    content: list,
    classes: list,
    id_: str,
) -> html.Ol:
    """Parse ol"""

    ol = html.Ol(class_=classes, id=id_)

    for item in content:
        li = html.Li()
        ol += li + blocks.parse(item, li)

    return ol
