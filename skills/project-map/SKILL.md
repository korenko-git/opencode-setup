---
name: project-map
description: Use this skill when you need to build a "project map" - a compact representation of the codebase structure (file tree + class/function signatures WITHOUT implementation bodies, similar to C++ .h headers). Triggers: the user asks "make a project map", "show the code structure without implementation", "I need a codebase overview for another agent/planner", "update the map after changes", or "compress the project down to signatures". Also use it proactively when the user describes a workflow like "cloud planning agent + local implementation model" that needs compact structural context without spending tokens on function bodies.
---

# Project Map - project map (signatures without implementation)

## Why This Exists

When a codebase is large, you cannot pass the whole repository into the context
of a model that only does planning (for example, a cloud agent that does not
write code and only decides what to change and where). It does not need
function bodies - only: which files exist, which classes/functions they
contain, what their signatures are, and any top-level docstrings/comments. This
is similar to C++ header files (`.h`): the interface is visible, the
implementation is hidden.

The local implementation model then:
1. Reads the map and receives a plan from the planner.
2. Opens the specific required files in full (the map is not a replacement for
   reading code; it is a navigator).
3. Writes or edits code.
4. **Runs the script again** to refresh the map to match the current repository
   state - the map must be regenerated after every meaningful structural change
   (new functions/classes/files), not edited manually.

## How To Use It

The script is located at `scripts/project_map.py`. It is a standalone Python
script with no external dependencies (stdlib only: `ast`, `re`, `os`,
`argparse`).

Basic usage:

```bash
python3 scripts/project_map.py /path/to/project --out PROJECT_MAP.md
```

Useful options:

| Option | Purpose | Default |
|---|---|---|
| `--out FILE` | where to write the map | `PROJECT_MAP.md` |
| `--exclude a,b,c` | which directories to skip | `.git,node_modules,venv,.venv,__pycache__,dist,build,.next,target,.idea,.vscode,...` |
| `--ext .py,.ts` | which extensions to parse into signatures (everything else is included in the tree as-is) | `.py,.js,.jsx,.ts,.tsx` |
| `--max-bytes N` | files larger than N bytes are not parsed line-by-line and are marked as "large file" | `300000` |
| `--docstring-chars N` | how many docstring characters to keep (long descriptions are truncated) | `160` |
| `--stdout` | also print the map to the terminal (not only to the file) | off |

Example for a real project with a TypeScript frontend and Python backend:

```bash
python3 scripts/project_map.py . --out PROJECT_MAP.md \
    --ext .py,.ts,.tsx \
    --exclude .git,node_modules,dist,__pycache__,migrations
```

## What To Do After Running It

1. Check that `PROJECT_MAP.md` was created in the repository root (or wherever
   `--out` points).
2. Give the **entire `PROJECT_MAP.md` file** to the cloud planning agent as the
   primary structural context. There is no need to restate the structure in
   plain text separately; the file is already in the right format.
3. When the local model changes the code (new/removed functions, classes, or
   files), **rerun the same script with the same parameters** so that
   `PROJECT_MAP.md` is overwritten and reflects the current state. Do not edit
   the map by hand - it is always regenerated.
4. If the map becomes too large (hundreds of files), narrow the scope via
   `--ext` (for example, only `.py`) or generate maps for subfolders
   separately (`scripts/project_map.py backend/ --out backend_map.md`,
   `scripts/project_map.py frontend/ --out frontend_map.md`).

## What It Supports

- **Python (`.py`)** - precise parsing via `ast`: top-level imports, classes
  (base classes, docstring, annotated fields), methods and functions
  (decorators, annotated parameters with default values, return type, `async`,
  first-line/truncated docstring). The function body is always replaced with
  `...`.
- **JS/JSX/TS/TSX** - best-effort parsing via regular expressions with bracket
  nesting awareness: `function`, arrow functions in `const/let/var`, classes
  and their methods (`static`/`async`/`private`/... modifiers),
  `export`/`export default`. This is not a full AST parser, so very unusual
  syntax (TS decorators, generics with nested braces inside types, etc.) may be
  parsed imperfectly. In that case, the line may simply be omitted from the
  map; the file's presence in the tree is still preserved.
- **Other text files** - included in the tree with line count and size; content
  is not included.
- **Binary files** (images, fonts, archives, etc.) - included only in the
  tree, marked as `[binary file]`.

## Limitations (Important For The Planner)

- This is not a replacement for reading code - the map does not include
  function bodies, logic, conditions, or loops. It answers "what exists and
  where", not "how it works internally".
- The JS/TS parser is regex-based, not AST-based, so it does not guarantee
  100% accuracy for every syntax form (for example, nested template strings
  with braces inside `${...}` may confuse nesting depth in rare cases).
- For very large monorepos, generate the map in parts (see item 4 above) or
  narrow `--ext`; otherwise even signatures may consume too many tokens.
