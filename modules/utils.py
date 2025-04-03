"""Utilities for the project."""

import os
import re
from typing import Any


def crawl(root: str, pattern: str, ignore: list | None = None) -> list[list]:
    """
    Get paths to the files with names that match pattern.

    :param root: root folder
    :type root: str
    :param pattern: regex pattern
    :type pattern: str
    :param ignore: list of prefixes to ignore
    :type ignore: list
    :return: flat list of lists with breadcrumbs
    :rtype: list
    """
    paths = []

    def loop(folder):
        for f in os.listdir(folder):
            if ignore and f[0] in ignore:
                continue
            path = os.path.join(folder, f)
            if os.path.isfile(path) and re.search(pattern, f):
                paths.append(path.split(os.path.sep))
            elif os.path.isdir(path):
                loop(path)

    loop(root)

    return paths


def sort_recursively(data) -> Any:
    """Sort a dictionary or list recursively."""
    if isinstance(data, dict):
        return {k: sort_recursively(v) for k, v in sorted(data.items())}
    elif isinstance(data, list):
        return [sort_recursively(item) for item in sorted(data, key=str)]
    else:
        return data


def update_version(
    patch: bool = False,
    minor: bool = False,
    major: bool = False,
    cache: str = "VERSION.txt",
) -> str:
    """Update the version number."""

    with open(cache, encoding="utf-8") as f:
        version: str = f.read().strip()

    if patch or minor or major:
        new_version: list = version.split(".")
        if patch:
            new_version[2] = str(int(new_version[2]) + 1)
        if minor:
            new_version[1] = str(int(new_version[1]) + 1)
            new_version[2] = "0"
        if major:
            new_version[0] = str(int(new_version[0]) + 1)
            new_version[1] = "0"
            new_version[2] = "0"
        version = ".".join(new_version)
        with open(cache, "w", encoding="utf-8") as f:
            f.write(version)

    return version
