"""Head"""

import pyghtml as html

from ..utils import link
from . import description, title
from ..context import ctx


def parse() -> html.Head:
    """Parse head"""
    head = html.Head()

    # Encoding and viewport
    head += html.CommentHtml("Encoding and viewport")
    head += html.Meta(charset="utf-8")
    head += html.Meta(
        name="viewport",
        content="width=device-width, initial-scale=1.0",
    )

    # Primary meta tags
    head += html.CommentHtml("Primary meta tags")
    page_title = title.parse()
    head += page_title
    page_descr = description.parse()
    head += page_descr
    head += html.Meta(name="author", content="Artem Shush")

    # Open Graph
    head += html.CommentHtml("Open Graph")
    head += html.Meta(property="og:type", content="website")
    head += html.Meta(
        property="og:url",
        content=link(ctx.url, *ctx.path[1:-1]),
    )
    head += html.Meta(
        property="og:title",
        content=page_title.inner_html,
    )
    head += html.Meta(
        property="og:description",
        content=page_descr.content,
    )
    head += html.Meta(
        property="og:image",
        content=link(ctx.url, *ctx.paths["images"], "og-image.png"),
    )

    # Use the latest IE engine
    head += html.CommentHtml("Use the latest IE engine")
    head += html.Meta(http_equiv="X-UA-Compatible", content="IE=edge")

    # Preload fonts
    head += html.CommentHtml("Preload fonts")
    for font in ctx.fonts:
        head += html.Link(
            rel="preload",
            href=link(ctx.root, *font[1:]),
            as_="font",
            type="font/woff2",
            crossorigin=True,
        )

    # Preload font styles
    head += html.CommentHtml("Preload font styles")
    head += html.Link(
        rel="preload",
        href=link(ctx.root, *ctx.paths["styles"], "fonts.css?ver=" + ctx.version),
        as_="style",
    )

    # Specify color scheme
    head += html.CommentHtml("Specify color scheme")
    head += html.Meta(name="color-scheme", content="light dark")
    # and theme color for pwa
    head += html.Meta(
        name="theme-color",
        media="(prefers-color-scheme: light)",
        content="#e6e6e6",
    )
    head += html.Meta(
        name="theme-color",
        media="(prefers-color-scheme: dark)",
        content="#0d0d0d",
    )

    # Load styles
    head += html.CommentHtml("Load styles")
    head += html.Link(
        rel="stylesheet",
        href=link(ctx.root, *ctx.paths["styles"], "fonts.css?ver=" + ctx.version),
    )
    head += html.Link(
        rel="stylesheet",
        href=link(ctx.root, *ctx.paths["styles"], "main.css?ver=" + ctx.version),
    )

    # Load scripts
    head += html.CommentHtml("Load scripts")
    head += html.Script(
        src=link(ctx.root, *ctx.paths["scripts"], "main.js"),
    )
    if ctx.schema == "lesson":
        head += html.Script(
            src=link(ctx.root, *ctx.paths["scripts"], "lesson.js"),
            type="module",
            defer=True,
        )

    # Add favicons
    head += html.CommentHtml("Add favicons")
    head += html.Link(
        rel="icon",
        sizes="192x192",
        href=link(ctx.root, *ctx.paths["icons"], "kobza-icon-192x192.png"),
    )
    head += html.Link(
        rel="apple-touch-icon",
        sizes="180x180",
        href=link(ctx.root, *ctx.paths["icons"], "kobza-icon-180x180.png"),
    )
    head += html.Link(
        rel="icon",
        sizes="96x96",
        href=link(ctx.root, *ctx.paths["icons"], "kobza-icon-96x96.png"),
    )

    # Manifest
    head += html.CommentHtml("Manifest")
    head += html.Link(
        rel="manifest",
        href=link(ctx.root, "site.webmanifest"),
    )

    return head
