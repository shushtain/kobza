"""Exercise: Order"""

import pyghtml as html


def parse(
    content: list,
    classes: list,
    id_: str,
) -> html.Div:
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
