import subprocess
import sys
from pathlib import Path

from bs4 import BeautifulSoup

selectors = [
    ('script[language="Python"]', True),
    ("pre>code", False),
]

acceptable_ruff_format_errors = {
    "Expected a newline after line continuation character",
    "Expected a statement",
    "Simple statements must be separated by newlines or semicolons",
    "Expected an expression",
}

paths = [
    *Path(".").rglob("*.html"),
    *Path(".").rglob("*.htm"),
    # Can't use case_sensitive=False until Python 3.12
    *Path(".").rglob("*.HTM"),
]


def _elem_tag_start(raw: str, elem) -> int:
    lines = raw.splitlines(keepends=True)
    return sum(len(l) for l in lines[: elem.sourceline - 1]) + elem.sourcepos


def replace_elem_content(
    raw: str, tag_start: int, tag_name: str, new_content: str
) -> str:
    inner_start = raw.index(">", tag_start) + 1
    inner_end = raw.lower().index(f"</{tag_name}>", inner_start)
    return raw[:inner_start] + new_content + raw[inner_end:]


returncode = 0

for path in paths:
    try:
        raw = path.read_text(encoding="utf-8")
    except Exception as error:
        returncode = max(returncode, 1)
        # Likely a UnicodeDecodeError, but catch and print all
        print(f"\033[31m{path}: {error}\033[0m")

    soup = BeautifulSoup(raw, "html.parser")
    pending: list[tuple[int, str, str]] = []  # (tag_start, tag_name, formatted)

    for selector, strict in selectors:
        for elem in soup.select(selector):
            text = elem.get_text()
            if ">>>" in text:
                # Can't format REPL outside docstrings
                continue

            proc = subprocess.run(
                ["ruff", "format", "-"],
                input=text,
                text=True,
                capture_output=True,
            )

            if proc.returncode != 0:
                stderr = proc.stderr.strip()
                error_message = stderr.split(": ", 2)[-1]
                if strict or error_message not in acceptable_ruff_format_errors:
                    color = "\033[31m"
                    returncode = max(returncode, proc.returncode)
                else:
                    color = "\033[33m"
                    stderr = stderr.replace("error: ", "warning: ", 1)
                print(
                    f"{color}{path}:{elem.sourceline}:{elem.sourcepos}: {stderr}\033[0m",
                    file=sys.stderr,
                )
                continue

            formatted = proc.stdout.strip()
            if "\n" in formatted:
                # Multi-line: add surrounding newlines so tags are on their own line
                formatted = f"\n{proc.stdout.strip()}\n"

            if formatted != text:
                pending.append((_elem_tag_start(raw, elem), elem.name, formatted))

    if pending:
        print(f"Formatting {path}")
        for tag_start, tag_name, formatted in sorted(
            pending, key=lambda x: x[0], reverse=True
        ):
            raw = replace_elem_content(raw, tag_start, tag_name, formatted)
        path.write_text(raw, encoding="utf-8")

sys.exit(returncode)
