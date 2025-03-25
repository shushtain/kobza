"""Generate HTML from data files."""

import os
import argparse
import subprocess
import shutil
import asyncio  # Add asyncio import
import json
import re
from functools import partial  # Add partial import

import pyghtml as html
import colson

from _modules import parser
from _modules import crawler
from _modules.utils import sort_recursively, update_version

SEP = os.path.sep
ROOT = "."  # true root is `.` to work with relative paths
ROOT_ABS = "https://shushtain.github.io/kobza"
FONTS_FOLDER = "fonts"
DATA_FILES_PATTERN = r"\.colson$"
FONT_FILES_PATTERN = r"\.woff2$"

SEMAPHORE_LIMIT = 8


async def main() -> None:
    """Does everything. Hurts nobody?"""

    # command line interface tab size
    cli_tab = " " * 2

    # check for arguments
    args = add_args()

    # update version
    version = update_version(
        new_patch=args["patch"],
        new_minor=args["minor"],
        new_major=args["major"],
        root=ROOT,
    )

    # check for npx
    npx_path: str | None = None
    if args["format"]:
        npx_path = shutil.which("npx")
        if npx_path is None:
            raise FileNotFoundError("npx not found. Cannot format HTML without it.")

    # * START FEEDBACK
    if True in args.values():
        modes = [key for key, value in args.items() if value]
        print(f"Compiling mode: {', '.join(modes)}")
    if args["dir"] is not None:
        print(f"Directory focus: {args['dir']}")
    print(f"Compiling v{version}...\n")

    # find fonts
    print(f"{cli_tab}Finding fonts...")
    fonts: list = crawler.crawl(os.path.join(ROOT, FONTS_FOLDER), FONT_FILES_PATTERN)
    for font in fonts:
        print(f"{cli_tab}{cli_tab}{os.path.join(*font[1:])}")
    print(f"{cli_tab}Found {len(fonts)} fonts.\n")

    # find appropriate data files
    print(f"{cli_tab}Finding files...")
    paths: list = crawler.crawl(ROOT, DATA_FILES_PATTERN)
    # filter by directory if needed
    if args["dir"] is not None:
        new_paths = []
        for path in paths:
            if len(path) == 2 or args["dir"] in path:
                new_paths.append(path)
        paths = new_paths
    for i, path in enumerate(paths):
        print(f"{cli_tab}{cli_tab}{i+1}/{len(paths)} {os.path.join(*path[1:])}")
    if len(paths) != 0:
        print(f"{cli_tab}Files found.\n")
    else:
        print(f"{cli_tab}No files found.\n")
        print("Nothing to compile.")
        return

    # load data
    print(f"{cli_tab}Gathering data...")
    data: dict = {}
    for i, path in enumerate(paths):
        with open(os.path.join(*path), encoding="utf-8") as f:
            file = f.read()
        data[os.path.join(*path)] = colson.loads(file)
        print(f"{cli_tab}{cli_tab}{i+1}/{len(paths)} {os.path.join(*path[1:])}")
    print(f"{cli_tab}Data gathered.\n")

    # parse into JSON
    if args["json"]:
        ascii_mode = "ASCII" if args["ascii"] else "UTF-8"
        print(f"{cli_tab}Parsing into JSON ({ascii_mode})...")
        for i, path in enumerate(paths):
            new_file_name = re.sub(DATA_FILES_PATTERN, ".json", path[-1])
            new_path = os.path.join(*path[:-1], new_file_name)
            with open(new_path, "w", encoding="utf-8") as f:
                f.write(
                    json.dumps(
                        data[os.path.join(*path)],
                        ensure_ascii=args["ascii"],
                        indent=2,
                    )
                )
            print(
                f"{cli_tab}{cli_tab}{i+1}/{len(paths)} {os.path.join(*path[1:-1], new_file_name)}"
            )
        print(f"{cli_tab}Parsed into JSON.\n")

    # map lessons
    print(f"{cli_tab}Mapping lessons...")
    sitemap: dict = map_lessons(data)
    print(f"{cli_tab}Lessons mapped.\n")

    # generate pages
    print(f"{cli_tab}Generating pages (async)...")

    semaphore = asyncio.Semaphore(SEMAPHORE_LIMIT)

    async def generate_with_semaphore(
        path, paths, data, sitemap, version, fonts, npx_path, index, total
    ):
        async with semaphore:
            new_path = await asyncio.to_thread(
                partial(
                    generate_page,
                    path=path,
                    paths=paths,
                    data=data,
                    sitemap=sitemap,
                    version=version,
                    fonts=fonts,
                    npx_path=npx_path,
                )
            )
            print(
                f"{cli_tab}{cli_tab}{index + 1}/{total} {os.path.join(*new_path[1:])}"
            )
            return new_path

    tasks = [
        generate_with_semaphore(
            path=path,
            paths=paths,
            data=data[os.path.join(*path)],
            sitemap=sitemap,
            version=version,
            fonts=fonts,
            npx_path=npx_path,
            index=i,
            total=len(paths),
        )
        for i, path in enumerate(paths)
    ]
    await asyncio.gather(*tasks)
    print(f"{cli_tab}Pages generated.\n")

    # * END FEEDBACK
    print("Compiled successfully.")
    # exit


def add_args() -> dict:
    """Parse command line arguments."""

    arg_parser = argparse.ArgumentParser(description="Compile ColSON into HTML.")

    arg_parser.add_argument(
        "-f",
        "--format",
        action="store_true",
        help="Format compiled HTML with Prettier.",
    )

    arg_parser.add_argument(
        "-j",
        "--json",
        action="store_true",
        help="Parse into JSON files as well.",
    )

    arg_parser.add_argument(
        "-a",
        "--ascii",
        action="store_true",
        help="Ensure ascii for JSON files if `-j` is provided.",
    )

    arg_parser.add_argument(
        "-p",
        "--patch",
        action="store_true",
        help="Increment the patch version.",
    )

    arg_parser.add_argument(
        "-m",
        "--minor",
        action="store_true",
        help="Increment the minor version.",
    )

    arg_parser.add_argument(
        "-M",
        "--major",
        action="store_true",
        help="Increment the major version.",
    )

    arg_parser.add_argument(
        "-d",
        "--dir",
        type=str,
        help="Compile a specific subdirectory. Includes root files.",
    )

    arg_parsed = arg_parser.parse_args()

    args: dict = {}
    args["format"] = arg_parsed.format
    args["json"] = arg_parsed.json
    args["ascii"] = arg_parsed.ascii
    args["patch"] = arg_parsed.patch
    args["minor"] = arg_parsed.minor
    args["major"] = arg_parsed.major
    args["dir"] = arg_parsed.dir
    return args


def map_lessons(data: dict) -> dict:
    """Create a sitemap for lessons."""

    sitemap: dict = {}

    for path, page in data.items():
        if "lesson" not in page["meta"]:
            continue

        topic = page["hero"][0]["content"] if "hero" in page else ""
        grammar = page["grammar"][0]["content"] if "grammar" in page else ""
        vocabulary = page["vocabulary"][0]["content"] if "vocabulary" in page else ""

        level = page["meta"]["level"].lower()
        unit = page["meta"]["unit"].lower()
        lesson = page["meta"]["lesson"].lower()

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


def generate_page(
    path: list,
    paths: list,
    data: dict,
    sitemap: dict,
    version: str,
    fonts: list,
    npx_path: str | None = None,
) -> list:
    """Generate a page from the data."""

    meta = data["meta"]

    parser.PATH = path
    parser.PATHS = paths
    parser.SITEMAP = sitemap
    parser.DATA = data
    parser.FONTS = fonts
    parser.VERSION = version
    parser.WEBSITE = meta["book"] if "book" in meta else ""
    parser.LEVEL = meta["level"].lower() if "level" in meta else ""
    parser.UNIT = meta["unit"].lower() if "unit" in meta else ""
    parser.LESSON = meta["lesson"].lower() if "lesson" in meta else ""
    parser.SCHEMA = meta["type"].lower() if "type" in meta else ""
    parser.ROOT = "/".join([".." for _ in path[:-1]])[:-1]  # ../../.
    parser.ROOT_ABS = ROOT_ABS

    file_name = "index.html"

    page_html: html.Html | None = None

    match data["meta"]["type"]:
        case "main":
            page_html = parser.parse_html()
        case "404":
            page_html = parser.parse_html()
            file_name = "404.html"
        case "level":
            page_html = parser.parse_html()
        case "lesson":
            page_html = parser.parse_html()
        case "test":
            page_html = parser.parse_html()
        case _:
            raise ValueError(f"{path[-1]} has unknown page type.")

    if page_html is None:
        raise ValueError(f"{path[-1]} could not be parsed into HTML.")

    page: str = str(html.Doctype()) + str(page_html)
    if npx_path is not None:
        page = format_page(page, npx_path)

    with open(os.path.join(*path[:-1], file_name), "w", encoding="utf-8") as f:
        f.write(page)

    return path[:-1] + [file_name]


def format_page(page, npx_path):
    """Format the page with Prettier."""
    try:
        process = subprocess.Popen(
            [npx_path, "prettier", "--parser", "html", "--stdin"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except subprocess.SubprocessError as e:
        raise ModuleNotFoundError(
            f"{e}\nPrettier not found. Please install Prettier through npx and try again."
        ) from e

    stdout, stderr = process.communicate(input=page.encode("utf-8"))

    if process.returncode == 0:
        return stdout.decode("utf-8")

    print(f"Prettier error: {stderr.decode('utf-8')}")
    return page  # Return original if formatting fails


if __name__ == "__main__":
    asyncio.run(main())
