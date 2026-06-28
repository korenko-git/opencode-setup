---
name: opencode-skills
description: Explain and author OpenCode skills. Invoke when creating SKILL.md files, choosing skill locations, writing frontmatter, configuring skill permissions, or troubleshooting skill discovery.
compatibility: opencode
---

# OpenCode Skills

Reference skill for OpenCode skill discovery, authoring, and permission control.

## When To Use

Use this skill when the task involves:

- creating a new OpenCode skill,
- deciding where a skill should live,
- writing valid `SKILL.md` frontmatter,
- splitting a skill into focused modules,
- controlling which skills agents may load,
- troubleshooting why a skill is not being discovered.

## Discovery Locations

OpenCode discovers skills from these locations:

- Project config: `.opencode/skills/<name>/SKILL.md`
- Global config: `~/.config/opencode/skills/<name>/SKILL.md`
- Project Claude-compatible: `.claude/skills/<name>/SKILL.md`
- Global Claude-compatible: `~/.claude/skills/<name>/SKILL.md`
- Project agent-compatible: `.agents/skills/<name>/SKILL.md`
- Global agent-compatible: `~/.agents/skills/<name>/SKILL.md`

For project-local paths, OpenCode walks up from the current directory to the git root and loads matching skill files it finds along the way.

## Required Structure

Each skill needs:

1. One folder per skill name.
2. A `SKILL.md` file inside that folder.

Example:

```text
.agents/
  skills/
    my-skill/
      SKILL.md
```

## Valid Frontmatter

Only these fields are recognized:

- `name` required
- `description` required
- `license` optional
- `compatibility` optional
- `metadata` optional string map

Example:

```markdown
---
name: my-skill
description: Explain a reusable workflow. Invoke when the user asks for that workflow or when the task clearly matches it.
compatibility: opencode
---
```

## Name Rules

The `name` must:

- be 1 to 64 characters,
- use lowercase letters and digits,
- use single hyphens as separators,
- not start or end with `-`,
- not contain consecutive `--`,
- match the directory name exactly.

Equivalent regex:

```text
^[a-z0-9]+(-[a-z0-9]+)*$
```

## Description Rules

The `description` should say:

1. what the skill does,
2. when to invoke it.

Keep it specific enough that the system can choose the skill correctly.

## Writing Good Skills

1. Put the core decision logic in `SKILL.md`.
2. Keep the top-level file concise and easy to route from.
3. If the domain is broad, add focused companion markdown files in the same directory.
4. Preserve one clear purpose per skill.
5. Prefer action-oriented sections such as:
   - when to use,
   - capability map,
   - workflow,
   - guardrails,
   - examples.

## Skill Permissions

Skills can be controlled in `opencode.json`:

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

Available behaviors:

- `allow`: load immediately
- `ask`: request approval
- `deny`: hide the skill from the agent

## Per-Agent Overrides

You can override skill permissions for built-in agents or custom agents.

Example:

```json
{
  "agent": {
    "plan": {
      "permission": {
        "skill": {
          "internal-*": "allow"
        }
      }
    }
  }
}
```

## Troubleshooting

If a skill does not appear:

1. Confirm the file is named `SKILL.md` in uppercase.
2. Confirm frontmatter includes `name` and `description`.
3. Confirm the directory name matches the skill `name`.
4. Confirm the name is unique across all loaded skill locations.
5. Confirm permissions do not hide it.

## Best Practices

1. Put evergreen knowledge into skills, not transient task output.
2. Keep skill names short and memorable.
3. Use one multi-file skill instead of many overlapping duplicates when the domain is broad.
4. Keep examples minimal but valid.
5. Prefer global skills for personal reusable knowledge and project-local skills for team workflows.
