import subprocess
import sys
from pathlib import Path

from bs4 import BeautifulSoup

if sys.version_info >= (3, 12):
    paths = [
        *Path(".").rglob("*.html"),
        *Path(".").rglob("*.htm", case_sensitive=False),
    ]
else:
    paths = [
        *Path(".").rglob("*.html"),
        *Path(".").rglob("*.htm"),
        *Path(".").rglob("*.HTM"),
    ]

SELECTOR = 'script[language="Python"], code[lang="python"], pre>code:not([lang])'


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
        print(f"\033[31m{path}: {error}\033[0m", file=sys.stderr)

    soup = BeautifulSoup(raw, "html.parser")
    pending: list[tuple[int, str, str]] = []  # (tag_start, tag_name, formatted)

    for elem in soup.select(SELECTOR):
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
            returncode = max(returncode, proc.returncode)
            print(
                f"\033[31m{path}:{elem.sourceline}:{elem.sourcepos}: {stderr}\033[0m",
                file=sys.stderr,
            )
            continue

        formatted = proc.stdout.strip()
        if "\n" in formatted:
            # Single-line: Keep tags on the same line
            # Multi-line: add trailing newline so tags end on their own line
            # Do not add preceding newline as it'll get rendered in <pre>
            formatted = f"{proc.stdout.strip()}\n"

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
