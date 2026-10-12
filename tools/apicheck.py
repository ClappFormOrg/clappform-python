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

griffe skips ``clappform.gen``. Those modules are protoc output whose
module-level ``DESCRIPTOR`` holds the serialized FileDescriptorProto, so every
regeneration reports a multi-kilobyte value change that says nothing about the
surface anyone calls. Users still read fields off the raw request and response
messages, so a second pass decodes that serialized descriptor from each
``_pb2.py`` in both trees and reports every message or field that went away.
A renamed field shows up as a removal of the old name.

Exits 1 when breakages are found, 0 when there are none.
"""

from __future__ import annotations

import argparse
import ast
import subprocess
import sys
from collections.abc import Iterable, Iterator
from pathlib import Path

import griffe
from google.protobuf import descriptor_pb2

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


def serialized_descriptor(source: str) -> bytes | None:
    """Return the FileDescriptorProto bytes a protoc ``_pb2.py`` registers."""
    for node in ast.walk(ast.parse(source)):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr == "AddSerializedFile"
            and node.args
            and isinstance(node.args[0], ast.Constant)
            and isinstance(node.args[0].value, bytes)
        ):
            return node.args[0].value
    return None


def _messages(
    messages: Iterable[descriptor_pb2.DescriptorProto], prefix: str
) -> Iterator[tuple[str, list[str]]]:
    for message in messages:
        if message.options.map_entry:
            continue  # synthetic entry type of a map field, not a class anyone reads
        name = f"{prefix}{message.name}"
        yield name, [field.name for field in message.field]
        yield from _messages(message.nested_type, f"{name}.")


def message_fields(sources: dict[str, str], search: str) -> dict[str, tuple[str, set[str]]]:
    """Map each generated message class path to (pb2 file, field names).

    *sources* maps a repo-relative ``_pb2.py`` path to its source text.
    """
    found: dict[str, tuple[str, set[str]]] = {}
    for path, source in sources.items():
        data = serialized_descriptor(source)
        if data is None:
            continue
        module = path.removeprefix(f"{search}/").removesuffix(".py").replace("/", ".")
        file = descriptor_pb2.FileDescriptorProto.FromString(data)
        for name, fields in _messages(file.message_type, f"{module}."):
            found[name] = (path, set(fields))
    return found


def proto_breakages(
    old: dict[str, tuple[str, set[str]]], new: dict[str, tuple[str, set[str]]]
) -> list[tuple[str, str]]:
    """Return (file, message) for each message or field that *new* lacks."""
    breakages = []
    for name, (path, fields) in sorted(old.items()):
        if name not in new:
            breakages.append((path, f"{name}: Proto message was removed"))
            continue
        new_path, new_fields = new[name]
        breakages += [
            (new_path, f"{name}.{field}: Proto field was removed")
            for field in sorted(fields - new_fields)
        ]
    return breakages


def pb2_sources_at(ref: str, root: str) -> dict[str, str]:
    """Read every ``_pb2.py`` under *root* at git *ref* in one ``cat-file`` call."""
    listing = subprocess.run(
        ["git", "ls-tree", "-r", "--name-only", ref, "--", root],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.split()
    paths = [path for path in listing if path.endswith("_pb2.py")]
    if not paths:
        return {}
    batch = subprocess.run(
        ["git", "cat-file", "--batch"],
        input="".join(f"{ref}:{path}\n" for path in paths).encode(),
        check=True,
        capture_output=True,
    ).stdout
    # Each object comes back as "<sha> blob <size>\n<content>\n".
    sources = {}
    offset = 0
    for path in paths:
        header_end = batch.index(b"\n", offset)
        size = int(batch[offset:header_end].split()[2])
        body = batch[header_end + 1 : header_end + 1 + size]
        sources[path] = body.decode("utf-8")
        offset = header_end + 1 + size + 1
    return sources


def pb2_sources_on_disk(root: str) -> dict[str, str]:
    return {
        path.as_posix(): path.read_text(encoding="utf-8")
        for path in sorted(Path(root).rglob("*_pb2.py"))
    }


def render_proto(file: str, message: str, style: str) -> str:
    if style == "github":
        return f"::warning file={file},title=API breakage::{message}"
    return f"{file}:-: {message}"


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    search = [args.search]

    old = griffe.load_git(args.package, ref=args.against, search_paths=search)
    new = griffe.load(args.package, search_paths=search)

    lines = [
        render(breakage, args.search, args.format)
        for breakage in griffe.find_breaking_changes(old, new)
        if not breakage.obj.path.startswith(SKIPPED_PREFIX)
    ]

    gen_root = f"{args.search}/{SKIPPED_PREFIX.replace('.', '/')}"
    old_fields = message_fields(pb2_sources_at(args.against, gen_root), args.search)
    new_fields = message_fields(pb2_sources_on_disk(gen_root), args.search)
    lines += [
        render_proto(file, message, args.format)
        for file, message in proto_breakages(old_fields, new_fields)
    ]

    for line in lines:
        print(line)

    if not lines:
        print(f"no public API breakage against {args.against}")
        return 0
    print(f"\n{len(lines)} public API breakage(s) against {args.against}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
