"""Title"""

import pyghtml as html

from ..context import ctx


def parse() -> html.Title:
    """Parse title"""

    title = html.Title()

    content = []
    sep = " • "

    match ctx.schema:

        case "main":
            content.append(ctx.website)

        case "404":
            content.append("404 NOT FOUND")
            content.append(ctx.website)

        case "level":
            content.append(f"Level {ctx.level.upper()}")
            content.append(ctx.website)

        case "lesson":
            content.append(f"Lesson {ctx.unit}{ctx.lesson.upper()}")
            content.append(f"Level {ctx.level.upper()}")
            content.append(ctx.website)

    title += sep.join(content)

    return title
