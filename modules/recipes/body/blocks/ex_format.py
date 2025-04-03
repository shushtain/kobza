"""Exercise: Format"""

import pyghtml as html


def parse(
    content: list,
    classes: list,
    id_: str,
) -> html.Div:
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
                tile = html.Button(type="button", class_=["error"])
                tile += html.Span(class_=["q"]) + q
                tile += html.Span(class_=["a"]) + a
                task += tile
        tasks += task

    ex_format += tasks
    return ex_format
