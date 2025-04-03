"""Body"""

import pyghtml as html
from . import header, main, footer


def parse() -> html.Body:
    """Parse body"""

    body = html.Body()

    body += header.parse()
    body += main.parse()
    body += footer.parse()

    return body
