---
description: "Remove unused code safely using local analysis, verification, and scoped edits"
argument-hint: "[file-path|directory|symbol|all]"
agent: build
---

# Remove Dead Code Safely

Analyze the current project for unused code and remove only high-confidence dead code.

## Scope

$ARGUMENTS

## Core Rules

1. Use only documented OpenCode capabilities and repo-local agents.
2. Never commit, push, or create git history unless the user explicitly asks.
3. Never use destructive rollback commands such as `git checkout --` or `git reset --hard`.
4. Never remove likely entry points, public API surfaces, or config by default.
5. Prefer a narrow, explainable cleanup over aggressive mass deletion.

## False Positive Guards

Treat these as live unless the user explicitly says otherwise:

- symbols exported from package entry points or barrel files,
- anything referenced by tests,
- command templates, skill definitions, agent files, and MCP/config files,
- symbols marked as public API with tags such as `@public` or `@api`,
- framework entry files such as `src/index.*`, `src/main.*`, `app/layout.*`, CLI entry points, and package export targets.

## Scope Control

Interpret `$ARGUMENTS` like this:

- file path -> inspect only that file,
- directory -> inspect only that directory,
- symbol name -> inspect only matching definitions and references,
- `all` or empty -> inspect the whole project conservatively.

## Workflow

### 1. Establish Project Context

Determine the language and validation commands that actually exist in the repo.

Examples:

- TypeScript: `bunx tsc --noEmit --noUnusedLocals --noUnusedParameters`
- JS/TS lint: project lint or typecheck command
- Python: linter, type checker, or test command if present

Do not invent commands that are not available in the repository.

### 2. Gather Candidates

Use repo-native evidence:

- `glob` to find likely source files,
- `grep` to find exports, imports, and symbol references,
- `read` to inspect files before making decisions,
- `bash` only for safe project analysis commands such as typecheck, lint, or tests.

If helpful, delegate read-only search to the built-in `explore` agent, but keep final decisions in the main flow.

### 3. Verify Each Candidate

For every candidate, verify all of the following before editing:

1. The symbol or file is not part of an entry point or public API.
2. It is not referenced by tests, docs examples, config, or exports.
3. Search results show no meaningful usages outside the declaration site.
4. The surrounding file structure confirms the removal is syntactically safe.

Use these action types:

- `REMOVE` -> delete an unused import, declaration, or dead file when confidence is high.
- `PREFIX _` -> rename an unused parameter to `_name` when the signature still matters.
- `SKIP` -> keep the candidate when confidence is not high enough.

If there are no high-confidence candidates, report `No dead code found` and stop.

### 4. Decide Whether To Edit Immediately

Proceed without another question only when all of these are true:

- scope is narrow or candidate count is small,
- confidence is high,
- changes are localized,
- validation is cheap.

Otherwise, present a candidate table first and ask the user which removals to apply.

### 5. Apply Changes Safely

When editing:

1. Work file by file.
2. Re-read the file before modifying it.
3. Clean up trailing commas, blank lines, and import lists.
4. Prefer minimal edits that keep behavior unchanged.
5. Do not touch unrelated user changes.

### 6. Validate After Edits

Run the closest available validation:

- typecheck for typed languages,
- targeted tests if relevant,
- build only if it is a normal lightweight project check.

If validation fails:

1. Stop immediately.
2. Report the failure clearly.
3. Do not auto-revert with destructive git commands.
4. Ask the user how to proceed.

## Output Format

Report results as:

```markdown
## Dead Code Review

### Removed
| # | Symbol/File | Action | Reason |
|---|-------------|--------|--------|

### Skipped
| # | Symbol/File | Reason |
|---|-------------|--------|

### Validation
- Typecheck: PASS/FAIL/NOT RUN
- Tests: PASS/FAIL/NOT RUN
- Build: PASS/FAIL/NOT RUN
```

## Abort Conditions

Stop and ask before editing if:

- more than 25 plausible candidates are found,
- the scope is ambiguous,
- the repo has dirty changes in the same files,
- validation commands are missing and safety cannot be established.
