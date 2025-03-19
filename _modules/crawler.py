import os
import re


def crawl(root: str, pattern: str, ignore: list = [".", "_"]) -> list[list]:
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
            if f[0] in ignore:
                continue
            path = os.path.join(folder, f)
            if os.path.isfile(path) and re.search(pattern, f):
                paths.append(path.split(os.path.sep))
            elif os.path.isdir(path):
                loop(path)

    loop(root)

    return paths
