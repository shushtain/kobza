"""Utility functions for the project."""

from typing import Any
import os


def sort_recursively(data) -> Any:
    """Sort a dictionary or list recursively."""
    if isinstance(data, dict):
        return {k: sort_recursively(v) for k, v in sorted(data.items())}
    elif isinstance(data, list):
        return [sort_recursively(item) for item in sorted(data, key=str)]
    else:
        return data


def update_version(
    new_patch: bool = False,
    new_minor: bool = False,
    new_major: bool = False,
    root: str = ".",
) -> str:
    """Update the version number."""

    try:
        with open(os.path.join(root, "VERSION.txt"), encoding="utf-8") as f:
            version: str = f.read().strip()
    except FileNotFoundError as e:
        raise FileNotFoundError(
            f"{e}\nVERSION.txt is missing from the root folder."
        ) from e

    if new_patch or new_minor or new_major:
        try:
            new_version: list = version.split(".")
            if new_patch:
                new_version[2] = str(int(new_version[2]) + 1)
            if new_minor:
                new_version[1] = str(int(new_version[1]) + 1)
                new_version[2] = "0"
            if new_major:
                new_version[0] = str(int(new_version[0]) + 1)
                new_version[1] = "0"
                new_version[2] = "0"
            version = ".".join(new_version)
            with open("VERSION.txt", "w", encoding="utf-8") as f:
                f.write(version)
        except ValueError as e:
            raise ValueError(
                f"{e}\nVERSION.txt does not follow Semantic Versioning (major.minor.patch)."
            ) from e

    return version
