"""Figure"""

import pyghtml as html

from .. import inline


def parse(
    content: dict,
    classes: list,
    id_: str,
) -> html.Figure:
    """Parse figure"""

    figure = html.Figure(class_=classes, id=id_)

    src = content["img"]
    alt = content["alt"] if "alt" in content else ""
    figure += html.Img(src=src, alt=alt)

    if "caption" in content:
        caption = inline.parse(content["caption"])
        figure += html.Figcaption(class_=["subtle"]) + caption

    return figure
