"""Exercise: Choice"""

import pyghtml as html


def parse(
    content: list,
    classes: list,
    id_: str,
) -> html.Div:
    """Parse ex-choice"""

    ex_choice = html.Div(class_=classes + ["exercise", "ex-choice"], id=id_)
    tasks = html.Ol(class_=["tasks"])

    for line in content:
        if isinstance(line, str):
            task = html.Li(class_=["task", "no-shuffle"])
            q = html.Div(class_=["q"])
            a = html.Div(class_=["a"])
            q += line[1:].strip()
            true = html.Button(type="button") + (html.Span() + "True")
            false = html.Button(type="button") + (html.Span() + "False")
            if line[0] == "+":
                true.class_ = ["true"]
            else:
                false.class_ = ["true"]
            a += true
            a += false
        else:
            task = html.Li(class_=["task"])
            q = html.Div(class_=["q"])
            a = html.Div(class_=["a"])
            q_elems = line["q"].split("|")
            for i, elem in enumerate(q_elems):
                if i % 2 == 0:
                    q += elem
                else:
                    q += html.Span(class_=["gap"]) + "___"

            for i, option in enumerate(line["a"]):
                text = html.Span() + option.strip()
                button = html.Button(type="button") + text
                if i == 0:
                    button.class_ = ["true"]
                a += button

        task += q
        task += a
        tasks += task

    ex_choice += tasks
    return ex_choice
