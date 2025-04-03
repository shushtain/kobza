"""Flashcards"""

import pyghtml as html

from ...utils import icon


def parse(
    content: list,
    classes: list,
    id_: str,
) -> html.Div:
    """Parse flashcards"""

    flashcards_wrapper = html.Div(class_=["flashcards-wrapper"])

    # controls

    flashcards_controls = html.Div(class_=["controls"])
    toggle_flashcards = html.Button(
        type="button", class_=["button", "toggle-flashcards"]
    )
    toggle_flashcards += icon("show", classes=["toggle-show"])
    toggle_flashcards += icon("hide", classes=["toggle-hide"])
    toggle_flashcards += html.Span() + "Show answers"
    flashcards_controls += toggle_flashcards

    flashcards_wrapper += flashcards_controls

    # flashcards

    flashcards = html.Div(class_=classes + ["flashcards"], id=id_)

    for item in content:
        term = item["q"]
        definition = item["a"]
        img_link = item["img"] if "img" in item else None
        img_alt = item["alt"] if "alt" in item else ""

        card = html.Div(class_=["flashcard", "tile"], tabindex="0")

        if img_link:
            card += html.Img(src=img_link, alt=img_alt)

        dl = html.Dl()
        dl += html.Dt() + term
        if isinstance(definition, list):
            for line in definition:
                dl += html.Dd() + line
        else:
            dl += html.Dd() + definition

        card += dl
        flashcards += card

    flashcards_wrapper += flashcards

    return flashcards_wrapper
