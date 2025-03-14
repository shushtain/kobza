import json
import os
import asyncio

import pyghtml as html

from _modules import parser

DATA_PATH = "." + os.path.sep
VERSION = "25.02.04"
FONTS = [
    "/_fonts/inter-regular.woff2",
    "/_fonts/inter-regular-italic.woff2",
    "/_fonts/inter-bold.woff2",
    "/_fonts/inter-bold-italic.woff2",
]


def scan(parent_folder) -> list:
    paths = []

    def loop(folder):
        for f in os.listdir(folder):
            if f[:1] == "_" or f[:1] == ".":
                continue
            path = os.path.join(folder, f)
            if os.path.isfile(path) and f.find(".json") != -1:
                paths.append(path.split(os.path.sep))
            elif os.path.isdir(path):
                loop(path)

    loop(parent_folder)

    return paths


def map_pages(paths) -> dict:
    sitemap: dict = {}

    for path in paths:
        if len(path) > 3:

            with open(os.path.join(*path), encoding="utf-8") as f:
                file = f.read()
                data = json.loads(file)

            grammar = data["grammar"][0]["content"] if "grammar" in data else ""
            vocabulary = (
                data["vocabulary"][0]["content"] if "vocabulary" in data else ""
            )

            level = data["meta"]["level"].lower()
            unit = data["meta"]["unit"].lower()
            lesson = data["meta"]["lesson"].lower()

            if level not in sitemap:
                sitemap[level] = {}

            if unit not in sitemap[level]:
                sitemap[level][unit] = {}

            if lesson not in sitemap[level][unit]:
                sitemap[level][unit][lesson] = {}

            sitemap[level][unit][lesson] = {
                "grammar": grammar,
                "vocabulary": vocabulary,
            }

    return sitemap


paths = scan(DATA_PATH)
sitemap = map_pages(paths)


async def compile_page(path, task_index, semaphore):

    async with semaphore:

        with open(os.path.join(*path), encoding="utf-8") as f:
            file = f.read()
            data = json.loads(file)

        meta = data["meta"]

        parser.PATH = path
        parser.PATHS = paths
        parser.SITEMAP = sitemap
        parser.DATA = data
        parser.FONTS = FONTS
        parser.VERSION = VERSION
        parser.WEBSITE = meta["book"] if "book" in meta else ""
        parser.LEVEL = meta["level"].lower() if "level" in meta else ""
        parser.UNIT = meta["unit"].lower() if "unit" in meta else ""
        parser.LESSON = meta["lesson"].lower() if "lesson" in meta else ""
        parser.SCHEMA = meta["type"].lower() if "type" in meta else ""

        file_name = "index.html"

        match meta["type"]:
            case "main":
                page = parser.parse_page()
            case "404":
                page = parser.parse_page()
                file_name = "404.html"
            case "level":
                page = parser.parse_page()
            case "lesson":
                page = parser.parse_page()
            case _:
                page = html.H1(inner_html="CHECK TYPE")

        with open(os.path.join(*path[:-1], file_name), "w", encoding="utf-8") as f:
            f.write(str(html.Doctype()) + str(page))

        print(f"{task_index + 1}/{len(paths)}", os.path.join(*path))


async def main():
    semaphore = asyncio.Semaphore(8)

    print("Compiling...")
    tasks = [
        asyncio.create_task(compile_page(path, i, semaphore))
        for i, path in enumerate(paths)
    ]
    await asyncio.gather(*tasks)
    print("ALL DONE")


if __name__ == "__main__":
    asyncio.run(main())
