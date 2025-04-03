"""Exercise: Preferences"""

import pyghtml as html

from ...utils import icon


def parse(
    content: list,
    classes: list,
    id_: str,
) -> html.Div:
    """Parse ex-pref"""

    ex_pref = html.Div(class_=classes + ["exercise", "ex-pref"], id=id_)

    for i, line in enumerate(content):
        task = html.Div(class_=["task"])
        box = html.Button(type="button", class_=["box"]) + (html.Span() + (i + 1))
        dialog = html.Dialog(tabindex="-1")
        modal = html.Div(class_=["wrapper"])

        if isinstance(line, str):
            modal += html.Div(class_=["text"]) + line
        else:
            img_link = line["img"] if "img" in line else None
            img_alt = line["alt"] if "alt" in line else ""
            modal += html.Img(src=img_link, alt=img_alt)
            modal += html.Div(class_=["text"]) + line["text"]

        dislike = html.Button(type="button", class_=["dislike", "error"]) + icon(
            "thumb-down"
        )
        like = html.Button(type="button", class_=["like", "success"]) + icon("thumb-up")
        buttons = html.Div(class_=["buttons"]) + dislike + like
        modal += buttons

        modal += html.Button(type="button", class_=["close"]) + icon("close")

        dialog += modal

        task += box
        task += dialog

        ex_pref += task

    return ex_pref
