"""Utilities for the recipes."""

import pyghtml as html

from .context import ctx


def link(*parts):
    """Join parts of a path and return it"""
    return "/".join(parts)


def icon(
    icon_name: str,
    id_: str | None = None,
    classes: list[str | None] | None = None,
):
    """Return an icon"""
    svg = html.Svg(class_=["icon"] + (classes if classes else []), id=id_)
    use = html.Use(href=link(ctx.root, *ctx.paths["icons"], f"sprite.svg#{icon_name}"))
    svg += use
    return f"\n{svg}\n"
