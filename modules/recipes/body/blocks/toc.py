"""Table of Contents"""

import pyghtml as html

from ...context import ctx
from ...utils import link


def parse(
    classes: list,
    id_: str,
) -> html.Div:
    """Parse Table of Contents"""

    toc = html.Div(class_=classes + ["toc"], id=id_)
    toc.id = f"toc-{ctx.schema}" if id_ is None else id_

    match ctx.schema:

        case "main":
            for level in ctx.sitemap:
                card = html.A(
                    href=link(ctx.root, level),
                    class_=["tile", level],
                )
                text = html.Span() + level.upper()
                toc += card + text

        case "level":
            for unit, lessons in ctx.sitemap[ctx.level].items():
                ul = html.Ul()
                for lesson, topics in lessons.items():
                    card = html.A(
                        href=link(ctx.root, ctx.level, unit + lesson),
                        class_=["button"],
                    )
                    text = html.Span() + ". ".join(
                        [
                            f"Lesson {unit + lesson.upper()}",
                            topics["topic"],
                            # topics["grammar"],
                            # topics["vocabulary"],
                        ]
                    )
                    text += html.Br()
                    text += html.Small() + ". ".join(
                        [topics["grammar"], topics["vocabulary"]]
                    )
                    card += text
                    ul += html.Li() + card
                toc += html.Section() + html.H3(inner_html=f"Unit {unit}") + ul

    return toc
