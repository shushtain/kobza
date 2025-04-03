"""Paragraph"""

from typing import Any

import pyghtml as html

from .. import blocks


def parse(
    content: Any,
    classes: list,
    id_: str,
) -> html.P:
    """Parse p"""

    p = html.P(class_=classes, id=id_)

    p += blocks.parse(content, p)

    return p
