"""Description"""

import pyghtml as html

from ..context import ctx


def parse() -> html.Meta:
    """Parse description"""

    description = html.Meta(name="description")

    content = []
    sep = " "

    match ctx.schema:

        case "main":
            content.append(f"{ctx.website}, Open Source English Course.")

        case "404":
            content.append("ERROR 404: Page Not Found.")

        case "level":
            content.append(f"{ctx.website} {ctx.level.upper()}.")
            content.append(f"{len(ctx.sitemap[ctx.level])} units.")

        case "lesson":
            # content.append(f"{WEBSITE} {LEVEL.upper()}.")
            # content.append(f"Unit {UNIT}. Lesson {UNIT + LESSON.upper()}.")
            topic = ctx.sitemap[ctx.level][ctx.unit][ctx.lesson]["topic"]
            grammar = ctx.sitemap[ctx.level][ctx.unit][ctx.lesson]["grammar"]
            vocabulary = ctx.sitemap[ctx.level][ctx.unit][ctx.lesson]["vocabulary"]
            content.append(". ".join([topic, grammar, vocabulary]))

    description.content = sep.join(content)

    return description
