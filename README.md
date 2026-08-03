# OpenCode Setup

Curated personal OpenCode setup stored in `~/.config/opencode`.

It contains:

- three subagents for implementation, lightweight text-first work, and code review,
- explicit slash commands for recurring workflows,
- primary reusable skills in `skills/`,
- modular rule files in `rules/` and `docs/`,
- a separate OpenCode reference suite in `.agents/skills/` for authoring and maintaining OpenCode itself.

## Snapshot

- **3 subagents** across `agents/`
- **19 slash commands** in `commands/`
- **13 primary skills** in `skills/`
- **7 OpenCode reference skills** in `.agents/skills/`
- **Plugin version:** `@opencode-ai/plugin@1.17.7`

## Repository Layout

```text
~/.config/opencode/
├── AGENTS.md                 # Global instructions for agents working in this repo
├── README.md                 # This document
├── docs/                     # Task-specific rule files loaded on demand
├── opencode.jsonc            # Main OpenCode config
├── package.json              # Plugin dependency
├── rules/                    # Always-applicable shared guidelines
├── agents/                   # Agent definition files
├── commands/                 # Slash commands available in the TUI
├── skills/                   # Primary reusable skills
└── .agents/
    └── skills/               # OpenCode-specific reference skills
```

## Configuration

| File | Purpose |
|------|---------|
| `opencode.jsonc` | Main OpenCode config using schema `https://opencode.ai/config.json` |
| `AGENTS.md` | Router-style instruction entrypoint with lazy-loaded references |
| `rules/general-guidelines.md` | Always-applicable execution, code style, git, and security rules |
| `docs/architecture-rules.md` | Architecture, reuse, module ownership, and anti-duplication guardrails |
| `package.json` | Pins `@opencode-ai/plugin` to `1.17.7` |

### Current Config Notes

- `small_model` is set to `openai/gpt-5.6-luna` for cheaper helper and background tasks.
- The built-in `plan` agent uses `openai/gpt-5.6-sol` and is permission-scoped to the `project-map` skill plus the `explore` subagent only.
- The built-in `build` agent uses `openai/gpt-5.6-terra`, allows subagent tasks, and only exposes the `project-map` skill.
- The configured `code-reviewer` subagent is read-only, runs on `openai/gpt-5.6-sol`, and focuses on security, performance, and maintainability reviews.
- The `implementation` subagent is the execution-side coding agent for real repository changes and verification.
- The `lightweight` subagent uses `openai/gpt-5.6-luna` for low-cost text-first tasks such as commit messages, short summaries, and small rewrites.
- `AGENTS.md` uses lazy loading for referenced instruction files instead of inlining every rule.
- User-facing communication should match the user's language, per `rules/general-guidelines.md`.
- The active rule path is intentionally minimal: always load `rules/general-guidelines.md`, and load `docs/architecture-rules.md` when the task needs architecture guidance.

## Configured Agents

| Agent | Focus |
|------|-------|
| `implementation` | Execution subagent that inspects the real repository, implements source changes, runs verification, and reports the result |
| `lightweight` | Lightweight text-first helper on `openai/gpt-5.6-luna` for commit messages, short summaries, compact rewrites, and similar low-cost tasks |
| `code-reviewer` | Read-only review subagent focused on security, performance, and maintainability |

## Slash Commands

### UI and Product

| Command | Purpose |
|--------|---------|
| `/accessibility-audit` | Audit UI code for WCAG compliance |
| `/add-analytics` | Apply the analytics integration guide for Plausible, GTM, and Yandex.Metrika |
| `/add-google-auth` | Apply the Google OAuth + JWT authentication guide |
| `/design-review` | Review existing UI for design and usability issues |
| `/design-system-setup` | Initialize design tokens and design-system scaffolding |
| `/add-limits-and-credits` | Apply the ledger-based billing and credits guide |

### Code, Docs, and Architecture

| Command | Purpose |
|--------|---------|
| `/code-explain` | Explain complex code with structured breakdowns |
| `/code-migrate` | Generate migration plans between stacks or versions |
| `/doc-generate` | Generate project documentation |
| `/prompt-optimize` | Improve prompts for production use |
| `/refactor-clean` | Refactor for maintainability and cleaner design |
| `/remove-deadcode` | Safely remove unused code with local verification |
| `/tech-debt` | Analyze debt and propose remediation |

### Testing and TDD

| Command | Purpose |
|--------|---------|
| `/tdd-cycle` | Full red-green-refactor workflow |
| `/tdd-red` | Generate failing tests |
| `/tdd-green` | Implement the minimal passing code |
| `/tdd-refactor` | Refactor safely with test coverage as a safety net |
| `/test-generate` | Generate targeted automated tests |

### OpenCode Maintenance

| Command | Purpose |
|--------|---------|
| `/update-opencode-skills` | Refresh local OpenCode reference skills against current docs |

## Primary Skills

These are the main reusable skills under `skills/`.

| Skill | Purpose |
|------|---------|
| `accessibility-compliance` | Implement WCAG 2.2 compliant interfaces with mobile accessibility, inclusive design patterns, and assistive technology support. |
| `codebase-design` | Shared vocabulary for designing deeper, more coherent modules |
| `commit-message` | Commit message generation helpers and analysis tooling |
| `domain-modeling` | Domain language, ADRs, and model refinement |
| `find-skills` | Discover relevant installable skills for a task |
| `i18n` | Unified localization architecture, audits, and SEO-aware translation workflow |
| `improve-codebase-architecture` | Deepening scan with HTML report output |
| `payments-integration` | Stripe, PayPal, LemonSqueezy, and YooKassa integration patterns |
| `project-map` | Generates compact codebase maps for planner-driven workflows using signatures without implementation bodies |
| `responsive-design` | Modern adaptive layout patterns and responsive UI guidance |
| `security-suite` | Unified security workflow from threat modeling to hardening |
| `seo-suite` | SEO optimization across structure, snippets, freshness, and authority |
| `tdd` | Test-driven development practices and reference materials |

### Notable Skill Suites

- `i18n` is the primary localization skill in this repository.
- `i18n` explicitly prefers domain-based message files such as `locales/en/common.json`.
- `project-map` includes a real helper script in `skills/project-map/project_map.py` for regenerating maps instead of editing them manually.
- `security-suite`, `seo-suite`, and `payments-integration` are multi-file suites with reference modules.
- `commit-message` and `i18n` both include helper scripts inside the skill directory.

## OpenCode Reference Skills

These live under `.agents/skills/` and document how to work with OpenCode itself.

| Skill | Purpose |
|------|---------|
| `opencode-agents` | Agent creation, modes, tools, and configuration |
| `opencode-commands` | Slash command authoring and command metadata |
| `opencode-config` | `opencode.json/jsonc` structure and precedence |
| `opencode-models` | Model/provider selection and troubleshooting |
| `opencode-rules` | `AGENTS.md`, instructions, and rule precedence |
| `opencode-skills` | Skill authoring, discovery, and permissions |
| `opencode-tools-permissions` | Tool access, approvals, and permission patterns |

## Current Project Conventions

- `analytics`, `auth`, and `limits-and-credits` are now maintained as **commands**, not primary skills.
- The repository uses `~/.config/opencode` as the canonical location, not `.opencode/`.
- Markdown command files are the main way recurring workflows are exposed to the TUI.
- OpenCode-specific authoring guidance is intentionally separated into `.agents/skills/` so it does not mix with product/domain skills.
- `AGENTS.md` is intentionally short and acts as a router to deeper guidance in `rules/` and `docs/`.
- For non-trivial feature work, the preferred thinking model is module boundaries and domain ownership, using the design vocabulary from `skills/codebase-design` and `skills/domain-modeling`.
- Architecture rules explicitly discourage one-file features, local utility duplication, and mixed-responsibility catch-all files.

## Maintenance Checklist

- Update `README.md` when agent, command, or skill counts change materially.
- Update `README.md` when the rule system in `AGENTS.md`, `rules/`, or `docs/` changes materially.
- Prefer editing existing commands and skills over introducing duplicates.
- Keep `skills/<name>/SKILL.md` compliant with OpenCode discovery rules.
- Re-check command and skill diagnostics after substantive markdown edits.
