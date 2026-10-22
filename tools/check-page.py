#!/usr/bin/env python3
"""Check that the simulation page is internally consistent.

Two things go wrong in a hand-built static page like this one, and neither
is caught by a browser until someone opens it:

1. A reference to a file that is not there -- a renamed script, a deleted
   stylesheet, an image moved into the wrong folder.
2. A script that does not parse, so half the page silently stops working.

Both are cheap to check, so they are checked on every push.

Usage
-----
    python3 tools/check-page.py
"""

from __future__ import annotations

import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HTML = ROOT / "index.html"

# References that are resolved by the browser rather than the filesystem.
EXTERNAL = re.compile(r"^(https?:|//|data:|mailto:|#)")

# src, href and the url() function in inline styles.
REF_RE = re.compile(r'(?:src|href)\s*=\s*["\']([^"\']+)["\']', re.IGNORECASE)
CSS_URL_RE = re.compile(r"url\(\s*['\"]?([^'\")]+)['\"]?\s*\)", re.IGNORECASE)


def local_references(html: str) -> set[str]:
    """Every local file the page refers to."""
    refs: set[str] = set()

    for match in REF_RE.findall(html):
        if EXTERNAL.match(match):
            continue
        refs.add(match.split("?")[0].split("#")[0])

    for match in CSS_URL_RE.findall(html):
        if EXTERNAL.match(match):
            continue
        refs.add(match.split("?")[0].split("#")[0])

    return {ref for ref in refs if ref}


def check_references(html: str) -> list[str]:
    """Report references that do not resolve to a file."""
    problems = []
    for ref in sorted(local_references(html)):
        if not (ROOT / ref.lstrip("/")).exists():
            problems.append(f"index.html refers to {ref}, which does not exist")
    return problems


def check_scripts_parse() -> list[str]:
    """Report JavaScript files that do not parse."""
    node = shutil.which("node")
    if not node:
        return []

    problems = []
    for script in sorted(ROOT.rglob("*.js")):
        if "node_modules" in script.parts:
            continue
        result = subprocess.run(
            [node, "--check", str(script)], capture_output=True, text=True, check=False
        )
        if result.returncode != 0:
            detail = result.stderr.strip().splitlines()
            reason = detail[0] if detail else "parse error"
            problems.append(f"{script.relative_to(ROOT)} does not parse: {reason}")
    return problems


def main() -> int:
    if not HTML.exists():
        print("error: index.html is missing", file=sys.stderr)
        return 2

    html = HTML.read_text(encoding="utf-8", errors="replace")

    problems = check_references(html) + check_scripts_parse()

    for problem in problems:
        print(f"  {problem}")

    if problems:
        print(f"\n{len(problems)} problem(s) found", file=sys.stderr)
        return 1

    scripts = len(list(ROOT.rglob("*.js")))
    print(f"ok: {len(local_references(html))} local references resolve, {scripts} scripts parse")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
