import re


def main():
    with open("test.columnson", encoding="utf-8") as f:
        file = f.read()
    print(loads(file))


def loads(file):
    data = file.split("\n")
    return parse(data, scope=[])


def parse(data, scope, level=-1, tab=4):

    # finish at the end of the file
    if len(data) == 0:
        return scope[0]

    # initialize scope
    if len(scope) == 0:
        scope.append({})

    line = data[0]
    content = line.strip()
    rest = data[1:]

    # skip empty strings
    if re.search(r"^\s*$", line):
        return parse(rest, scope, level, tab)

    # skip comments
    if re.search(r"^\s*//.*$", line):
        return parse(rest, scope, level, tab)

    # honor indentation
    level_new = re.search(r"^\s*", line).end() // tab
    indent = level_new - level
    scope = scope[:-1] if indent <= 0 else scope
    scope = scope[:indent] if indent < 0 else scope

    # start a list inside a dict
    if re.search(r"^\s*\w+\s*::\s*$", line):
        key = content.split("::")[0].strip()
        temp = []
        scope[-1][key] = temp
        scope.append(temp)
        return parse(rest, scope, level_new, tab)

    # start a list inside a list
    if re.search(r"^\s*::\s*$", line):
        temp = []
        scope[-1].append(temp)
        scope.append(temp)
        return parse(rest, scope, level_new, tab)

    # start a dict inside a dict
    if re.search(r"^\s*\w+\s*:::\s*$", line):
        key = content.split(":::")[0].strip()
        temp = {}
        scope[-1][key] = temp
        scope.append(temp)
        return parse(rest, scope, level_new, tab)

    # start a dict inside a list
    if re.search(r"^\s*:::\s*$", line):
        temp = {}
        scope[-1].append(temp)
        scope.append(temp)
        return parse(rest, scope, level_new, tab)

    # process key-value pairs
    if re.search(r"^\s*\w+\s*::\s*.+\s*$", line):
        key, value = content.split("::")
        key, value = key.strip(), value.strip()

        value = parse_value(value)

        scope[-1][key] = value
        scope.append(value)
        return parse(rest, scope, level_new, tab)

    # process other lines as list items
    if isinstance(scope[-1], list):

        value = parse_value(content)

        try:
            scope[-1].append(value)
        except:
            return f"{scope[-1]} is not a list. 103"

        scope.append(value)
        return parse(rest, scope, level_new, tab)

    return "ERROR"


def parse_value(value):

    if value == "...":
        return ""

    return value


if __name__ == "__main__":
    main()
