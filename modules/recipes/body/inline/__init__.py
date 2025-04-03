import re
import pyghtml as html

from ...context import ctx
from ...utils import link


def parse(line) -> str:
    """Parse Markdown content of the blocks into HTML"""

    line = line.strip()

    line = re.sub(r"\\\*", r"\*", line)
    line = re.sub(r"\\\|", r"\|", line)
    line = re.sub(r"\\\[", r"\[", line)
    line = re.sub(r"\\\]", r"\]", line)
    line = re.sub(r"\\\(", r"\(", line)
    line = re.sub(r"\\\)", r"\)", line)
    line = re.sub(r"\\\+", r"\+", line)
    line = re.sub(r"\\#", r"#", line)
    line = re.sub(r"\\!", r"!", line)
    line = re.sub(r"\\-", r"-", line)
    line = re.sub(r"\\`", r"`", line)
    line = re.sub(r"\\>", r">", line)

    # line = re.sub(r"&", "&amp;", line)
    line = re.sub(r"<", "&lt;", line)
    line = re.sub(r">", "&gt;", line)
    line = re.sub(r"  ", rf"{html.Br()}", line)

    # strong + em
    line = re.sub(
        r"\*\*\*(?P<text>(.*?))\*\*\*", r"<strong><em>\g<text></em></strong>", line
    )

    # strong
    line = re.sub(r"\*\*(?P<text>(.*?))\*\*", fr"{html.Strong()+ r"\g<text>"}", line)

    # em
    line = re.sub(r"\*(?P<text>([^`]*?))\*", fr"{html.Em()+ r"\g<text>"}", line)

    # s
    line = re.sub(r"~~(?P<text>([^`]*?))~~", fr"{html.S()+ r"\g<text>"}", line)

    # code
    line = re.sub(r"`(?P<text>(.*?))`", fr"{html.Mark()+ r"\g<text>"}", line)

    # link
    pattern_link = re.compile(
        r'\[(?P<text>.*?)\]\((?P<href>.*?)\s?(?:"(?P<title>.*?)")?\)'
    )
    for match in pattern_link.finditer(line):
        text = match.group("text")
        href = match.group("href")
        title = match.group("title")
        target = None

        if href.startswith("/"):
            href = link(ctx.root, href[1:])
        if href.startswith("http"):
            target = "_blank"

        sub = f"{html.A(href=href, target=target, title=title) + text}"
        line = pattern_link.sub(sub, line, count=1)

    return line


# def parse_code(code) -> str:
#     """Parse Markdown content of the code blocks into HTML"""

#     code = code.strip()

#     code = re.sub(r"&", "&amp;", code)
#     code = re.sub(r"<", "&lt;", code)
#     code = re.sub(r">", "&gt;", code)
#     code = re.sub(r"  ", rf"{html.Br()}", code)

#     return code
