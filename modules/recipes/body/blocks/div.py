"""Div"""

from typing import Any

import pyghtml as html

from .. import blocks


def parse(
    content: Any,
    classes: list,
    id_: str,
) -> html.Div:
    """Parse div"""

    div = html.Div(class_=classes, id=id_)

    div += blocks.parse(content, div)

    return div
