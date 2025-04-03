"""Blocks"""

import pyghtml as html

from ...context import ctx
from .. import inline
from . import (
    aside,
    cta,
    div,
    ex_choice,
    ex_facts,
    ex_format,
    ex_gaps,
    ex_order,
    ex_pref,
    figure,
    flashcards,
    h1,
    h2,
    h3,
    h4,
    hr,
    label,
    note,
    ol,
    p,
    quote,
    section,
    toc,
    ul,
)


def parse(block, scope):
    """Main function for parsing sections"""

    if isinstance(block, list):
        subs = []
        for sub in block:
            subs.append(parse(sub, scope))
        return subs

    if isinstance(block, dict):

        content = block.get("content", None)
        classes = []
        if "class" in block:
            classes = [x for x in block["class"].replace(",", "").split(" ") if x != ""]
        id_ = block.get("id", None)

        match block["type"]:

            case "section":
                return section.parse(
                    content=content,
                    classes=classes,
                    id_=id_,
                )

            case "div":
                return div.parse(
                    content=content,
                    classes=classes,
                    id_=id_,
                )

            case "h1":
                return h1.parse(
                    content=content,
                    classes=classes,
                    id_=id_,
                )

            case "h2":
                return h2.parse(
                    content=content,
                    scope=scope,
                    classes=classes,
                    id_=id_,
                )

            case "h3":
                return h3.parse(
                    content=content,
                    classes=classes,
                    id_=id_,
                )

            case "h4":
                return h4.parse(
                    content=content,
                    classes=classes,
                    id_=id_,
                )

            case "p":
                return p.parse(
                    content=content,
                    classes=classes,
                    id_=id_,
                )

            case "quote":
                return quote.parse(
                    content=content,
                    cite=block.get("cite", None),
                    classes=classes,
                    id_=id_,
                )

            case "aside":
                return aside.parse(
                    content=content,
                    classes=classes,
                    id_=id_,
                )

            case "---":
                return hr.parse(
                    classes=classes,
                    id_=id_,
                )

            case "ul":
                return ul.parse(
                    content=content,
                    classes=classes,
                    id_=id_,
                )

            case "ol":
                return ol.parse(
                    content=content,
                    classes=classes,
                    id_=id_,
                )

            case "cta":
                return cta.parse(
                    content=content,
                    classes=classes,
                    id_=id_,
                )

            case "figure":
                return figure.parse(
                    content=content,
                    classes=classes,
                    id_=id_,
                )

            case "label":
                return label.parse(
                    content=content,
                    classes=classes,
                    id_=id_,
                )

            case "note":
                return note.parse(
                    content=content,
                    classes=classes,
                    id_=id_,
                )

            case "toc":
                return toc.parse(
                    classes=classes,
                    id_=id_,
                )

            case "flashcards":
                return flashcards.parse(
                    content=content,
                    classes=classes,
                    id_=id_,
                )

            case "ex-choice":
                return ex_choice.parse(
                    content=content,
                    classes=classes,
                    id_=id_,
                )

            case "ex-gaps":
                return ex_gaps.parse(
                    content=content,
                    classes=classes,
                    id_=id_,
                )

            case "ex-format":
                return ex_format.parse(
                    content=content,
                    classes=classes,
                    id_=id_,
                )

            case "ex-order":
                return ex_order.parse(
                    content=content,
                    classes=classes,
                    id_=id_,
                )

            case "ex-pref":
                return ex_pref.parse(
                    content=content,
                    classes=classes,
                    id_=id_,
                )

            case "ex-facts":
                return ex_facts.parse(
                    content=content,
                    classes=classes,
                    id_=id_,
                )

            case _:
                return html.CommentHtml() + content

    return inline.parse(block)
