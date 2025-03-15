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


def parse_page():
    page = html.Html(lang="en")

    page += parse_head()
    page += parse_body()

    return page


def parse_head() -> html.Head:
    head = html.Head()

    for font in FONTS:
        head += html.Link(
            rel="preload",
            href=font,
            as_="font",
            type="font/woff2",
            crossorigin=True,
        )

    head += html.Link(
        rel="preload",
        href=f"/fonts.css?ver={VERSION}",
        as_="style",
    )
    head += html.Link(
        rel="stylesheet",
        href=f"/fonts.css?ver={VERSION}",
    )
    head += html.Link(
        rel="stylesheet",
        href=f"/style.css?ver={VERSION}",
    )

    head += html.Script(
        src="/script.js",
        defer=True,
    )

    head += html.Link(
        rel="icon",
        sizes="192x192",
        href="/android-icon-192x192.png",
    )
    head += html.Link(
        rel="apple-touch-icon",
        sizes="180x180",
        href="/apple-icon-180x180.png",
    )
    head += html.Link(
        rel="icon",
        sizes="96x96",
        href="/favicon-96x96.png",
    )

    head += html.Meta(
        name="viewport",
        content="width=device-width, initial-scale=1.0",
    )
    head += html.Meta(charset="utf-8")

    head += parse_title()
    head += parse_description()

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
            content.append(". ".join(SITEMAP[LEVEL][UNIT][LESSON].values()))

    description.content = sep.join(content)

    return description


def parse_body() -> html.Body:
    body = html.Body()

    body += parse_header()
    body += parse_main()
    body += parse_footer()

    return body


def parse_header() -> html.Header:
    header = html.Header(class_=LEVEL)

    nav = html.Nav(aria_attrs={"aria-label": "Main"})
    nav += html.A(
        href="#main",
        class_="button skip",
        inner_html=html.Span() + "Skip to content",
    )

    menu = html.Menu()
    menu += html.Li() + html.A(
        href="/",
        class_="button logo",
        title="Home",
        inner_html=html.Span() + "Kobza",
    )

    if SCHEMA == "lesson":
        menu += html.Li() + html.A(
            href=f"/{LEVEL}/",
            class_=f"button {LEVEL}",
            inner_html=html.Span() + LEVEL.upper(),
        )

    nav += menu
    header += nav

    return header


def parse_main() -> html.Main:
    main = html.Main(id="main", class_=LEVEL)

    for key, value in DATA.items():

        if key == "meta":
            continue

        section = html.Section(id=key)
        section += parse_block(value, section)
        main += section

    return main


def parse_footer() -> html.Footer:
    footer = html.Footer()
    nav = html.Nav(aria_attrs={"aria-label": "Bottom"})
    menu_back = ""
    menu_lessons = ""

    if SCHEMA == "lesson":
        menu_lessons = html.Menu(class_="menu-lessons")

        lessons: list = []
        for unit in SITEMAP[LEVEL]:
            for lesson in SITEMAP[LEVEL][unit]:
                lessons.append([unit, lesson])

        lesson_prev_index = lessons.index([UNIT, LESSON]) - 1
        lesson_next_index = lessons.index([UNIT, LESSON]) + 1

        if lesson_prev_index >= 0:
            lesson_prev = lessons[lesson_prev_index]
            lesson_prev_link = f"/{LEVEL}/{"".join(lesson_prev)}/"
            lesson_prev_text = ". ".join(
                [
                    f"Lesson {"".join(lesson_prev).upper()}",
                    SITEMAP[LEVEL][lesson_prev[0]][lesson_prev[1]]["grammar"],
                    SITEMAP[LEVEL][lesson_prev[0]][lesson_prev[1]]["vocabulary"],
                ]
            )
            menu_lessons += html.Li() + html.A(
                href=lesson_prev_link,
                class_="button lesson-prev",
                inner_html=html.Span() + lesson_prev_text,
            )

        if lesson_next_index < len(lessons):
            lesson_next = lessons[lesson_next_index]
            lesson_next_link = f"/{LEVEL}/{"".join(lesson_next)}/"
            lesson_next_text = ". ".join(
                [
                    f"Lesson {"".join(lesson_next).upper()}",
                    SITEMAP[LEVEL][lesson_next[0]][lesson_next[1]]["grammar"],
                    SITEMAP[LEVEL][lesson_next[0]][lesson_next[1]]["vocabulary"],
                ]
            )
            menu_lessons += html.Li() + html.A(
                href=lesson_next_link,
                class_="button lesson-next",
                inner_html=html.Span() + lesson_next_text,
            )

    if len(PATH) > 2:
        path_parent = "/"
        for breadcrumb in PATH[1:-2]:
            path_parent += breadcrumb
            path_parent += "/"
        menu_back = html.Menu(class_="menu-back")
        menu_back += html.Li() + html.A(
            href=path_parent,
            class_="button back",
            inner_html=html.Span() + "Back",
        )

    menu_contacts = html.Menu(class_="menu-contacts")
    menu_contacts += html.Li() + html.A(
        href="mailto:shushtain@gmail.com",
        class_="button mail",
        target="_blank",
        inner_html=html.Span() + "shushtain@gmail.com",
    )

    nav += menu_lessons
    nav += menu_back
    nav += menu_contacts
    footer += nav

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
    section = html.Section(class_=class_, id=id_)

    match SCHEMA:

        case _:
            section += parse_block(content, section)

    return section


def parse_div(content, scope, class_=None, id_=None) -> html.Div:
    div = html.Div(class_=class_, id=id_)

    match SCHEMA:

        case _:
            div += parse_block(content, div)

    return div


def parse_h1(content, scope, class_=None, id_=None) -> html.H1:
    h1 = html.H1(class_=class_, id=id_)

    match SCHEMA:

        case "lesson":
            h1 += html.Span() + f"Lesson {UNIT}{LESSON.upper()}:"
            h1 += html.Br()
            h1 += f"{content}"

        case _:
            h1 += parse_block(content, h1)

    return h1


def parse_h2(content, scope, class_=None, id_=None) -> html.H2:
    h2 = html.H2(class_=class_, id=id_)

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
    h3 = html.H3(class_=class_, id=id_)

    match SCHEMA:

        case _:
            h3 += parse_block(content, h3)

    return h3


def parse_h4(content, scope, class_=None, id_=None) -> html.H4:
    h4 = html.H4(class_=class_, id=id_)

    match SCHEMA:

        case _:
            h4 += parse_block(content, h4)

    return h4


def parse_h5(content, scope, class_=None, id_=None) -> html.H5:
    h5 = html.H5(class_=class_, id=id_)

    match SCHEMA:

        case _:
            h5 += parse_block(content, h5)

    return h5


def parse_h6(content, scope, class_=None, id_=None) -> html.H6:
    h6 = html.H6(class_=class_, id=id_)

    match SCHEMA:

        case _:
            h6 += parse_block(content, h6)

    return h6


def parse_p(content, scope, class_=None, id_=None) -> html.P:
    p = html.P(class_=class_, id=id_)

    match SCHEMA:

        case _:
            p += parse_block(content, p)

    return p


def parse_ul(content, scope, class_=None, id_=None) -> html.Ul:
    ul = html.Ul(class_=class_, id=id_)

    for item in content:

        match SCHEMA:

            case _:
                li = html.Li()
                ul += li + parse_block(item, li)

    return ul


def parse_ol(content, scope, class_=None, id_=None) -> html.Ol:
    ol = html.Ol(class_=class_, id=id_)

    for item in content:

        match SCHEMA:

            case _:
                li = html.Li()
                ol += li + parse_block(item, li)

    return ol


def parse_blockquote(content, scope, class_=None, id_=None) -> html.Blockquote:
    blockquote = html.Blockquote(class_=class_, id=id_)

    match SCHEMA:

        case _:
            blockquote += parse_block(content, blockquote)

    return blockquote


def parse_button(content, scope, class_=None, id_=None) -> html.A:
    button = html.A(class_=["button", class_], id=id_)

    match SCHEMA:

        case _:
            inner, href_title = content[1:-1].split("](")
            href_title_list = href_title.split('"')

            button.href = href_title_list[0].strip()
            button += html.Span() + inner

            if len(href_title_list) > 1:
                button.title = href_title_list[1].strip()

    return button


def parse_figure(content, scope, class_=None, id_=None) -> html.Figure:
    figure = html.Figure(class_=class_, id=id_)

    src = content["img"]
    alt = content["alt"]
    figcaption = parse_inline(content["figcaption"])

    match SCHEMA:

        case _:
            figure += html.Img(src=src, alt=alt)
            figure += html.Figcaption() + figcaption

    return figure


def parse_flashcards(content, scope, class_=None, id_=None) -> html.Div:
    flashcards = html.Div(class_=["flashcards", class_], id=id_)

    for item in content:

        match SCHEMA:

            case _:
                card = html.Div(class_="flashcard")
                card += html.Img(src=item["img"])
                card += (
                    html.Div(class_="flashcard-text")
                    + html.P(class_="flashcard-q", inner_html=parse_inline(item["q"]))
                    + html.P(class_="flashcard-a", inner_html=parse_inline(item["a"]))
                )
                flashcards += card

    return flashcards


def parse_toc(content, scope, class_=None, id_=None) -> html.Div:
    toc = html.Div(class_=["toc", class_])
    toc.id = f"toc-{SCHEMA}" if id_ is None else id_

    match SCHEMA:

        case "main":
            toc.class_.append("cards")

            for level in SITEMAP:
                toc += html.Div(class_=f"card {level}") + html.A(
                    href=f"/{level}/", inner_html=level.upper()
                )

        case "level":

            for unit, lessons in SITEMAP[LEVEL].items():
                ul = html.Ul()
                for lesson, topics in lessons.items():
                    ul += html.Li() + html.A(
                        href=f"/{LEVEL}/{unit + lesson}/",
                        inner_html=". ".join(
                            [f"Lesson {unit + lesson.upper()}", *topics.values()]
                        ),
                    )
                toc += html.Section() + html.H3(inner_html=f"Unit {unit}") + ul

    return toc


def parse_fillgaps(content, scope, class_=None, id_=None) -> html.Ol:
    fillgaps = html.Ol(class_=["fillgaps", class_], id=id_)

    match SCHEMA:

        case _:
            for line in content:
                task = html.Li()
                elems = line.split("|")
                for i, elem in enumerate(elems):
                    if i % 2 == 0:
                        task += elem
                    else:
                        span = html.Span() + elem.strip()
                        task += html.Label() + html.Input(type="checkbox") + span
                fillgaps += task

    return fillgaps


def parse_orderwords(content, scope, class_=None, id_=None) -> html.Ol:
    orderwords = html.Ol(class_=["orderwords", class_], id=id_)

    match SCHEMA:

        case _:
            for line in content:
                task = html.Li(class_="orderwords-line")
                elems = line.split("|")
                for elem in elems:
                    task += html.Span(class_="draggable") + elem.strip()
                orderwords += task

    return orderwords


def parse_matchpictures(content, scope, class_=None, id_=None) -> html.Div:
    matchpictures = html.Div(class_=["matchpictures", class_], id=id_)

    match SCHEMA:

        case _:
            phrases = html.Ol(class_="mp-phrases")
            pictures = html.Ol(class_="mp-pictures")

            for block in content:
                code = block["img"].split(".")[0]
                phrases += html.Li(class_=[code, "mp-phrase", "draggable"]) + html.Span(
                    inner_html=block["text"]
                )
                pictures += html.Li(class_=[code, "mp-picture"]) + html.Img(
                    src=block["img"]
                )

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
    line = re.sub(
        r'\[(?P<text>.*?)\]\((?P<href>.*?)\s?(?:"(?P<title>.*?)")?\)',
        fr'{html.A(href=r"\g<href>", target="_blank", title=r"\g<title>") + r"\g<text>"}',
        line,
    )

    return line


def parse_code(code) -> str:
    """Parse content of the blocks into HTML"""

    code = code.strip()

    code = re.sub(r"&", "&amp;", code)
    code = re.sub(r"<", "&lt;", code)
    code = re.sub(r">", "&gt;", code)
    code = re.sub(r"  ", rf"{html.Br()}", code)

    return code
