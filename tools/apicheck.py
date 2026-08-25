"""Report public API breakages between the working tree and a git ref.

The wrapper layer under ``clappform`` and the generated service layer under
``clappform.services`` are what the docs promise and what users import. Neither
the type checker nor the test suite notices when a method, a keyword argument
or a class disappears from that surface: mypy sees a consistent tree, and the
tests only cover what they happen to exercise. griffe diffs the two trees and
names every removal and signature change.

Usage:
    python tools/apicheck.py --against origin/Major/6
    python tools/apicheck.py --against v6.0.0a0 --format github

``clappform.gen`` is skipped. Those modules are protoc output whose
module-level ``DESCRIPTOR`` holds the serialized FileDescriptorProto, so every
regeneration reports a multi-kilobyte value change that says nothing about the
surface anyone calls. The service layer generated from the same protos carries
the same information in readable form.

Exits 1 when breakages are found, 0 when there are none.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import griffe

SKIPPED_PREFIX = "clappform.gen"

# A value change quotes the old and new value, which for a large default or a
# long type annotation runs to hundreds of characters. Keep a log line readable.
MAX_VALUE = 120


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Report public API breakages.")
    parser.add_argument(
        "--against",
        default="origin/Major/6",
        metavar="REF",
        help="git ref to diff the working tree against (default: %(default)s)",
    )
    parser.add_argument(
        "--package",
        default="clappform",
        help="package to load (default: %(default)s)",
    )
    parser.add_argument(
        "--search",
        default="src",
        help="path to search the package in, in both trees (default: %(default)s)",
    )
    parser.add_argument(
        "--format",
        choices=("text", "github"),
        default="text",
        help="'github' emits ::warning workflow commands (default: %(default)s)",
    )
    return parser.parse_args(argv)


def location(obj: griffe.Object, search: str) -> tuple[str, int | None]:
    """Return (repo-relative file, line) for *obj*, or (file, None) for a removal.

    griffe loads the older ref from a temporary git worktree, so anything that
    only exists there carries a path outside the repo and a line number that
    means nothing in the current tree. Keep the ``<search>/...`` tail of the
    path and drop the line.
    """
    filepath = obj.filepath
    if isinstance(filepath, list):  # namespace package: several source roots
        filepath = filepath[0]
    try:
        return filepath.relative_to(Path.cwd()).as_posix(), obj.lineno
    except ValueError:
        _, marker, tail = filepath.as_posix().partition(f"/{search}/")
        return f"{search}/{tail}" if marker else filepath.as_posix(), None


def clip(value: object) -> str:
    text = str(value)
    return text if len(text) <= MAX_VALUE else text[:MAX_VALUE] + " [...]"


def detail(breakage: griffe.Breakage) -> str:
    """Return the old/new pair worth printing, empty when it adds nothing."""
    if breakage.kind is griffe.BreakageKind.OBJECT_REMOVED:
        return ""  # the dotted path already names what went
    old, new = breakage.old_value, breakage.new_value
    if old is not None and new is not None:
        return f"{clip(old)} -> {clip(new)}"
    return clip(old) if old is not None else ""


def render(breakage: griffe.Breakage, search: str, style: str) -> str:
    message = f"{breakage.obj.path}: {breakage.kind.value}"
    if extra := detail(breakage):
        message += f" ({extra})"

    file, line = location(breakage.obj, search)
    if style == "github":
        anchor = f"file={file}" + (f",line={line}" if line else "")
        return f"::warning {anchor},title=API breakage::{message}"
    return f"{file}:{line if line else '-'}: {message}"


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    search = [args.search]

    old = griffe.load_git(args.package, ref=args.against, search_paths=search)
    new = griffe.load(args.package, search_paths=search)

    breakages = [
        breakage
        for breakage in griffe.find_breaking_changes(old, new)
        if not breakage.obj.path.startswith(SKIPPED_PREFIX)
    ]

    for breakage in breakages:
        print(render(breakage, args.search, args.format))

    if not breakages:
        print(f"no public API breakage against {args.against}")
        return 0
    print(f"\n{len(breakages)} public API breakage(s) against {args.against}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
