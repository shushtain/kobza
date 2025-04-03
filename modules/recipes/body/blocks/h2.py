"""Heading 2"""

import pyghtml as html

from ...context import ctx
from .. import inline


def parse(
    content: str,
    scope: html.Section,
    classes: list,
    id_: str,
) -> html.H2:
    """Parse h2"""

    h2 = html.H2(class_=classes, id=id_)

    match ctx.schema:

        case "lesson":
            if content == "":
                if scope.id:
                    h2 += f"{scope.id.capitalize()}"
            else:
                if scope.id:
                    h2 += html.Span() + f"{scope.id.capitalize()}:"
                h2 += html.Br()
            h2 += inline.parse(content)

        case _:
            h2 += inline.parse(content)

    return h2
