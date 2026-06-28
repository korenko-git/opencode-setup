# General Guidelines

## Language

- Code comments and commit messages in English.
- User communication must match the user's language.

## Execution

- Execute steps in order. Do not skip ahead.
- Halt on failure. Present the error and ask how to proceed.
- Prefer local agents only. Do not rely on cross-plugin dependencies.
- When using agents via Task tool, always specify `subagent_type`, pass full context in the prompt, and never assume shared state.

## Code Style

- Follow existing conventions in the project. When in doubt, read neighboring files first.
- Prefer editing existing files over creating new ones.
- Do not add comments unless they are explicitly requested or genuinely necessary.
- Use type hints in Python and explicit types in TypeScript, Go, and Rust.

## Git

- Never commit secrets, keys, or tokens.
- Run lint, typecheck, or equivalent validation before committing when available.
- Commit messages must use imperative mood, lowercase, and no trailing period.
- Do not commit unless explicitly asked.
- Do not use destructive git operations unless explicitly asked.

## Security

- Never log or expose secrets or environment variables.
- Use parameterized queries. Never interpolate user input into SQL.
- Validate all external input at API boundaries.
