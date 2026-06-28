---
name: opencode-agents
description: Explain and configure OpenCode agents. Invoke when creating agents, choosing between Build/Plan/General/Explore, or setting agent tools, permissions, prompts, and modes.
compatibility: opencode
---

# OpenCode Agents

Reference skill for OpenCode agent types, built-in agents, and custom agent configuration.

## When To Use

Use this skill when the task involves:

- creating or editing OpenCode agents,
- choosing the right built-in agent for a task,
- configuring agent `mode`, `prompt`, `model`, `tools`, or `permission`,
- understanding primary vs subagent behavior,
- deciding whether a workflow should use Build, Plan, General, or Explore.

## Agent Types

OpenCode supports two agent types:

1. `primary`
   - The main assistant you interact with directly.
   - Built-in examples: `build`, `plan`.
2. `subagent`
   - Specialized assistants invoked by a primary agent or by `@mention`.
   - Built-in examples: `general`, `explore`.

## Built-In Agents

### `build`

- Default primary agent.
- Full tool access.
- Best for implementation work and direct edits.

### `plan`

- Restricted primary agent for planning and analysis.
- Commonly configured so file edits and bash require approval or are disabled.
- Best when the user wants a plan without modifications.

### `general`

- General-purpose subagent for multi-step work.
- Can make changes when allowed.
- Good for deeper research or delegated tasks.

### `explore`

- Read-only exploration subagent.
- Good for searching the codebase and answering structural questions quickly.

## Choosing An Agent

```text
Need to edit files or run commands now? ─────────── use Build
Need analysis or a plan without changes? ───────── use Plan
Need delegated multi-step implementation? ──────── use General
Need fast read-only codebase exploration? ──────── use Explore
```

## JSON Configuration Shape

Use `opencode.json` for built-in agent overrides or custom agents:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "agent": {
    "plan": {
      "mode": "primary",
      "tools": {
        "edit": false,
        "bash": false
      }
    },
    "docs-helper": {
      "description": "Documentation-focused subagent",
      "mode": "subagent",
      "model": "anthropic/claude-sonnet-4-20250514",
      "prompt": "Write concise docs and examples"
    }
  }
}
```

## Common Agent Fields

- `description`: short explanation of the agent purpose.
- `mode`: `primary` or `subagent`.
- `model`: model identifier such as `provider/model`.
- `prompt`: the agent's custom instructions.
- `tools`: enable, disable, or scope tool access.
- `permission`: override approval behavior for tools and skills.

## Tools And Permissions

- `tools: true` is equivalent to allowing all tools.
- `tools: false` disables all tools.
- Per-tool booleans can narrow the set.
- `permission` gives finer control than simple enable or disable flags.

Example:

```json
{
  "agent": {
    "reviewer": {
      "mode": "subagent",
      "tools": {
        "edit": false,
        "bash": false,
        "read": true
      },
      "permission": {
        "skill": {
          "documents-*": "allow"
        }
      }
    }
  }
}
```

## Markdown Frontmatter Agents

Custom agents can also be defined in markdown-based formats when supported by the surrounding toolchain.
When in doubt, prefer `opencode.json` for centralized configuration.

## Best Practices

1. Keep one clear purpose per custom agent.
2. Use `plan`-style restrictions for analysis-only workflows.
3. Use subagents for focused delegation, not for every trivial step.
4. Pair custom prompts with tight tool and permission scopes.
5. Keep descriptions specific so the system can choose the right agent.
