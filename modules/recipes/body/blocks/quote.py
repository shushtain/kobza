"""Blockquote"""

import pyghtml as html

from .. import inline


def parse(
    content: str,
    cite: str | None,
    classes: list,
    id_: str,
) -> html.Blockquote:
    """Parse blockquote"""

    blockquote = html.Blockquote(class_=classes, id=id_)
    blockquote += html.P() + inline.parse(content)

    if cite is not None:
        blockquote += html.Cite() + inline.parse(cite)

    return blockquote
