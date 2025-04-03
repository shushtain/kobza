"""Footer"""

import pyghtml as html

from ..context import ctx
from ..utils import icon, link


def parse() -> html.Footer:
    """Footer from the Body"""

    footer = html.Footer()

    nav = html.Nav(aria_attrs={"aria-label": "Secondary"})

    nav_prev = html.A(class_=["button", "disabled"])
    nav_next = html.A(class_=["button", "disabled"])

    # Secondary navigation
    if ctx.schema == "lesson":

        lessons: list = []
        for unit in ctx.sitemap[ctx.level]:
            for lesson in ctx.sitemap[ctx.level][unit]:
                lessons.append([unit, lesson])

        lesson_prev_index = lessons.index([ctx.unit, ctx.lesson]) - 1
        lesson_next_index = lessons.index([ctx.unit, ctx.lesson]) + 1

        if lesson_prev_index >= 0:
            lesson_prev = lessons[lesson_prev_index]
            truncated = "".join(lesson_prev).upper()
            lesson_prev_link = link(ctx.root, ctx.level, "".join(lesson_prev))
            lesson_prev_text = ". ".join(
                [
                    f"Lesson {truncated}",
                    ctx.sitemap[ctx.level][lesson_prev[0]][lesson_prev[1]]["topic"],
                    # SITEMAP[LEVEL][lesson_prev[0]][lesson_prev[1]]["grammar"],
                    # SITEMAP[LEVEL][lesson_prev[0]][lesson_prev[1]]["vocabulary"],
                ]
            )
            nav_prev = html.A(
                href=lesson_prev_link,
                class_=["button", "prev"],
                aria_attrs={"aria-label": "Previous lesson"},
            )
            nav_prev += icon("arrow-left")
            nav_prev += html.Span(class_=["long"]) + lesson_prev_text
            nav_prev += html.Span(class_=["short"]) + truncated

        if lesson_next_index < len(lessons):
            lesson_next = lessons[lesson_next_index]
            truncated = "".join(lesson_next).upper()
            lesson_next_link = link(ctx.root, ctx.level, "".join(lesson_next))
            lesson_next_text = ". ".join(
                [
                    f"Lesson {truncated}",
                    ctx.sitemap[ctx.level][lesson_next[0]][lesson_next[1]]["topic"],
                    # SITEMAP[LEVEL][lesson_next[0]][lesson_next[1]]["grammar"],
                    # SITEMAP[LEVEL][lesson_next[0]][lesson_next[1]]["vocabulary"],
                ]
            )
            nav_next = html.A(
                href=lesson_next_link,
                class_=["button", "next"],
                aria_attrs={"aria-label": "Next lesson"},
            )
            nav_next += html.Span(class_=["long"]) + lesson_next_text
            nav_next += html.Span(class_=["short"]) + truncated
            nav_next += icon("arrow-right")

    nav_up = html.A(
        href="#",
        class_=["button", "up"],
        aria_attrs={"aria-label": "To the top"},
    )
    nav_up += icon("arrow-up")

    nav += nav_prev
    nav += nav_up
    nav += nav_next

    footer += nav

    # # Back navigation
    # if len(PATH) > 2:
    #     path_parent = link(ROOT, *[crumb for crumb in PATH[1:-2]])

    #     nav_back = html.Nav(class_=["back"], aria_attrs={"aria-label": "Back"})
    #     nav_back += html.A(
    #         href=path_parent,
    #         class_=["button", "back"],
    #         inner_html=html.Span() + "Back",
    #     )

    #     footer += nav_back

    # Contacts
    footer += html.A(
        href="https://github.com/shushtain/kobza",
        class_=["credits"],
        inner_html=html.Small() + "Kobza, MIT 2025",
    )

    return footer
