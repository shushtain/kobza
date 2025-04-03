"""Sitemap generator."""

from modules.utils import sort_recursively


def parse(pages: dict) -> dict:
    """Create a sitemap for lessons."""

    sitemap: dict = {}

    for path, page in pages.items():
        if page["meta"]["type"] != "lesson":
            continue

        topic = page["hero"][0]["content"] if "hero" in page else ""
        grammar = page["grammar"][0]["content"] if "grammar" in page else ""
        vocabulary = page["vocabulary"][0]["content"] if "vocabulary" in page else ""

        level = str(page["meta"]["level"]).lower()
        unit = str(page["meta"]["unit"])
        lesson = str(page["meta"]["lesson"]).lower()

        if level not in sitemap:
            sitemap[level] = {}

        if unit not in sitemap[level]:
            sitemap[level][unit] = {}

        if lesson in sitemap[level][unit]:
            raise ValueError(
                f'{path} is duplicating lesson code "{lesson.upper()}" of {sitemap[level][unit][lesson]["path"]}'
            )

        sitemap[level][unit][lesson] = {
            "topic": topic,
            "grammar": grammar,
            "vocabulary": vocabulary,
            "path": path,
        }

    return sort_recursively(sitemap)
