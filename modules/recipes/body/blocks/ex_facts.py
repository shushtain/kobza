"""Exercise: Facts"""

import pyghtml as html

from ...utils import icon


def parse(
    content: list,
    classes: list,
    id_: str,
) -> html.Div:
    """Parse ex-facts"""

    ex_facts = html.Div(class_=classes + ["exercise", "ex-facts"], id=id_)

    for i, line in enumerate(content):
        task = html.Div(class_=["task"])
        box = html.Button(type="button", class_=["box"]) + (html.Span() + (i + 1))
        dialog = html.Dialog(tabindex="-1")
        modal = html.Div(class_=["wrapper"])

        if isinstance(line, str):
            modal += html.Div(class_=["text"]) + line[1:].strip()
            check = line[0] == "+"
        else:
            img_link = line["img"] if "img" in line else None
            img_alt = line["alt"] if "alt" in line else ""
            check = line["a"]
            modal += html.Img(src=img_link, alt=img_alt)
            modal += html.Div(class_=["text"]) + line["text"]

        false = html.Button(type="button") + "False"
        true = html.Button(type="button") + "True"

        if check:
            true.class_ = ["true"]
        else:
            false.class_ = ["true"]

        buttons = html.Div(class_=["buttons"]) + false + true
        modal += buttons

        modal += html.Button(type="button", class_=["close"]) + icon("close")

        dialog += modal

        task += box
        task += dialog

        ex_facts += task

    return ex_facts
