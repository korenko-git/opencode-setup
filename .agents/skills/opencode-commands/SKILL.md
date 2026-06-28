---
name: opencode-commands
description: Explain OpenCode custom commands. Invoke when creating slash commands, choosing between command files and config, using arguments or file references, or overriding agent/model per command.
compatibility: opencode
---

# OpenCode Commands

Reference skill for custom slash commands in OpenCode.

## When To Use

Use this skill when the task involves:

- creating custom `/commands`,
- deciding between markdown command files and `opencode.json`,
- passing arguments into commands,
- injecting shell output or file content into command prompts,
- overriding `agent`, `model`, or `subtask` for a command,
- documenting repeatable workflows as slash commands.

## What Commands Are

Custom commands let you define reusable prompts that run from the TUI with a slash prefix:

```text
/my-command
```

They complement built-in commands such as `/init`, `/undo`, `/redo`, `/share`, and `/help`.

## Where Commands Live

You can define commands in either place:

- Global markdown files: `~/.config/opencode/commands/`
- Project markdown files: `.opencode/commands/`
- Config-based commands: `command` block in `opencode.json` or `opencode.jsonc`

## Markdown Command Example

Create `.opencode/commands/test.md`:

```markdown
---
description: Run tests with coverage
agent: build
model: anthropic/claude-3-5-sonnet-20241022
---

Run the full test suite with coverage report and show any failures.

Focus on the failing tests and suggest fixes.
```

The file name becomes the command name, so `test.md` maps to:

```text
/test
```

## JSON Command Example

```json
{
  "$schema": "https://opencode.ai/config.json",
  "command": {
    "test": {
      "template": "Run the full test suite with coverage report and show any failures.\nFocus on the failing tests and suggest fixes.",
      "description": "Run tests with coverage",
      "agent": "build",
      "model": "anthropic/claude-3-5-sonnet-20241022"
    }
  }
}
```

## Command Options

### Required

- `template` in JSON configuration

### Common Optional Fields

- `description`
- `agent`
- `subtask`
- `model`

## Arguments

Use `$ARGUMENTS` to capture the full argument string:

```markdown
---
description: Create a new component
---

Create a new React component named $ARGUMENTS with TypeScript support.
```

Run:

```text
/component Button
```

You can also use positional arguments:

- `$1`
- `$2`
- `$3`

Example:

```markdown
---
description: Create a file
---

Create a file named $1 in directory $2 with this content: $3
```

## Shell Output

Use `!` with backticks to include command output in the prompt:

```markdown
---
description: Review recent changes
---

Recent commits:

!`git log --oneline -10`

Review these changes and suggest improvements.
```

The shell command runs in the project root and its output becomes part of the prompt.

## File References

Use `@path/to/file` to include file content:

```markdown
---
description: Review a component
---

Review @src/components/Button.tsx for performance and maintainability.
```

## Agent And Subtask Behavior

- If `agent` is omitted, the current agent is used.
- If `agent` points to a subagent, the command triggers subagent behavior by default.
- Set `subtask: false` if you do not want that default subagent invocation behavior.
- Set `subtask: true` to force subagent-style execution even when the chosen agent is primary.

## Model Override

Set `model` on a command when one workflow benefits from a different model than your default session.

## Important Behavior

- Custom commands can override built-in commands if they share the same name.
- Prefer distinct names unless you intentionally want to replace a built-in.

## Best Practices

1. Use commands for repetitive prompts, not one-off tasks.
2. Keep each command focused on one workflow.
3. Use markdown files for discoverable local workflows and config for centralized shared setup.
4. Prefer arguments and file references over hardcoding file names into every command.
5. Be careful with shell interpolation so prompts stay deterministic and readable.
