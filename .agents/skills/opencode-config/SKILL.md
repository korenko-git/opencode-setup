---
name: opencode-config
description: Explain OpenCode configuration files and schema. Invoke when editing opencode.json/jsonc, choosing config precedence, setting models, providers, keybinds, instructions, or project-vs-global config.
compatibility: opencode
---

# OpenCode Config

Reference skill for `opencode.json` and `opencode.jsonc` structure, precedence, and common configuration patterns.

## When To Use

Use this skill when the task involves:

- creating or editing `opencode.json`,
- understanding config precedence,
- choosing global vs project config,
- setting models, providers, keybinds, or autoupdate,
- wiring `instructions`, `agent`, or `permission` blocks,
- using a custom config path.

## Supported Formats

OpenCode supports:

- `opencode.json`
- `opencode.jsonc`

Use JSONC when comments help maintainability.

## Config Locations And Precedence

OpenCode can read configuration from:

1. Global config: `~/.config/opencode/opencode.json`
2. Project config: `./opencode.json`
3. Custom path from `OPENCODE_CONFIG`

Recommended usage:

- global config for personal defaults such as themes, providers, and keybinds,
- project config for repository-specific models, agents, permissions, or instructions,
- `OPENCODE_CONFIG` for one-off or scripted overrides.

## Minimal Example

```json
{
  "$schema": "https://opencode.ai/config.json",
  "model": "anthropic/claude-sonnet-4-20250514",
  "autoupdate": true
}
```

## Common Top-Level Areas

- `provider`
- `model`
- `small_model`
- `theme`
- `agent`
- `permission`
- `instructions`
- `keybinds`
- `autoupdate`
- `formatter`
- `mcp`

## Models

Use `provider/model` identifiers.

Example:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "model": "anthropic/claude-sonnet-4-20250514",
  "small_model": "anthropic/claude-3-5-haiku-20241022"
}
```

Use `small_model` for lightweight tasks such as titles or other cheaper helper work when available.

## Instructions

Use `instructions` to load reusable rule files without duplicating them into `AGENTS.md`.

Example:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "instructions": [
    "docs/guidelines.md",
    ".cursor/rules/*.md",
    "https://raw.githubusercontent.com/my-org/shared-rules/main/style.md"
  ]
}
```

## Agents In Config

Use the `agent` block to override built-in agents or define custom ones.

```json
{
  "$schema": "https://opencode.ai/config.json",
  "agent": {
    "plan": {
      "tools": {
        "edit": false,
        "bash": false
      }
    }
  }
}
```

## Permissions In Config

Use the `permission` block to control sensitive operations and skill loading.

```json
{
  "$schema": "https://opencode.ai/config.json",
  "permission": {
    "edit": "ask",
    "bash": {
      "git push": "ask",
      "*": "allow"
    },
    "skill": {
      "experimental-*": "ask"
    }
  }
}
```

## Custom Config Path

Use `OPENCODE_CONFIG` to point to an alternate config file:

```bash
export OPENCODE_CONFIG=/path/to/custom-opencode.json
opencode run "hello"
```

## Best Practices

1. Keep global config personal and project config team-relevant.
2. Put reusable standards into `instructions` instead of duplicating them.
3. Keep permissions explicit in shared repos.
4. Use schema-backed files so the editor can validate them.
5. Prefer small targeted agent and permission overrides over large blanket changes.
