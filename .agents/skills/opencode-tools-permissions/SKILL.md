---
name: opencode-tools-permissions
description: Explain OpenCode tools and approval controls. Invoke when choosing built-in tools, configuring tool permissions, allowing safe bash patterns, or limiting edits, web access, and skill loading.
compatibility: opencode
---

# OpenCode Tools And Permissions

Reference skill for built-in tools, approval behavior, and permission patterns in OpenCode.

## When To Use

Use this skill when the task involves:

- understanding which built-in tools exist,
- configuring tool permissions,
- making bash safer with approval patterns,
- restricting file edits or web access,
- deciding between `allow`, `ask`, and `deny`,
- mapping a workflow to the minimum required tool set.

## Built-In Tools

Common built-in tools include:

- `bash`
- `edit`
- `write`
- `read`
- `grep`
- `glob`
- `patch`
- `skill`
- `todowrite`
- `webfetch`
- `websearch`
- `question`

Some environments may also expose LSP or other integrations.

## Important Permission Notes

- By default, tools are generally enabled unless restricted.
- `write` is controlled by `edit` permission because both modify files.
- Permissions can be set globally or via more specific patterns.

## Top-Level Permission Example

```json
{
  "$schema": "https://opencode.ai/config.json",
  "permission": {
    "edit": "ask",
    "bash": "ask",
    "webfetch": "allow"
  }
}
```

## Tool Permission Semantics

- `allow`: run without approval
- `ask`: request approval first
- `deny`: disable the tool or command pattern

## Edit Permission

Use `permission.edit` to control file modifications.

```json
{
  "permission": {
    "edit": "ask"
  }
}
```

This applies to file modification operations, including write-like behavior.

## Bash Permission

Use `permission.bash` for command execution policy.

### Ask For All Commands

```json
{
  "permission": {
    "bash": "ask"
  }
}
```

### Allow Safe Commands, Ask For Sensitive Ones

```json
{
  "permission": {
    "bash": {
      "git status": "allow",
      "git diff": "allow",
      "npm run build": "allow",
      "git push": "ask",
      "*": "allow"
    }
  }
}
```

### Block Specific Families

```json
{
  "permission": {
    "bash": {
      "terraform *": "deny"
    }
  }
}
```

## Web Permissions

`webfetch` can be controlled explicitly when remote content access should be constrained:

```json
{
  "permission": {
    "webfetch": "ask"
  }
}
```

## Skill Permissions

Skill loading can also be permission-controlled:

```json
{
  "permission": {
    "skill": {
      "*": "allow",
      "internal-*": "deny",
      "experimental-*": "ask"
    }
  }
}
```

## Choosing A Permission Strategy

```text
Personal sandbox, low risk ───────────── mostly allow
Shared repo, normal development ─────── ask for edit and risky bash
Sensitive infra or production repo ──── deny dangerous patterns, ask for most writes
Review-only workflows ───────────────── disable edit and restrict bash
```

## Best Practices

1. Use explicit bash pattern rules for risky commands.
2. Default to safer approvals in shared or sensitive repos.
3. Restrict edit access for analysis-only agents.
4. Grant only the tools each custom agent actually needs.
5. Review wildcard rules carefully so they do not accidentally over-allow dangerous actions.
