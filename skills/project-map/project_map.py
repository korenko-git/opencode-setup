#!/usr/bin/env python3
"""
project_map.py - generates a "project map": a file tree plus class/function
signatures without implementation bodies (similar to C++ .h files).

Purpose: give a planning LLM a compact view of the code structure (file names,
classes, methods, functions, parameters, docstrings) without the function code
itself, so context is not wasted on implementation details.

Usage:
    python project_map.py <path_to_project> [options]

Options:
    --out FILE            Where to write the map (default: PROJECT_MAP.md)
    --exclude DIRS        Comma-separated list of directories to exclude
                          (default: .git,node_modules,venv,.venv,
                          __pycache__,dist,build,.next,target,.idea,.vscode)
    --ext EXTS            Comma-separated list of extensions to parse into
                          signatures (default: .py,.js,.jsx,.ts,.tsx)
    --max-bytes N         Files larger than N bytes are marked as "large file"
                          and are not parsed line-by-line (default: 300000)
    --docstring-chars N   How many docstring/comment characters to keep
                          (default: 160)
    --stdout              Also print the map to stdout

Example:
    python project_map.py /home/user/myrepo --out PROJECT_MAP.md

Language support:
    - Python: precise parsing via the ast module (imports, classes, methods,
      functions, decorators, type annotations, docstrings,
      async/staticmethod/classmethod/property).
    - JS/JSX/TS/TSX: regex-based best-effort parsing: function declarations,
      arrow functions in const/let/var, classes and their methods,
      export/export default. Complex or unusual constructs may be parsed
      imperfectly - in that case the line is included in the map "as is"
      without removing the body (safe fallback).
    - Other text files: included in the tree with size/line count; content is
      not included.
    - Binary files: shown only in the tree, marked as [binary].
"""

import argparse
import ast
import os
import re
import sys
from pathlib import Path

DEFAULT_EXCLUDE_DIRS = {
    ".git", "node_modules", "venv", ".venv", "__pycache__", "dist", "build",
    ".next", "target", ".idea", ".vscode", ".pytest_cache", ".mypy_cache",
    "egg-info", ".tox", "coverage", ".ruff_cache",
}
DEFAULT_PARSE_EXTS = {".py", ".js", ".jsx", ".ts", ".tsx"}

BINARY_EXTS = {
    ".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico", ".pdf", ".zip", ".gz",
    ".tar", ".exe", ".dll", ".so", ".dylib", ".woff", ".woff2", ".ttf",
    ".eot", ".mp3", ".mp4", ".mov", ".sqlite", ".db", ".pyc", ".class",
}


# --------------------------------------------------------------------------
# Python
# --------------------------------------------------------------------------

def _truncate(text, n):
    text = " ".join(text.split())
    if len(text) > n:
        return text[: n - 1].rstrip() + "…"
    return text


def _py_format_args(args: ast.arguments) -> str:
    parts = []

    def ann_str(node):
        if node is None:
            return None
        try:
            return ast.unparse(node)
        except Exception:
            return None

    posonly = getattr(args, "posonlyargs", [])
    all_pos = list(posonly) + list(args.args)
    defaults = list(args.defaults)
    n_no_default = len(all_pos) - len(defaults)

    for i, a in enumerate(all_pos):
        s = a.arg
        ann = ann_str(a.annotation)
        if ann:
            s += f": {ann}"
        if i >= n_no_default:
            default = defaults[i - n_no_default]
            try:
                s += f" = {ast.unparse(default)}"
            except Exception:
                s += " = ..."
        parts.append(s)
        if posonly and i == len(posonly) - 1:
            parts.append("/")

    if args.vararg:
        s = f"*{args.vararg.arg}"
        ann = ann_str(args.vararg.annotation)
        if ann:
            s += f": {ann}"
        parts.append(s)
    elif args.kwonlyargs:
        parts.append("*")

    for a, d in zip(args.kwonlyargs, args.kw_defaults):
        s = a.arg
        ann = ann_str(a.annotation)
        if ann:
            s += f": {ann}"
        if d is not None:
            try:
                s += f" = {ast.unparse(d)}"
            except Exception:
                s += " = ..."
        parts.append(s)

    if args.kwarg:
        s = f"**{args.kwarg.arg}"
        ann = ann_str(args.kwarg.annotation)
        if ann:
            s += f": {ann}"
        parts.append(s)

    return ", ".join(parts)


def _py_decorators(node) -> list:
    out = []
    for d in getattr(node, "decorator_list", []):
        try:
            out.append("@" + ast.unparse(d))
        except Exception:
            out.append("@<decorator>")
    return out


def _py_signature(node, doc_chars) -> list:
    lines = []
    for dec in _py_decorators(node):
        lines.append(dec)

    prefix = "async def" if isinstance(node, ast.AsyncFunctionDef) else "def"
    args_str = _py_format_args(node.args)
    ret = ""
    if node.returns is not None:
        try:
            ret = f" -> {ast.unparse(node.returns)}"
        except Exception:
            pass
    lines.append(f"{prefix} {node.name}({args_str}){ret}: ...")

    doc = ast.get_docstring(node)
    if doc:
        lines.append(f'    """{_truncate(doc, doc_chars)}"""')
    return lines


def parse_python(source: str, doc_chars: int):
    """Return a list of map lines for a Python file."""
    out = []
    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        return [f"# [parse error: {e}] - file included without parsing"]

    module_doc = ast.get_docstring(tree)
    if module_doc:
        out.append(f'"""{_truncate(module_doc, doc_chars)}"""')

    imports = []
    for node in tree.body:
        if isinstance(node, ast.Import):
            names = ", ".join(a.name + (f" as {a.asname}" if a.asname else "") for a in node.names)
            imports.append(f"import {names}")
        elif isinstance(node, ast.ImportFrom):
            mod = "." * (node.level or 0) + (node.module or "")
            names = ", ".join(a.name + (f" as {a.asname}" if a.asname else "") for a in node.names)
            imports.append(f"from {mod} import {names}")
    if imports:
        out.extend(imports)
        out.append("")

    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            out.extend(_py_signature(node, doc_chars))
            out.append("")
        elif isinstance(node, ast.ClassDef):
            bases = []
            for b in node.bases:
                try:
                    bases.append(ast.unparse(b))
                except Exception:
                    pass
            base_str = f"({', '.join(bases)})" if bases else ""
            for dec in _py_decorators(node):
                out.append(dec)
            out.append(f"class {node.name}{base_str}:")
            doc = ast.get_docstring(node)
            if doc:
                out.append(f'    """{_truncate(doc, doc_chars)}"""')

            class_vars = []
            body_items = []
            for item in node.body:
                if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    body_items.append(item)
                elif isinstance(item, ast.AnnAssign) and isinstance(item.target, ast.Name):
                    try:
                        ann = ast.unparse(item.annotation)
                    except Exception:
                        ann = "?"
                    class_vars.append(f"    {item.target.id}: {ann}")
                elif isinstance(item, ast.Assign):
                    for t in item.targets:
                        if isinstance(t, ast.Name):
                            class_vars.append(f"    {t.id} = ...")

            if class_vars:
                out.extend(class_vars)

            if not body_items and not class_vars and not doc:
                out.append("    pass")

            for item in body_items:
                for line in _py_signature(item, doc_chars):
                    out.append("    " + line if line else "")
            out.append("")

    return out


# --------------------------------------------------------------------------
# JS / TS (best-effort, regex-based)
# --------------------------------------------------------------------------

JS_FUNC_DECL = re.compile(
    r'^\s*(export\s+)?(default\s+)?(async\s+)?function\s*\*?\s*([A-Za-z0-9_$]+)\s*\(([^)]*)\)\s*(:\s*[^\{]+)?\s*\{'
)
JS_ARROW_CONST = re.compile(
    r'^\s*(export\s+)?(default\s+)?(const|let|var)\s+([A-Za-z0-9_$]+)\s*(:\s*[^=]+)?=\s*(async\s+)?\(([^)]*)\)\s*(:\s*[^=]+)?=>\s*[\{]'
)
JS_CLASS_DECL = re.compile(
    r'^\s*(export\s+)?(default\s+)?class\s+([A-Za-z0-9_$]+)\s*(extends\s+[A-Za-z0-9_.$]+)?\s*\{'
)
JS_METHOD = re.compile(
    r'^\s*((?:(?:public|private|protected|static|async|readonly)\s+)*)'
    r'([A-Za-z0-9_$]+)\s*\(([^)]*)\)\s*(:\s*[^\{]+)?\s*\{'
)
JS_IMPORT = re.compile(r'^\s*import\s+.+from\s+[\'"].+[\'"];?\s*$')
JS_EXPORT_DEFAULT_NAME = re.compile(r'^\s*export\s+default\s+([A-Za-z0-9_$]+)\s*;?\s*$')


def _brace_delta(line: str) -> int:
    """Rough brace balance count for a line.

    Ignores strings/comments - good enough for best-effort parsing, but not a
    fully accurate parser.
    """
    return line.count("{") - line.count("}")


def _skip_body(lines, i, n, depth, target_depth):
    """Skip function/class body lines until depth returns to target_depth.

    Returns (new_index, new_depth).
    """
    while i < n and depth > target_depth:
        depth += _brace_delta(lines[i])
        i += 1
    return i, depth


def parse_jsts(source: str, doc_chars: int):
    """Best-effort JS/TS parsing with brace nesting awareness.

    This prevents a method body from terminating class parsing too early.
    """
    out = []
    lines = source.split("\n")
    n = len(lines)
    i = 0
    depth = 0
    class_body_depth = None  # depth corresponding to "inside the class body"

    while i < n:
        line = lines[i]
        stripped = line.strip()

        # Inside a class: look for methods or the end of the class
        if class_body_depth is not None and depth == class_body_depth:
            if stripped == "}":
                out.append("}")
                depth += _brace_delta(line)
                class_body_depth = None
                i += 1
                continue

            m = JS_METHOD.match(line) if "class " not in line else None
            if m:
                mods, name, args, ret = m.groups()
                mods = (mods or "").strip()
                head = f"  {mods + ' ' if mods else ''}{name}({args.strip()})"
                if ret:
                    head += ret.rstrip()
                out.append(head + " { ... }")
                new_depth = depth + _brace_delta(line)
                i += 1
                i, depth = _skip_body(lines, i, n, new_depth, depth)
                continue

            # Class property / comment - skip without output
            depth += _brace_delta(line)
            i += 1
            continue

        # Top level (depth == 0): classes, functions, imports, named default export
        if depth == 0:
            if JS_IMPORT.match(line):
                out.append(stripped)
                i += 1
                continue

            m = JS_CLASS_DECL.match(line)
            if m:
                export, default, name, extends = m.groups()
                head = ""
                if export:
                    head += "export "
                if default:
                    head += "default "
                head += f"class {name}"
                if extends:
                    head += f" {extends}"
                out.append(head + " {")
                depth += _brace_delta(line)
                class_body_depth = depth
                i += 1
                continue

            m = JS_FUNC_DECL.match(line)
            if m:
                export, default, is_async, name, args, ret = m.groups()
                head = ""
                if export:
                    head += "export "
                if default:
                    head += "default "
                if is_async:
                    head += "async "
                head += f"function {name}({args.strip()})"
                if ret:
                    head += ret.rstrip()
                out.append(head.rstrip() + " { ... }")
                new_depth = depth + _brace_delta(line)
                i += 1
                i, depth = _skip_body(lines, i, n, new_depth, depth)
                continue

            m = JS_ARROW_CONST.match(line)
            if m:
                export, default, kind, name, typ, is_async, args, ret = m.groups()
                head = ""
                if export:
                    head += "export "
                if default:
                    head += "default "
                head += f"{kind} {name}"
                if typ:
                    head += typ.rstrip()
                head += " = "
                if is_async:
                    head += "async "
                head += f"({args.strip()})"
                if ret:
                    head += ret.rstrip()
                out.append(head + " => { ... }")
                new_depth = depth + _brace_delta(line)
                i += 1
                i, depth = _skip_body(lines, i, n, new_depth, depth)
                continue

            m = JS_EXPORT_DEFAULT_NAME.match(line)
            if m:
                out.append(stripped)
                i += 1
                continue

        depth += _brace_delta(line)
        i += 1

    return out


# --------------------------------------------------------------------------
# File system traversal
# --------------------------------------------------------------------------

def should_skip_dir(name: str, exclude_dirs: set) -> bool:
    return name in exclude_dirs or name.startswith(".") and name not in {".", ".."}


def build_tree_lines(root: Path, exclude_dirs: set):
    """Build a textual file tree (similar to `tree`)."""
    lines = []

    def walk(dir_path: Path, prefix: str):
        try:
            entries = sorted(
                [e for e in dir_path.iterdir()
                 if not (e.is_dir() and should_skip_dir(e.name, exclude_dirs))],
                key=lambda e: (e.is_file(), e.name.lower()),
            )
        except PermissionError:
            return
        for idx, entry in enumerate(entries):
            connector = "└── " if idx == len(entries) - 1 else "├── "
            lines.append(prefix + connector + entry.name + ("/" if entry.is_dir() else ""))
            if entry.is_dir():
                extension = "    " if idx == len(entries) - 1 else "│   "
                walk(entry, prefix + extension)

    lines.append(root.name + "/")
    walk(root, "")
    return lines


def iter_files(root: Path, exclude_dirs: set):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if not should_skip_dir(d, exclude_dirs)]
        for fn in sorted(filenames):
            yield Path(dirpath) / fn


def generate_map(root: Path, out_path: Path, exclude_dirs: set, parse_exts: set,
                  max_bytes: int, doc_chars: int) -> str:
    parts = []
    parts.append(f"# Project Map: {root.resolve()}\n")
    parts.append(
        "Generated automatically by project_map.py. "
        "This is the code structure (files, classes, functions, signatures) WITHOUT function bodies - "
        "use it for planning; open the relevant file to inspect the implementation.\n"
    )

    parts.append("## File Tree\n")
    parts.append("```")
    parts.extend(build_tree_lines(root, exclude_dirs))
    parts.append("```\n")

    parts.append("## Signatures By File\n")

    file_count = 0
    parsed_count = 0

    for fpath in iter_files(root, exclude_dirs):
        if fpath.resolve() == out_path.resolve():
            continue
        file_count += 1
        rel = fpath.relative_to(root)
        ext = fpath.suffix.lower()

        if ext in BINARY_EXTS:
            parts.append(f"### `{rel}`\n[binary file]\n")
            continue

        try:
            size = fpath.stat().st_size
        except OSError:
            continue

        if ext not in parse_exts:
            try:
                with open(fpath, "r", encoding="utf-8", errors="replace") as f:
                    n_lines = sum(1 for _ in f)
                parts.append(f"### `{rel}`\n{n_lines} lines, {size} bytes (not parsed into signatures)\n")
            except Exception:
                parts.append(f"### `{rel}`\n{size} bytes\n")
            continue

        if size > max_bytes:
            parts.append(f"### `{rel}`\n[file {size} bytes - exceeds --max-bytes, not parsed]\n")
            continue

        try:
            source = fpath.read_text(encoding="utf-8", errors="replace")
        except Exception as e:
            parts.append(f"### `{rel}`\n[read error: {e}]\n")
            continue

        if ext == ".py":
            body_lines = parse_python(source, doc_chars)
        else:
            body_lines = parse_jsts(source, doc_chars)

        parsed_count += 1
        lang = ext.lstrip(".")
        parts.append(f"### `{rel}`")
        parts.append(f"```{lang}")
        parts.extend(body_lines if body_lines else ["# (empty / no top-level signatures)"])
        parts.append("```\n")

    parts.append(f"\n---\nTotal files: {file_count}, parsed into signatures: {parsed_count}\n")
    return "\n".join(parts)


def main():
    ap = argparse.ArgumentParser(description="Project map generator (signatures without function bodies)")
    ap.add_argument("root", help="Path to the project root")
    ap.add_argument("--out", default="PROJECT_MAP.md", help="Path to the output file")
    ap.add_argument("--exclude", default=",".join(sorted(DEFAULT_EXCLUDE_DIRS)),
                     help="Comma-separated directories to exclude")
    ap.add_argument("--ext", default=",".join(sorted(DEFAULT_PARSE_EXTS)),
                     help="Comma-separated extensions to parse into signatures")
    ap.add_argument("--max-bytes", type=int, default=300_000,
                     help="Maximum file size to parse")
    ap.add_argument("--docstring-chars", type=int, default=160,
                     help="How many docstring characters to keep")
    ap.add_argument("--stdout", action="store_true", help="Also print the result to stdout")
    args = ap.parse_args()

    root = Path(args.root).resolve()
    if not root.exists():
        print(f"Error: path not found: {root}", file=sys.stderr)
        sys.exit(1)

    exclude_dirs = set(x.strip() for x in args.exclude.split(",") if x.strip())
    parse_exts = set(("." + x.strip().lstrip(".")) for x in args.ext.split(",") if x.strip())
    out_path = Path(args.out).resolve()

    content = generate_map(
        root=root,
        out_path=out_path,
        exclude_dirs=exclude_dirs,
        parse_exts=parse_exts,
        max_bytes=args.max_bytes,
        doc_chars=args.docstring_chars,
    )

    out_path.write_text(content, encoding="utf-8")
    print(f"Project map written to: {out_path}")

    if args.stdout:
        print(content)


if __name__ == "__main__":
    main()
