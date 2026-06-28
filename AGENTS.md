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
