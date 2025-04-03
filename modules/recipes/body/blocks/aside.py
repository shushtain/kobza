"""Aside"""

from typing import Any

import pyghtml as html

from .. import blocks


def parse(
    content: Any,
    classes: list,
    id_: str,
) -> html.Aside:
    """Parse aside"""

    aside = html.Aside(class_=classes, id=id_)
    aside += blocks.parse(content, aside)

    return aside
