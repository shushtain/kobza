"""Main"""

import pyghtml as html
from . import blocks
from ..context import ctx


def parse() -> html.Main:
    """Main from the Body"""

    main = html.Main(id="main")

    for key, value in ctx.data.items():

        if key == "meta":
            continue

        section = html.Section(id=key)
        section += blocks.parse(value, section)
        main += section

    return main
