# Global Agent Instructions

## Language

- Code comments and commit messages in English.
- User communication: match the user's language.

## Code Style

- Follow existing conventions in the project. When in doubt, read neighboring files.
- No comments unless explicitly asked.
- Prefer editing existing files over creating new ones.
- Use type hints (Python), explicit types (TS/Go/Rust).

## Git

- Never commit secrets, keys, or tokens.
- Run linter/typecheck before committing if available.
- Commit messages: imperative mood, lowercase, no period. Examples: `add user endpoint`, `fix null check in auth`.
- Do not commit unless explicitly asked.

## Behavioral

- Execute steps in order. Do not skip ahead.
- Halt on failure. Present the error and ask how to proceed.
- When using agents via Task tool — specify `subagent_type`, pass full context in prompt, never assume shared state.
- Prefer local agents only. No cross-plugin dependencies.

## Security

- Never log or expose secrets and environment variables.
- Use parameterized queries. Never interpolate user input into SQL.
- Validate all external input at API boundaries.
