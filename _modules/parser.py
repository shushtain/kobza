"""Parses Python objects into HTML, according to the recipes."""

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


def parse_html() -> html.Html:
    """HTML with Head and Body"""
    page = html.Html(lang="en")

    page += parse_head()
    page += parse_body()

    return page


def parse_head() -> html.Head:
    """Head"""
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

    # Specify color scheme
    head += html.CommentHtml("Specify color scheme")
    head += html.Meta(name="color-scheme", content="light dark")

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
        # defer=True,
    )
    if SCHEMA == "lesson":
        head += html.Script(
            src=link(ROOT, "script-lesson.js"),
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
    """Title from the Head"""
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
            content.append(f"Level {LEVEL.upper()}")
            content.append(WEBSITE)

        case "lesson":
            content.append(f"Lesson {UNIT}{LESSON.upper()}")
            content.append(f"Level {LEVEL.upper()}")
            content.append(WEBSITE)

    title += sep.join(content)

    return title


def parse_description() -> html.Meta:
    """Description from the Head"""
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
            topic = SITEMAP[LEVEL][UNIT][LESSON]["topic"]
            grammar = SITEMAP[LEVEL][UNIT][LESSON]["grammar"]
            vocabulary = SITEMAP[LEVEL][UNIT][LESSON]["vocabulary"]
            content.append(". ".join([topic, grammar, vocabulary]))

    description.content = sep.join(content)

    return description


def parse_body() -> html.Body:
    """Body"""
    body = html.Body()

    body += parse_header()
    body += parse_main()
    body += parse_footer()

    return body


def parse_header() -> html.Header:
    """Header from the Body"""
    header = html.Header()

    nav = html.Nav(aria_attrs={"aria-label": "Primary"})
    nav += html.A(
        href="#main",
        class_=["button", "skip"],
        inner_html=html.Span() + "Skip to content",
    )

    nav += html.A(
        href=link(ROOT),
        class_=["button", "accent"],
        aria_attrs={"aria-label": "Kobza Home"},
        inner_html=html.Span() + "Kobza",
    )

    if SCHEMA == "lesson":
        nav += html.A(
            href=link(ROOT, LEVEL),
            class_=["button"],
            inner_html=html.Span() + LEVEL.upper(),
        )

    # color mode toggle
    toggle_theme = html.Button(
        type="button",
        id="toggle-theme",
        aria_attrs={"aria-label": "Toggle theme"},
    )
    toggle_theme += html.Svg(class_=["icon"], id="toggle-light") + html.Use(
        href=icon("light-mode")
    )
    toggle_theme += html.Svg(class_=["icon"], id="toggle-dark") + html.Use(
        href=icon("dark-mode")
    )

    header += nav
    header += toggle_theme

    return header


def parse_main() -> html.Main:
    """Main from the Body"""
    main = html.Main(id="main")

    for key, value in DATA.items():

        if key == "meta":
            continue

        section = html.Section(id=key)
        section += parse_block(value, section)
        main += section

    return main


def parse_footer() -> html.Footer:
    """Footer from the Body"""
    footer = html.Footer()

    nav = html.Nav(aria_attrs={"aria-label": "Secondary"})

    nav_prev = html.A(class_=["button", "disabled"])
    nav_next = html.A(class_=["button", "disabled"])

    # Secondary navigation
    if SCHEMA == "lesson":

        lessons: list = []
        for unit in SITEMAP[LEVEL]:
            for lesson in SITEMAP[LEVEL][unit]:
                lessons.append([unit, lesson])

        lesson_prev_index = lessons.index([UNIT, LESSON]) - 1
        lesson_next_index = lessons.index([UNIT, LESSON]) + 1

        if lesson_prev_index >= 0:
            lesson_prev = lessons[lesson_prev_index]
            truncated = "".join(lesson_prev).upper()
            lesson_prev_link = link(ROOT, LEVEL, "".join(lesson_prev))
            lesson_prev_text = ". ".join(
                [
                    f"Lesson {truncated}",
                    SITEMAP[LEVEL][lesson_prev[0]][lesson_prev[1]]["topic"],
                    # SITEMAP[LEVEL][lesson_prev[0]][lesson_prev[1]]["grammar"],
                    # SITEMAP[LEVEL][lesson_prev[0]][lesson_prev[1]]["vocabulary"],
                ]
            )
            nav_prev = html.A(
                href=lesson_prev_link,
                class_=["button", "prev"],
                aria_attrs={"aria-label": "Previous lesson"},
            )
            nav_prev += html.Svg(class_=["icon"]) + html.Use(href=icon("arrow-left"))
            nav_prev += html.Span(class_=["long"]) + lesson_prev_text
            nav_prev += html.Span(class_=["short"]) + truncated

        if lesson_next_index < len(lessons):
            lesson_next = lessons[lesson_next_index]
            truncated = "".join(lesson_next).upper()
            lesson_next_link = link(ROOT, LEVEL, "".join(lesson_next))
            lesson_next_text = ". ".join(
                [
                    f"Lesson {truncated}",
                    SITEMAP[LEVEL][lesson_next[0]][lesson_next[1]]["topic"],
                    # SITEMAP[LEVEL][lesson_next[0]][lesson_next[1]]["grammar"],
                    # SITEMAP[LEVEL][lesson_next[0]][lesson_next[1]]["vocabulary"],
                ]
            )
            nav_next = html.A(
                href=lesson_next_link,
                class_=["button", "next"],
                aria_attrs={"aria-label": "Next lesson"},
            )
            nav_next += html.Span(class_=["long"]) + lesson_next_text
            nav_next += html.Span(class_=["short"]) + truncated
            nav_next += html.Svg(class_=["icon"]) + html.Use(href=icon("arrow-right"))

    nav_up = html.A(
        href="#",
        class_=["button", "up"],
        aria_attrs={"aria-label": "To the top"},
    )
    nav_up += html.Svg(class_=["icon"]) + html.Use(href=icon("arrow-up"))

    nav += nav_prev
    nav += nav_up
    nav += nav_next

    footer += nav

    # # Back navigation
    # if len(PATH) > 2:
    #     path_parent = link(ROOT, *[crumb for crumb in PATH[1:-2]])

    #     nav_back = html.Nav(class_=["back"], aria_attrs={"aria-label": "Back"})
    #     nav_back += html.A(
    #         href=path_parent,
    #         class_=["button", "back"],
    #         inner_html=html.Span() + "Back",
    #     )

    #     footer += nav_back

    # Contacts
    footer += html.A(
        href="https://github.com/shushtain/kobza",
        class_=["credits"],
        inner_html=html.Small() + "Kobza, MIT 2025",
    )

    return footer


def parse_block(block, scope):
    """Main function for parsing sections"""

    if isinstance(block, list):
        subs = []
        for sub in block:
            subs.append(parse_block(sub, scope))
        return subs

    if isinstance(block, dict):

        content = block["content"] if "content" in block else None
        classes = []
        if "class" in block:
            classes = [x for x in block["class"].replace(",", "").split(" ") if x != ""]
        id_ = block["id"] if "id" in block else None
        mod = {}

        for key, value in block.items():
            if key not in ["type", "content", "class", "id"]:
                mod[key] = value

        package = [content, scope, classes, id_, mod]

        match block["type"]:
            # common
            case "section":
                return parse_section(*package)
            case "div":
                return parse_div(*package)
            case "h1":
                return parse_h1(*package)
            case "h2":
                return parse_h2(*package)
            case "h3":
                return parse_h3(*package)
            case "h4":
                return parse_h4(*package)
            case "p":
                return parse_p(*package)
            case "quote":
                return parse_blockquote(*package)
            case "aside":
                return parse_aside(*package)
            case "---":
                return html.Hr()
            case "ul":
                return parse_ul(*package)
            case "ol":
                return parse_ol(*package)
            case "cta":
                return parse_cta(*package)
            case "figure":
                return parse_figure(*package)

            # special
            case "toc":
                return parse_toc(*package)
            case "flashcards":
                return parse_flashcards(*package)
            case "ex-choice":
                return parse_ex_choice(*package)
            case "ex-fill":
                return parse_ex_fill(*package)
            case "ex-format":
                return parse_ex_format(*package)
            case "ex-order":
                return parse_ex_order(*package)
            case "ex-match":
                return parse_ex_match(*package)
            case "ex-match-img":
                return parse_ex_match_img(*package)
            case "ex-rate":
                return parse_ex_rate(*package)
            case "ex-verify":
                return parse_ex_verify(*package)

            # unknown types
            case _:
                return html.CommentHtml() + content

    return parse_inline(block)


def parse_section(content, scope, classes, id_, mod) -> html.Section:
    """Parse section"""
    section = html.Section(class_=classes, id=id_)
    section += parse_block(content, section)
    return section


def parse_div(content, scope, classes, id_, mod) -> html.Div:
    """Parse div"""
    div = html.Div(class_=classes, id=id_)
    div += parse_block(content, div)
    return div


def parse_h1(content, scope, classes, id_, mod) -> html.H1:
    """Parse h1"""
    h1 = html.H1(class_=classes, id=id_)

    match SCHEMA:

        case "lesson":
            h1 += html.Span() + f"Lesson {UNIT}{LESSON.upper()}:"
            h1 += html.Br()
            h1 += f"{content}"

        case _:
            h1 += parse_block(content, h1)

    return h1


def parse_h2(content, scope, classes, id_, mod) -> html.H2:
    """Parse h2"""
    h2 = html.H2(class_=classes, id=id_)

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


def parse_h3(content, scope, classes, id_, mod) -> html.H3:
    """Parse h3"""
    h3 = html.H3(class_=classes, id=id_)
    h3 += parse_block(content, h3)
    return h3


def parse_h4(content, scope, classes, id_, mod) -> html.H4:
    """Parse h4"""
    h4 = html.H4(class_=classes, id=id_)
    h4 += parse_block(content, h4)
    return h4


def parse_p(content, scope, classes, id_, mod) -> html.P:
    """Parse p"""
    p = html.P(class_=classes, id=id_)
    p += parse_block(content, p)
    return p


def parse_ul(content, scope, classes, id_, mod) -> html.Ul:
    """Parse ul"""
    ul = html.Ul(class_=classes, id=id_)

    for item in content:
        li = html.Li()
        ul += li + parse_block(item, li)

    return ul


def parse_ol(content, scope, classes, id_, mod) -> html.Ol:
    """Parse ol"""
    ol = html.Ol(class_=classes, id=id_)

    for item in content:
        li = html.Li()
        ol += li + parse_block(item, li)

    return ol


def parse_blockquote(content, scope, classes, id_, mod) -> html.Blockquote:
    """Parse blockquote"""
    blockquote = html.Blockquote(class_=classes, id=id_)
    blockquote += html.P() + parse_block(content, blockquote)

    if "source" in mod:
        cite = html.Cite()
        blockquote += cite + parse_block(mod["source"], cite)

    return blockquote


def parse_aside(content, scope, classes, id_, mod) -> html.Aside:
    """Parse aside"""
    aside = html.Aside(class_=classes, id=id_)
    aside += parse_block(content, aside)
    return aside


def parse_cta(content, scope, classes, id_, mod) -> html.A:
    """Parse Call to Action"""
    cta = html.A(class_=classes + ["button"], id=id_)

    text = content["text"]
    title = content["title"] if "title" in content else None
    href, target = parse_raw_link(content["link"])
    target = content["target"] if "target" in content else target

    if "mail" in classes or "mailto:" in href:
        cta += html.Svg(class_=["icon"]) + html.Use(href=icon("mail"))
    elif "file" in classes:
        cta += html.Svg(class_=["icon"]) + html.Use(href=icon("file"))

    cta.href = href
    cta.title = title
    cta.target = target
    cta += html.Span() + text

    if "download" in classes:
        cta += html.Svg(class_=["icon"]) + html.Use(href=icon("download"))
    elif "more" in classes:
        cta += html.Svg(class_=["icon"]) + html.Use(href=icon("arrow-right"))

    return cta


def parse_figure(content, scope, classes, id_, mod) -> html.Figure:
    """Parse figure"""
    figure = html.Figure(class_=classes, id=id_)

    src = content["img"]
    alt = content["alt"] if "alt" in content else ""
    figure += html.Img(src=src, alt=alt)

    if "figcaption" in content:
        figcaption = parse_inline(content["figcaption"])
        figure += html.Figcaption(class_=["subtle"]) + figcaption

    return figure


def parse_toc(content, scope, classes, id_, mod) -> html.Div:
    """Parse Table of Contents"""
    toc = html.Div(class_=classes + ["toc"], id=id_)
    toc.id = f"toc-{SCHEMA}" if id_ is None else id_

    match SCHEMA:

        case "main":
            for level in SITEMAP:
                card = html.A(
                    href=link(ROOT, level),
                    class_=["tile", level],
                )
                text = html.Span() + level.upper()
                toc += card + text

        case "level":
            for unit, lessons in SITEMAP[LEVEL].items():
                ul = html.Ul()
                for lesson, topics in lessons.items():
                    card = html.A(
                        href=link(ROOT, LEVEL, unit + lesson),
                        class_=["button"],
                    )
                    text = html.Span() + ". ".join(
                        [
                            f"Lesson {unit + lesson.upper()}",
                            topics["topic"],
                            # topics["grammar"],
                            # topics["vocabulary"],
                        ]
                    )
                    text += html.Br()
                    text += html.Small() + ". ".join(
                        [topics["grammar"], topics["vocabulary"]]
                    )
                    card += text
                    ul += html.Li() + card
                toc += html.Section() + html.H3(inner_html=f"Unit {unit}") + ul

    return toc


def parse_flashcards(content, scope, classes, id_, mod) -> html.Div:
    """Parse flashcards"""
    flashcards_wrapper = html.Div(class_=["flashcards-wrapper"])

    # controls

    flashcards_controls = html.Div(class_=["controls"])
    toggle_flashcards = html.Button(
        type="button", class_=["button", "toggle-flashcards"]
    )
    toggle_flashcards += html.Svg(class_=["icon", "toggle-show"]) + html.Use(
        href=icon("show")
    )
    toggle_flashcards += html.Svg(class_=["icon", "toggle-hide"]) + html.Use(
        href=icon("hide")
    )
    toggle_flashcards += html.Span() + "Show answers"
    flashcards_controls += toggle_flashcards

    flashcards_wrapper += flashcards_controls

    # flashcards

    flashcards = html.Div(class_=classes + ["flashcards"], id=id_)

    for item in content:
        term = item["q"]
        definition = item["a"]
        img_link = item["img"] if "img" in item else None
        img_alt = item["alt"] if "alt" in item else ""

        card = html.Div(class_=["flashcard", "tile"], tabindex="0")

        if img_link:
            card += html.Img(src=img_link, alt=img_alt)

        dl = html.Dl()
        dl += html.Dt() + term
        if isinstance(definition, list):
            for line in definition:
                dl += html.Dd() + line
        else:
            dl += html.Dd() + definition

        card += dl
        flashcards += card

    flashcards_wrapper += flashcards

    return flashcards_wrapper


def parse_ex_choice(content, scope, classes, id_, mod) -> html.Div:
    """Parse ex-choice"""
    ex_choice = html.Div(class_=classes + ["exercise", "ex-choice"], id=id_)
    tasks = html.Ol(class_=["tasks"])

    for line in content:
        task = html.Li(class_=["task"])

        q = html.Div(class_=["q"])
        q_elems = line["q"].split("|")
        for i, elem in enumerate(q_elems):
            if i % 2 == 0:
                q += elem
            else:
                text = html.Span() + elem.strip()
                q += html.Button(type="button") + text
        task += q

        a = html.Div(class_=["a"])
        a_elems = line["a"].split("|")
        for i, elem in enumerate(a_elems):
            text = html.Span() + elem.strip()
            a += html.Button(type="button") + text
        task += a

        tasks += task

    ex_choice += tasks
    return ex_choice


def parse_ex_fill(content, scope, classes, id_, mod) -> html.Div:
    """Parse ex-fill"""
    ex_fill = html.Div(class_=classes + ["exercise", "ex-fill"], id=id_)
    tasks = html.Ol(class_=["tasks"])

    for line in content:
        task = html.Li(class_=["task"])
        elems = line.split("|")
        for i, elem in enumerate(elems):
            if i % 2 == 0:
                task += elem
            else:
                text = html.Span() + elem.strip()
                task += html.Button(type="button") + text
        tasks += task

    ex_fill += tasks
    return ex_fill


def parse_ex_format(content, scope, classes, id_, mod) -> html.Div:
    """Parse ex-format"""
    ex_format = html.Div(class_=classes + ["exercise", "ex-format"], id=id_)
    tasks = html.Ol(class_=["tasks"])

    for line in content:
        task = html.Li(class_=["task"])
        elems = line.split("|")
        for i, elem in enumerate(elems):
            if i % 2 == 0:
                task += elem
            else:
                parts = elem.split("/")
                q, a = "", ""
                if len(parts) == 2:
                    q = parts[0].strip()
                a = parts[-1].strip()
                tile = html.Button(type="button")
                tile += html.Span(class_=["q"]) + q
                tile += html.Span(class_=["a"]) + a
                task += tile
        tasks += task

    ex_format += tasks
    return ex_format


def parse_ex_order(content, scope, classes, id_, mod) -> html.Div:
    """Parse ex-order"""
    ex_order = html.Div(class_=classes + ["exercise", "ex-order"], id=id_)
    tasks = html.Ol(class_=["tasks"])

    for line in content:
        task = html.Li(class_=["task"])
        elems = line.split("|")
        for elem in elems:
            text = html.Span() + elem.strip()
            task += html.Button(type="button", class_=["draggable"]) + text
        tasks += task

    ex_order += tasks
    return ex_order


def parse_ex_match(content, scope, classes, id_, mod) -> html.Div:
    """Parse ex-match"""
    ex_match = html.Div(class_=classes + ["exercise", "ex-match"], id=id_)
    task = html.Ol(class_=["task"])
    ref = html.Ol(class_=["ref"])

    for line in content:
        q = html.Li()
        text = html.Span() + line["q"]
        q += html.Button(type="button", class_=["draggable"]) + text
        task += q

        a = html.Li()
        a += html.Span() + line["a"]
        ref += a

    ex_match += task + ref
    return ex_match


def parse_ex_match_img(content, scope, classes, id_, mod) -> html.Div:
    """Parse ex-match-img"""
    ex_match_img = html.Div(class_=classes + ["exercise", "ex-match-img"], id=id_)
    task = html.Ol(class_=["task"])
    ref = html.Ol(class_=["ref"])

    for line in content:
        q = html.Li()
        text = html.Span() + line["text"]
        q += html.Button(type="button", class_=["draggable"]) + text
        task += q

        a = html.Li()
        src = link(ROOT, line["img"])
        alt = line["alt"] if "alt" in line else ""
        a += html.Img(src=src, alt=alt)
        ref += a

    ex_match_img += task + ref
    return ex_match_img


# ! UNFINISHED
def parse_ex_rate(content, scope, classes, id_, mod) -> html.Div:
    """Parse ex-rate"""
    return html.Div()


# ! UNFINISHED
def parse_ex_verify(content, scope, classes, id_, mod) -> html.Div:
    """Parse ex-verify"""
    return html.Div()


def parse_inline(line) -> str:
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
        target = "_blank"

        href, target = parse_raw_link(href, target)

        sub = f"{html.A(href=href, target=target, title=title) + text}"
        line = pattern_link.sub(sub, line)

    return line


def parse_code(code) -> str:
    """Parse Markdown content of the code blocks into HTML"""

    code = code.strip()

    code = re.sub(r"&", "&amp;", code)
    code = re.sub(r"<", "&lt;", code)
    code = re.sub(r">", "&gt;", code)
    code = re.sub(r"  ", rf"{html.Br()}", code)

    return code


def parse_raw_link(href, target="_blank"):
    """Parse raw link syntax"""

    if href[0] == "~" and "/" in href:
        href = link(ROOT, *href.split("/")[1:])
        target = "_self"

    return (href, target)


def link(*parts, as_is=False):
    """Join parts of a path and return it"""

    # link raw if specified
    if as_is:
        return "/".join(parts)

    # check if directory
    is_directory = False

    # empty string -> not directory
    if parts[-1] != "":
        # no file extension -> directory
        # ends on the relative '.' -> directory
        if "." not in parts[-1] or parts[-1][-1] == ".":
            is_directory = True

    return "/".join(parts) + ("/" if is_directory else "")


def icon(icon_name: str):
    """Return a link to an icon"""

    return link(ROOT, "icons", f"sprite.svg#{icon_name}")
