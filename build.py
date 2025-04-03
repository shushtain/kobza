"""Generate HTML from data files."""

import os
import shutil
import asyncio
import json
import re
from functools import partial

import colson

from modules import cli, sitemap, generator, utils

SEP = os.path.sep
URL = "https://shushtain.github.io/kobza"
PATHS = {
    "public": ["."],
    "fonts": ["res", "fonts"],
    "styles": ["res", "styles"],
    "scripts": ["res", "scripts"],
    "icons": ["res", "icons"],
    "images": ["res", "images"],
}
PATTERNS = {
    "data": r"\.colson$",
    "fonts": r"\.woff2$",
}
IGNORE = ["_", "."]
SEMAPHORE_LIMIT = 8


async def main() -> None:
    """Does everything. Hurts nobody?"""

    # get cli arguments
    args = cli.args()

    # update version
    version = utils.update_version(
        patch=args["patch"],
        minor=args["minor"],
        major=args["major"],
    )

    print(f"BUILDING {version}")
    if True in args.values():
        print(f"Modes: {" ".join([k for k, v in args.items() if v])}")

    # check for npx, if needed
    npx_path: str | None = None
    if args["format"]:
        npx_path = shutil.which("npx")
        if npx_path is None:
            raise FileNotFoundError("npx not found. Cannot format HTML without it.")

    # get fonts
    fonts: list = utils.crawl(
        root=os.path.join(*PATHS["public"], *PATHS["fonts"]),
        pattern=PATTERNS["fonts"],
        ignore=IGNORE,
    )

    # get data files
    paths: list = utils.crawl(
        root=os.path.join(*PATHS["public"]),
        pattern=PATTERNS["data"],
        ignore=IGNORE,
    )

    # load data
    pages: dict = {}
    for i, path in enumerate(paths):
        with open(os.path.join(*path), encoding="utf-8") as f:
            file = f.read()
        pages[os.path.join(*path)] = colson.loads(file)

    # parse into JSON, if needed
    if args["json"]:
        for i, path in enumerate(paths):
            new_file_name = re.sub(PATTERNS["data"], ".json", path[-1])
            new_path = os.path.join(*path[:-1], new_file_name)
            with open(new_path, "w", encoding="utf-8") as f:
                f.write(
                    json.dumps(
                        pages[os.path.join(*path)],
                        ensure_ascii=args["ascii"],
                        indent=2,
                    )
                )

    # map lessons
    site_map: dict = sitemap.parse(pages)

    # generate pages
    semaphore = asyncio.Semaphore(SEMAPHORE_LIMIT)
    progress = cli.Progress(total=len(paths))
    progress.print()

    async def generate_with_semaphore(
        path, data, site_map, lang, version, fonts, url, paths, npx_path, index
    ):
        async with semaphore:
            new_path = await asyncio.to_thread(
                partial(
                    generator.generate,
                    path=path,
                    lang=lang,
                    data=data,
                    sitemap=site_map,
                    version=version,
                    fonts=fonts,
                    url=url,
                    paths=paths,
                    npx_path=npx_path,
                )
            )
            progress.update(index)
            progress.print()
            return new_path

    tasks = [
        generate_with_semaphore(
            path=path,
            lang="en",
            data=pages[os.path.join(*path)],
            site_map=site_map,
            version=version,
            fonts=fonts,
            url=URL,
            paths=PATHS,
            npx_path=npx_path,
            index=i,
        )
        for i, path in enumerate(paths)
    ]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
    print("\nALL DONE")
