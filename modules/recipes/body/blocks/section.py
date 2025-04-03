"""Section"""

import pyghtml as html

from .. import blocks


def parse(
    content: list,
    classes: list,
    id_: str,
) -> html.Section:
    """Parse section"""

    section = html.Section(class_=classes, id=id_)

    section += blocks.parse(content, section)

    return section
