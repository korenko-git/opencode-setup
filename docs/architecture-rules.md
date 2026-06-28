# Architecture Rules

## Core Goal

Optimize for coherent module boundaries, reuse, and long-term maintainability rather than the shortest local edit.

## Design Vocabulary

- For non-trivial feature work, think in terms of module boundaries and domain ownership, not just task completion.
- Prefer the repository's design vocabulary from `skills/codebase-design` and `skills/domain-modeling` when shaping new code.
- Use `codebase-design` for interface depth, seams, module boundaries, and extraction decisions.
- Use `domain-modeling` when naming concepts, defining ownership, or shaping shared domain language.

## Guardrails

- Do not put an entire feature into one large file by default.
- Do not keep adding code to a file that already mixes UI, business logic, data access, and formatting.
- Prefer focused modules with one clear responsibility.
- Keep business logic out of UI components when possible.
- Keep reusable logic out of route handlers, page files, and feature entrypoints when possible.

## Reuse Before Create

- Before creating a new utility, helper, hook, type, service, or formatter, search for an existing one and reuse it if possible.
- If similar logic already exists, extend or consolidate it instead of creating a local duplicate.
- If new logic is used in two or more places, extract it unless it is clearly feature-private.
- Do not create slightly renamed duplicates of existing helpers without a clear boundary reason.

## File Ownership

Prefer this split when applicable:

- UI and rendering
- domain or business logic
- data access or API clients
- shared types and schemas
- reusable utilities

When the task is non-trivial, decide which file owns each responsibility before editing.

## Feature Planning

Before implementing a non-trivial feature or refactor:

1. identify existing modules that can be reused,
2. identify any missing module boundaries,
3. decide which files should own UI, domain logic, integration logic, and shared utilities,
4. avoid starting implementation until this split is clear.

## Duplication Smells

Treat these as architectural warnings:

- copying helper logic into a component or handler,
- creating feature-local utilities that are actually generic,
- adding more branches to a catch-all file instead of extracting modules,
- redefining types close to usage when a shared type already exists,
- placing cross-feature behavior into page or component files.

## Refactoring Direction

If a file becomes a catch-all, prefer extracting:

- `types` or schemas first,
- pure utilities second,
- domain logic or service functions third,
- UI wrappers last.

Make incremental extractions instead of rewriting everything at once.
