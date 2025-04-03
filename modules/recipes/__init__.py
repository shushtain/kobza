"""Parses Python objects into HTML pages."""

import pyghtml as html

from . import body, head
from .context import ctx


def parse() -> str:
    """Parse a page."""

    page = html.Html(lang=ctx.lang)

    page += head.parse()
    page += body.parse()

    return str(html.Doctype()) + str(page)
