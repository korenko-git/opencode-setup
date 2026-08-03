# Global Agent Instructions

## External File Loading

CRITICAL: When you encounter a file reference such as `@docs/architecture-rules.md`, use the Read tool to load it only when it is relevant to the current task.

Instructions:

- Do not preemptively load all referenced files.
- Use lazy loading based on the actual task.
- When a referenced file is loaded, treat its content as mandatory instructions for that task.
- Follow nested references recursively when needed.

## Always Applicable Rules

Read this file immediately because it applies to all tasks:

@rules/general-guidelines.md

## Task-Specific References

For architecture, module boundaries, utility reuse, file ownership, duplication control, and non-trivial feature design:

@docs/architecture-rules.md

## Subagent Delegation

Use subagents proactively when they match the task.

- For non-trivial code changes, delegate implementation to an `implementation` subagent.
- Before a multi-file refactor, use an `explore` subagent to identify affected modules and dependencies.
- For a code review request, use a `code-reviewer` subagent before responding.
- For a TDD refactor request, use a `tdd-orchestrator` subagent before responding.
- Before creating commits, use a `lightweight` subagent to propose logical commit groups and commit messages.
- Direct edits by the primary agent are allowed only for a trivial one-file change, or when delegation would add no value.
- The primary agent remains responsible for integration, verification, and user communication.

## Commit Workflow

Before creating commits:

1. Ask a `lightweight` subagent to propose the commit split and messages.
2. Inspect `git status`, `git diff`, `git diff --cached`, and `git log --oneline -10`.
3. Stage only files belonging to the selected commit group.
4. Follow the repository's commit-message style.
5. Do not amend or rewrite history unless the user explicitly requests it.
