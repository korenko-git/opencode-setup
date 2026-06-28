---
name: opencode-rules
description: Explain OpenCode rules and AGENTS.md behavior. Invoke when setting project instructions, using /init, choosing AGENTS.md locations, configuring instructions files, or understanding rule precedence.
compatibility: opencode
---

# OpenCode Rules

Reference skill for `AGENTS.md`, rule precedence, and reusable instruction loading in OpenCode.

## When To Use

Use this skill when the task involves:

- creating or improving `AGENTS.md`,
- running or reasoning about `/init`,
- deciding between project and global rules,
- configuring shared instructions through `opencode.json`,
- understanding `AGENTS.md` vs `CLAUDE.md` precedence,
- teaching OpenCode to load extra instruction files.

## What Rules Are

OpenCode uses `AGENTS.md` to inject custom project or personal instructions into the model context.
These rules are similar to Cursor-style project instructions.

## Creating Rules

The easiest way to initialize rules is:

```text
/init
```

`/init` scans the repo, asks targeted questions when needed, and creates or improves `AGENTS.md`.

## Rule Locations

### Project Rules

- Put `AGENTS.md` in the project root.
- These rules apply when working in that directory or its subdirectories.

### Global Rules

- Put `AGENTS.md` in `~/.config/opencode/AGENTS.md`.
- These rules apply across all OpenCode sessions.

## Claude Compatibility

OpenCode supports Claude-compatible fallbacks:

- project fallback: `CLAUDE.md`
- global fallback: `~/.claude/CLAUDE.md`
- skills fallback: `~/.claude/skills/`

These are used only when the OpenCode-native equivalent is absent, unless explicitly disabled.

## Precedence

OpenCode resolves rule files in this order:

1. Local project files by traversing upward: `AGENTS.md`, then `CLAUDE.md`
2. Global OpenCode file: `~/.config/opencode/AGENTS.md`
3. Global Claude fallback: `~/.claude/CLAUDE.md`

The first matching file wins in each category.

## Extra Instructions Via Config

Use `instructions` in `opencode.json` to load reusable external files:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "instructions": [
    "CONTRIBUTING.md",
    "docs/guidelines.md",
    ".cursor/rules/*.md"
  ]
}
```

Remote URLs are also supported:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "instructions": [
    "https://raw.githubusercontent.com/my-org/shared-rules/main/style.md"
  ]
}
```

## Manual External File Loading

If you want `AGENTS.md` to point to other files, teach the agent how to load them explicitly.

Useful pattern:

1. State that referenced files should be loaded lazily with the read tool.
2. Explain whether those files are always relevant or only task-specific.
3. Keep `AGENTS.md` concise and move deeper policies into referenced documents.

## What `/init` Is Good At

`/init` is especially useful for capturing:

- build, lint, and test commands,
- repo structure that is not obvious from filenames,
- project conventions,
- setup quirks and operational gotchas,
- references to other rule systems already present in the repo.

## Best Practices

1. Keep project rules committed to git.
2. Put personal preferences in global `AGENTS.md`, not in shared repo files.
3. Use `instructions` for modular standards instead of copying long documents into one file.
4. Keep rule files concise, specific, and enforceable.
5. Prefer lazy-loading references over preloading every possible document.
