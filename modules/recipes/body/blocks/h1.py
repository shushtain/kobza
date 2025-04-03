"""Heading 1"""

import pyghtml as html

from ...context import ctx
from .. import inline


def parse(
    content: str,
    classes: list,
    id_: str,
) -> html.H1:
    """Parse h1"""

    h1 = html.H1(class_=classes, id=id_)

    match ctx.schema:

        case "lesson":
            h1 += html.Span() + f"Lesson {ctx.unit}{ctx.lesson.upper()}:"
            h1 += html.Br()
            h1 += inline.parse(content)

        case _:
            h1 += inline.parse(content)

    return h1
