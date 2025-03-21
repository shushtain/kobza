import re

import pyghtml as html

PATH: list = []
PATHS: list = []
SITEMAP: dict = {}
DATA: dict = {}
FONTS: list = []
VERSION: str = ""
WEBSITE: str = ""
LEVEL: str = ""
UNIT: str = ""
LESSON: str = ""
SCHEMA: str = ""
ROOT: str = ""
ROOT_ABS: str = ""


def parse_page():
    page = html.Html(lang="en")

    page += parse_head()
    page += parse_body()

    return page


def parse_head() -> html.Head:
    head = html.Head()

    # Encoding and viewport
    head += html.CommentHtml("Encoding and viewport")
    head += html.Meta(charset="utf-8")
    head += html.Meta(
        name="viewport",
        content="width=device-width, initial-scale=1.0",
    )

    # Primary meta tags
    head += html.CommentHtml("Primary meta tags")
    head += parse_title()
    head += parse_description()
    head += html.Meta(name="author", content="Artem Shush")

    # Open Graph
    head += html.CommentHtml("Open Graph")
    head += html.Meta(property="og:type", content="website")
    head += html.Meta(
        property="og:url",
        content=link(ROOT_ABS, *PATH[1:-1]),
    )
    head += html.Meta(property="og:title", content=parse_title().inner_html)
    head += html.Meta(property="og:description", content=parse_description().content)
    head += html.Meta(
        property="og:image",
        content=link(ROOT_ABS, "og-image.png"),
    )

    # Use the latest IE engine
    head += html.CommentHtml("Use the latest IE engine")
    head += html.Meta(http_equiv="X-UA-Compatible", content="IE=edge")

    # Preload fonts
    head += html.CommentHtml("Preload fonts")
    for font in FONTS:
        head += html.Link(
            rel="preload",
            href=link(ROOT, *font[1:]),
            as_="font",
            type="font/woff2",
            crossorigin=True,
        )

    # Preload font styles
    head += html.CommentHtml("Preload font styles")
    head += html.Link(
        rel="preload",
        href=link(ROOT, "fonts.css?ver=" + VERSION),
        as_="style",
    )

    # Load styles
    head += html.CommentHtml("Load styles")
    head += html.Link(
        rel="stylesheet",
        href=link(ROOT, "fonts.css?ver=" + VERSION),
    )
    head += html.Link(
        rel="stylesheet",
        href=link(ROOT, "style.css?ver=" + VERSION),
    )

    # Load scripts
    head += html.CommentHtml("Load scripts")
    head += html.Script(
        src=link(ROOT, "script.js"),
        defer=True,
    )

    # Add favicons
    head += html.CommentHtml("Add favicons")
    head += html.Link(
        rel="icon",
        sizes="192x192",
        href=link(ROOT, "android-icon-192x192.png"),
    )
    head += html.Link(
        rel="apple-touch-icon",
        sizes="180x180",
        href=link(ROOT, "apple-icon-180x180.png"),
    )
    head += html.Link(
        rel="icon",
        sizes="96x96",
        href=link(ROOT, "favicon-96x96.png"),
    )

    # Manifest
    head += html.CommentHtml("Manifest")
    head += html.Link(
        rel="manifest",
        href=link(ROOT, "manifest.json"),
    )

    return head


def parse_title() -> html.Title:
    title = html.Title()

    content = []
    sep = " • "

    match SCHEMA:

        case "main":
            content.append(WEBSITE)

        case "404":
            content.append("404 NOT FOUND")
            content.append(WEBSITE)

        case "level":
            content.append(LEVEL.upper())
            content.append(WEBSITE)

        case "lesson":
            content.append(UNIT + LESSON.upper())
            content.append(LEVEL.upper())
            content.append(WEBSITE)

    title += sep.join(content)

    return title


def parse_description() -> html.Meta:
    description = html.Meta(name="description")

    content = []
    sep = " "

    match SCHEMA:

        case "main":
            content.append(f"{WEBSITE}, open source English textbook.")

        case "404":
            content.append("ERROR 404.")
            content.append("The page is not found.")

        case "level":
            content.append(f"{WEBSITE} {LEVEL.upper()}.")
            content.append(f"{len(SITEMAP[LEVEL])} units.")

        case "lesson":
            # content.append(f"{WEBSITE} {LEVEL.upper()}.")
            # content.append(f"Unit {UNIT}. Lesson {UNIT + LESSON.upper()}.")
            grammar = SITEMAP[LEVEL][UNIT][LESSON]["grammar"]
            vocabulary = SITEMAP[LEVEL][UNIT][LESSON]["vocabulary"]
            content.append(". ".join([grammar, vocabulary]))

    description.content = sep.join(content)

    return description


def parse_body() -> html.Body:
    body = html.Body()

    body += parse_header()
    body += parse_main()
    body += parse_footer()

    return body


def parse_header() -> html.Header:
    header = html.Header()

    nav = html.Nav(aria_attrs={"aria-label": "Primary"})
    nav += html.A(
        href="#main",
        class_=["button", "tile", "skip"],
        inner_html=html.Span() + "Skip to content",
    )

    nav += html.A(
        href=link(ROOT),
        class_=["button", "tile", "accent"],
        aria_attrs={"aria-label": "Kobza Home"},
        inner_html=html.Span() + "Kobza",
    )

    if SCHEMA == "lesson":
        nav += html.A(
            href=link(ROOT, LEVEL),
            class_=["button", "tile", "tone"],
            inner_html=html.Span() + LEVEL.upper(),
        )

    header += nav

    return header


def parse_main() -> html.Main:
    main = html.Main(id="main")

    for key, value in DATA.items():

        if key == "meta":
            continue

        section = html.Section(id=key)
        section += parse_block(value, section)
        main += section

    return main


def parse_footer() -> html.Footer:
    footer = html.Footer()

    # Lessons navigation
    if SCHEMA == "lesson":
        nav_lessons = html.Nav(class_=["lessons"], aria_attrs={"aria-label": "Lessons"})

        lessons: list = []
        for unit in SITEMAP[LEVEL]:
            for lesson in SITEMAP[LEVEL][unit]:
                lessons.append([unit, lesson])

        lesson_prev_index = lessons.index([UNIT, LESSON]) - 1
        lesson_next_index = lessons.index([UNIT, LESSON]) + 1

        if lesson_prev_index >= 0:
            lesson_prev = lessons[lesson_prev_index]
            lesson_prev_link = link(ROOT, LEVEL, "".join(lesson_prev))
            lesson_prev_text = ". ".join(
                [
                    f"Lesson {"".join(lesson_prev).upper()}",
                    SITEMAP[LEVEL][lesson_prev[0]][lesson_prev[1]]["grammar"],
                    SITEMAP[LEVEL][lesson_prev[0]][lesson_prev[1]]["vocabulary"],
                ]
            )
            nav_lessons += html.A(
                href=lesson_prev_link,
                class_=["button", "tile", "prev"],
                aria_attrs={"aria-label": "Previous lesson"},
                inner_html=html.Span() + lesson_prev_text,
            )

        if lesson_next_index < len(lessons):
            lesson_next = lessons[lesson_next_index]
            lesson_next_link = link(ROOT, LEVEL, "".join(lesson_next))
            lesson_next_text = ". ".join(
                [
                    f"Lesson {"".join(lesson_next).upper()}",
                    SITEMAP[LEVEL][lesson_next[0]][lesson_next[1]]["grammar"],
                    SITEMAP[LEVEL][lesson_next[0]][lesson_next[1]]["vocabulary"],
                ]
            )
            nav_lessons += html.A(
                href=lesson_next_link,
                class_=["button", "tile", "next"],
                aria_attrs={"aria-label": "Next lesson"},
                inner_html=html.Span() + lesson_next_text,
            )

        footer += nav_lessons

    # Back navigation
    if len(PATH) > 2:
        path_parent = link(ROOT, *[crumb for crumb in PATH[1:-2]])

        nav_back = html.Nav(class_=["back"], aria_attrs={"aria-label": "Back"})
        nav_back += html.A(
            href=path_parent,
            class_=["button", "tile", "back"],
            inner_html=html.Span() + "Back",
        )

        footer += nav_back

    # Contacts
    footer += html.Div(class_=["author"]) + html.A(
        href="https://github.com/shushtain/kobza",
        class_=["inline", "subtle"],
        inner_html=html.Small()
        + "@Kobza",  # Changed from having 'small' in class to using Small()
    )

    return footer


def parse_block(block, scope):

    if isinstance(block, list):
        subs = []
        for sub in block:
            subs.append(parse_block(sub, scope))
        return subs

    if isinstance(block, dict):

        content = block["content"] if "content" in block else None
        class_ = block["class"] if "class" in block else None
        id_ = block["id"] if "id" in block else None

        match block["type"]:
            case "section":
                return parse_section(content, scope, class_, id_)
            case "div":
                return parse_div(content, scope, class_, id_)
            case "h1":
                return parse_h1(content, scope, class_, id_)
            case "h2":
                return parse_h2(content, scope, class_, id_)
            case "h3":
                return parse_h3(content, scope, class_, id_)
            case "h4":
                return parse_h4(content, scope, class_, id_)
            case "h5":
                return parse_h5(content, scope, class_, id_)
            case "h6":
                return parse_h6(content, scope, class_, id_)
            case "p":
                return parse_p(content, scope, class_, id_)
            case "quote":
                return parse_blockquote(content, scope, class_, id_)
            case "ul":
                return parse_ul(content, scope, class_, id_)
            case "ol":
                return parse_ol(content, scope, class_, id_)
            case "flashcards":
                return parse_flashcards(content, scope, class_, id_)
            case "button":
                return parse_button(content, scope, class_, id_)
            case "figure":
                return parse_figure(content, scope, class_, id_)
            case "toc":
                return parse_toc(content, scope, class_, id_)
            case "fillgaps":
                return parse_fillgaps(content, scope, class_, id_)
            case "orderwords":
                return parse_orderwords(content, scope, class_, id_)
            case "matchpictures":
                return parse_matchpictures(content, scope, class_, id_)
            case _:
                return html.CommentHtml() + content

    return parse_inline(block)


def parse_section(content, scope, class_=None, id_=None) -> html.Section:
    section = html.Section(class_=[class_], id=id_)
    section += parse_block(content, section)
    return section


def parse_div(content, scope, class_=None, id_=None) -> html.Div:
    div = html.Div(class_=[class_], id=id_)
    div += parse_block(content, div)
    return div


def parse_h1(content, scope, class_=None, id_=None) -> html.H1:
    h1 = html.H1(class_=[class_], id=id_)

    match SCHEMA:

        case "lesson":
            h1 += html.Span() + f"Lesson {UNIT}{LESSON.upper()}:"
            h1 += html.Br()
            h1 += f"{content}"

        case _:
            h1 += parse_block(content, h1)

    return h1


def parse_h2(content, scope, class_=None, id_=None) -> html.H2:
    h2 = html.H2(class_=[class_], id=id_)

    match SCHEMA:

        case "lesson":
            if content == "":
                if scope.id:
                    h2 += f"{scope.id.capitalize()}"
            else:
                if scope.id:
                    h2 += html.Span() + f"{scope.id.capitalize()}:"
                h2 += html.Br()
            h2 += content

        case _:
            h2 += parse_block(content, h2)

    return h2


def parse_h3(content, scope, class_=None, id_=None) -> html.H3:
    h3 = html.H3(class_=[class_], id=id_)
    h3 += parse_block(content, h3)
    return h3


def parse_h4(content, scope, class_=None, id_=None) -> html.H4:
    h4 = html.H4(class_=[class_], id=id_)
    h4 += parse_block(content, h4)
    return h4


def parse_h5(content, scope, class_=None, id_=None) -> html.H5:
    h5 = html.H5(class_=[class_], id=id_)
    h5 += parse_block(content, h5)
    return h5


def parse_h6(content, scope, class_=None, id_=None) -> html.H6:
    h6 = html.H6(class_=[class_], id=id_)
    h6 += parse_block(content, h6)
    return h6


def parse_p(content, scope, class_=None, id_=None) -> html.P:
    p = html.P(class_=[class_], id=id_)
    p += parse_block(content, p)
    return p


def parse_ul(content, scope, class_=None, id_=None) -> html.Ul:
    ul = html.Ul(class_=[class_], id=id_)

    for item in content:
        li = html.Li()
        ul += li + parse_block(item, li)

    return ul


def parse_ol(content, scope, class_=None, id_=None) -> html.Ol:
    ol = html.Ol(class_=[class_], id=id_)

    for item in content:
        li = html.Li()
        ol += li + parse_block(item, li)

    return ol


def parse_blockquote(content, scope, class_=None, id_=None) -> html.Blockquote:
    blockquote = html.Blockquote(class_=[class_, "area"], id=id_)
    blockquote += parse_block(content, blockquote)
    return blockquote


def parse_button(content, scope, class_=None, id_=None) -> html.A:
    button = html.A(class_=["button", "tile", class_], id=id_)

    match: re.Match | None = re.search(
        r'\[(?P<text>.*?)\]\((?P<href>.*?)\s?(?:"(?P<title>.*?)")?\)', content
    )
    if match is None:
        raise ValueError("Invalid button format.")
    text = match.group("text")
    href = match.group("href")
    title = match.group("title")
    target = "_blank"

    if href[0] == "~":
        href = href.rstrip("/")
        href = link(ROOT, *href.split("/")[1:])

    button.href = href
    button.title = title
    button.target = target
    button += html.Span() + text

    return button


def parse_figure(content, scope, class_=None, id_=None) -> html.Figure:
    figure = html.Figure(class_=[class_], id=id_)

    src = content["img"]
    alt = content["alt"]
    figcaption = parse_inline(content["figcaption"])

    figure += html.Img(src=src, alt=alt)
    figure += html.Figcaption(class_=["subtle"]) + figcaption

    return figure


def parse_flashcards(content, scope, class_=None, id_=None) -> html.Div:
    flashcards = html.Div(class_=["flashcards-wrapper", class_], id=id_)

    # main viewer
    viewer = html.Div(class_=["flashcards-viewer"])
    flashcards += viewer

    # viewer header
    viewer_header = html.Div(class_=["header"])
    viewer_header += html.Button(class_=["restart", "button", "tile"]) + (
        html.Span() + "Restart"
    )
    viewer_header += (
        html.Div(class_=["counter", "subtle", "small"])
        + (html.Span(class_=["current"]) + "0")
        + "/"
        + (html.Span(class_=["total"]) + len(content))
    )
    viewer += viewer_header

    # viewer window
    viewer_window = html.Div(class_=["window", "tile"], tabindex="0")
    card_inner = html.Div(class_=["inner", "area"])
    card_inner += html.Div(class_=["front"])
    card_inner += html.Div(class_=["back"])
    viewer_window += card_inner
    viewer += viewer_window

    # viewer footer
    viewer_footer = html.Div(class_=["footer"])
    viewer_footer += html.Button(class_=["prev", "button", "tile"]) + (
        html.Span() + "Prev"
    )
    viewer_footer += html.Button(class_=["flip", "button", "tile"]) + (
        html.Span() + "Flip"
    )
    viewer_footer += html.Button(class_=["next", "button", "tile"]) + (
        html.Span() + "Next"
    )
    viewer += viewer_footer

    # all cards
    all_cards = html.Details(class_=["flashcards-all"])
    all_cards += html.Summary(class_=["button", "tile"]) + "All cards"
    cards = html.Div(class_=["flashcards"])

    for item in content:
        card = html.Div(class_=["flashcard", "area"])
        card += html.Img(src=item["img"], alt="")
        card += (
            html.Dl()
            + html.Dt(inner_html=parse_inline(item["q"]))
            + html.Dd(inner_html=parse_inline(item["a"]))
        )
        cards += card

    all_cards += cards
    flashcards += all_cards

    return flashcards


def parse_toc(content, scope, class_=None, id_=None) -> html.Div:
    toc = html.Div(class_=["toc", class_])
    toc.id = f"toc-{SCHEMA}" if id_ is None else id_

    match SCHEMA:

        case "main":
            if isinstance(toc.class_, list):
                toc.class_.append("cards")
            else:
                toc.class_ = "cards"

            for level in SITEMAP:
                toc += html.Div(class_=["card", "tile", "accent", level]) + html.A(
                    href=link(ROOT, level), inner_html=level.upper()
                )

        case "level":
            for unit, lessons in SITEMAP[LEVEL].items():
                ul = html.Ul()
                for lesson, topics in lessons.items():
                    ul += html.Li() + html.A(
                        href=link(ROOT, LEVEL, unit + lesson),
                        inner_html=". ".join(
                            [
                                f"Lesson {unit + lesson.upper()}",
                                topics["grammar"],
                                topics["vocabulary"],
                            ]
                        ),
                    )
                toc += html.Section() + html.H3(inner_html=f"Unit {unit}") + ul

    return toc


def parse_fillgaps(content, scope, class_=None, id_=None) -> html.Div:
    fillgaps = html.Div(class_=["ex-fg", class_], id=id_)
    tasks = html.Ol()

    for line in content:
        task = html.Li(class_=["task", "ex-fg-task"])
        elems = line.split("|")
        for i, elem in enumerate(elems):
            if i % 2 == 0:
                task += elem
            else:
                task += html.Span(class_=["tile"], tabindex="0") + elem.strip()
        tasks += task

    fillgaps += tasks
    return fillgaps


def parse_orderwords(content, scope, class_=None, id_=None) -> html.Div:
    orderwords = html.Div(class_=["ex-ow", class_], id=id_)
    tasks = html.Ol()

    for line in content:
        task = html.Li(class_=["task", "ex-ow-task"])
        elems = line.split("|")
        for elem in elems:
            task += html.Span(class_=["tile", "draggable"], tabindex="0") + elem.strip()
        tasks += task

    orderwords += tasks
    return orderwords


def parse_matchpictures(content, scope, class_=None, id_=None) -> html.Div:
    matchpictures = html.Div(class_=["ex-mp", class_], id=id_)

    phrases = html.Ol(class_=["task", "ex-mp-task"])
    pictures = html.Ol(class_=["ex-mp-ref"])

    for block in content:
        phrases += html.Li(class_=["draggable"], tabindex="0") + html.Span(
            class_=["tile"], inner_html=block["text"]
        )
        pictures += html.Li(class_=["ex-mp-ref-item"]) + html.Img(src=block["img"])

    matchpictures += phrases
    matchpictures += pictures

    return matchpictures


def parse_inline(line) -> str:
    """Parse content of the blocks into HTML"""

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
        target = "_blank"

        if href[0] == "~":
            href = href.rstrip("/")
            href = link(ROOT, *href.split("/")[1:])
            # target = ""

        sub = f"{html.A(class_="inline", href=href, target=target, title=title) + text}"
        line = pattern_link.sub(sub, line)

    return line


def parse_code(code) -> str:
    """Parse content of the blocks into HTML"""

    code = code.strip()

    code = re.sub(r"&", "&amp;", code)
    code = re.sub(r"<", "&lt;", code)
    code = re.sub(r">", "&gt;", code)
    code = re.sub(r"  ", rf"{html.Br()}", code)

    return code


def link(*parts, as_is=False):
    """Join parts of a path and return it."""

    # link raw if specified
    if as_is:
        return "/".join(parts)

    # check if directory
    is_directory = False

    # if no file extension -> directory
    if "." not in parts[-1]:
        is_directory = True

    # if ends on the root '..' -> directory
    if parts[-1][-2:] == "..":
        is_directory = True

    return "/".join(parts) + ("/" if is_directory else "")
