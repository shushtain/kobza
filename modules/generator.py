"""Generate HTML pages from data."""

import os

from modules import prettier, recipes
from modules.recipes.context import ctx


def generate(
    data: dict,
    sitemap: dict,
    path: list,
    url: str,
    version: str,
    fonts: list,
    lang: str,
    paths: dict,
    npx_path: str | None = None,
) -> list:
    """Generate a page from the data."""

    meta = data["meta"]

    ctx.data = data
    ctx.sitemap = sitemap
    ctx.path = path
    ctx.version = version
    ctx.fonts = fonts
    ctx.url = url
    ctx.lang = lang
    ctx.root = "/".join([".." for _ in path[:-1]])[:-1]  # ../../.
    ctx.schema = meta.get("type")
    ctx.level = str(meta.get("level")).lower()
    ctx.unit = str(meta.get("unit"))
    ctx.lesson = str(meta.get("lesson")).lower()
    ctx.paths = paths
    ctx.website = meta.get("book")

    page = recipes.parse()

    file_name = "index.html"
    if ctx.schema == "404":
        file_name = "404.html"

    if npx_path is not None:
        page = prettier.prettify(page, npx_path)

    with open(os.path.join(*path[:-1], file_name), "w", encoding="utf-8") as f:
        f.write(page)

    return path[:-1] + [file_name]
