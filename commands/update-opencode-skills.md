---
description: "Update local OpenCode skills from current docs and preserve local conventions"
agent: build
argument-hint: "[scope-or-notes]"
---

# Update OpenCode Skills

Update the local OpenCode-focused skills stored under `~/.config/opencode/.agents/skills/`.

## Scope

$ARGUMENTS

## Instructions

1. Treat `~/.config/opencode/.agents/skills/opencode-*/SKILL.md` as the primary target set.
2. If the user passed a scope in `$ARGUMENTS`, update only the matching skill or topic area.
3. Compare the current skill content against the latest relevant OpenCode documentation before editing.
4. Preserve local conventions and prior project decisions unless the docs clearly require a change.
5. Keep every skill compliant with OpenCode skill rules:
   - directory name matches `name`,
   - valid YAML frontmatter,
   - `description` explains what the skill does and when to invoke it,
   - content stays concise and actionable.
6. Prefer editing existing skills over creating duplicates.
7. If a topic is now missing and is clearly relevant to the local OpenCode suite, add it only if needed.
8. After edits, validate the changed `SKILL.md` files for diagnostics or formatting problems.

## Expected Workflow

1. List the current local OpenCode skills in `~/.config/opencode/.agents/skills/`.
2. Read the affected `SKILL.md` files.
3. Fetch only the relevant OpenCode docs pages for the requested scope.
4. Update the skill text with current behavior, commands, paths, and config examples.
5. Re-check diagnostics on edited files.
6. Report what changed, what was preserved, and any remaining gaps.

## Default Scope Map

- `agents` -> `opencode-agents`
- `skills` -> `opencode-skills`
- `config` -> `opencode-config`
- `tools` or `permissions` -> `opencode-tools-permissions`
- `rules` -> `opencode-rules`
- `commands` -> `opencode-commands`
- `models` or `providers` -> `opencode-models`

## Notes

- Prefer official OpenCode docs over stale examples.
- Do not rewrite unrelated user-created skills outside the OpenCode suite unless explicitly asked.
- If docs conflict with local conventions, keep the local convention and call out the mismatch in the summary.
