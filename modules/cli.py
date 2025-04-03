"""Command line interface."""

import argparse
import sys


def args() -> dict:
    """Parse command line arguments."""

    parser = argparse.ArgumentParser(description="Compile ColSON into HTML.")

    parser.add_argument(
        "-f",
        "--format",
        action="store_true",
        help="Format compiled HTML with Prettier.",
    )

    parser.add_argument(
        "-j",
        "--json",
        action="store_true",
        help="Parse into JSON files as well.",
    )

    parser.add_argument(
        "-a",
        "--ascii",
        action="store_true",
        help="Ensure ascii for JSON files if `-j` is provided.",
    )

    parser.add_argument(
        "-p",
        "--patch",
        action="store_true",
        help="Increment the patch version.",
    )

    parser.add_argument(
        "-m",
        "--minor",
        action="store_true",
        help="Increment the minor version.",
    )

    parser.add_argument(
        "-M",
        "--major",
        action="store_true",
        help="Increment the major version.",
    )

    parsed = parser.parse_args()
    return {
        "format": parsed.format,
        "json": parsed.json,
        "ascii": parsed.ascii,
        "patch": parsed.patch,
        "minor": parsed.minor,
        "major": parsed.major,
    }


class Progress:
    """Print a progress bar."""

    def __init__(self, total: int, empty: str = "—", filled: str = "■"):
        self.total = total
        self.empty = empty
        self.filled = filled
        self.array = list(self.empty * total)
        self.count = 0

    def __str__(self):
        digits = len(str(self.total))
        return "[" + "".join(self.array) + "]" + f" {self.count:{digits}}/{self.total}"

    def update(self, current: int):
        """Update the progress bar."""
        self.array[current] = self.filled
        self.count += 1

    def print(self):
        """Print the progress bar."""
        sys.stdout.write(f"\r{self}")
        sys.stdout.flush()
