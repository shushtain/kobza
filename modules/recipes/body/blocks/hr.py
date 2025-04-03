"""Horizontal Divider"""

import pyghtml as html


def parse(
    classes: list,
    id_: str,
) -> html.Hr:
    """Parse hr"""

    hr = html.Hr(class_=classes, id=id_)

    return hr
