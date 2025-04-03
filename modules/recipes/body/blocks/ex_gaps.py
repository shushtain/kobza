"""Exercise: Gaps"""

import pyghtml as html


def parse(
    content: list,
    classes: list,
    id_: str,
) -> html.Div:
    """Parse ex-gaps"""

    ex_gaps = html.Div(class_=classes + ["exercise", "ex-gaps"], id=id_)
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

    ex_gaps += tasks
    return ex_gaps
