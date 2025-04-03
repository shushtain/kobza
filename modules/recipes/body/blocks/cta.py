"""Call to Action"""

import pyghtml as html

from ...context import ctx
from ...utils import icon, link


def parse(
    content: dict,
    classes: list,
    id_: str,
) -> html.A:
    """Parse Call to Action"""

    cta = html.A(class_=classes + ["button"], id=id_)

    text = content.get("text", "")
    title = content.get("title", None)
    href = content.get("link", "")
    if href.startswith("/"):
        href = link(ctx.root, href[1:])
    target = content.get("target", None)
    if href.startswith("http"):
        target = "_blank"

    if "mail" in classes or "mailto:" in href:
        cta += icon("mail")
        target = "_blank"
    elif "file" in classes:
        cta += icon("file")
        target = "_blank"

    cta.href = href
    cta.title = title
    cta.target = target
    cta += html.Span() + text

    if "download" in classes:
        cta += icon("download")
        cta.target = "_blank"
    elif "more" in classes:
        cta += icon("arrow-right")

    return cta
