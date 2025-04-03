"""Header"""

import pyghtml as html

from ..context import ctx
from ..utils import icon, link


def parse() -> html.Header:
    """Parse header"""

    header = html.Header()

    nav = html.Nav(aria_attrs={"aria-label": "Primary"})
    nav += html.A(
        href="#main",
        class_=["button", "skip"],
        inner_html=html.Span() + "Skip to content",
    )

    nav += html.A(
        href=link(ctx.root),
        class_=["button", "accent"],
        aria_attrs={"aria-label": "Kobza Home"},
        inner_html=html.Span() + "Kobza",
    )

    if ctx.schema == "lesson":
        nav += html.A(
            href=link(ctx.root, ctx.level),
            class_=["button"],
            inner_html=html.Span() + ctx.level.upper(),
        )

    # color mode toggle
    toggle_theme = html.Button(
        type="button",
        id="toggle-theme",
        aria_attrs={"aria-label": "Toggle theme"},
    )
    toggle_theme += icon("light-mode", "toggle-light")
    toggle_theme += icon("dark-mode", "toggle-dark")

    header += nav
    header += html.Noscript() + "Some features require JavaScript."
    header += toggle_theme

    return header
