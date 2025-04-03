"""Format HTML with Prettier."""

import subprocess


def prettify(page, npx_path):
    """Format the page with Prettier."""
    try:
        process = subprocess.Popen(
            [npx_path, "prettier", "--parser", "html", "--stdin"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except subprocess.SubprocessError as e:
        raise ModuleNotFoundError(
            f"{e}\nPrettier not found. Please install Prettier through npx and try again."
        ) from e

    stdout, stderr = process.communicate(input=page.encode("utf-8"))

    if process.returncode == 0:
        return stdout.decode("utf-8")

    print(f"Prettier error: {stderr.decode('utf-8')}")
    return page
