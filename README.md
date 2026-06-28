# OpenCode Setup

Curated personal OpenCode setup stored in `~/.config/opencode`.

It contains:

- focused local agents for architecture, languages, data, UI, and TDD,
- explicit slash commands for recurring workflows,
- primary reusable skills in `skills/`,
- modular rule files in `rules/` and `docs/`,
- a separate OpenCode reference suite in `.agents/skills/` for authoring and maintaining OpenCode itself.

## Snapshot

- **26 local agents** in `agents/`
- **19 slash commands** in `commands/`
- **12 primary skills** in `skills/`
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
├── agents/                   # Local agent definitions
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

- All skills are allowed by default through `opencode.jsonc`.
- `improve-codebase-architecture` is explicitly denied in `opencode.jsonc`.
- `AGENTS.md` uses lazy loading for referenced instruction files instead of inlining every rule.
- User-facing communication should match the user's language, per `rules/general-guidelines.md`.
- The active rule path is intentionally minimal: always load `rules/general-guidelines.md`, and load `docs/architecture-rules.md` when the task needs architecture guidance.

## Local Agents

### Architecture, Platform, and Data

| Agent | Focus |
|------|-------|
| `architect-review` | Architecture review, clean architecture, DDD, microservices |
| `backend-architect` | Scalable backend services, APIs, distributed systems |
| `database-admin` | Cloud DB operations, HA/DR, automation, compliance |
| `database-architect` | Data modeling, DB selection, schema-first architecture |
| `database-optimizer` | Query tuning, indexing, caching, performance |
| `data-engineer` | Data pipelines, streaming, Spark, dbt, warehouse design |
| `deployment-engineer` | CI/CD, GitOps, deployment automation |
| `performance-engineer` | Observability, OpenTelemetry, load/perf optimization |
| `graphql-architect` | GraphQL schemas, federation, security, performance |
| `vector-database-engineer` | Semantic search, embeddings, vector DB systems |

### Languages and Frameworks

| Agent | Focus |
|------|-------|
| `bash-pro` | Defensive Bash scripting and automation |
| `cpp-pro` | Modern C++, RAII, templates, performance |
| `django-pro` | Django 5.x, DRF, Channels, Celery |
| `fastapi-pro` | Async APIs with FastAPI, SQLAlchemy 2.0, Pydantic V2 |
| `golang-pro` | Go 1.21+, concurrency, services, performance |
| `php-pro` | Modern PHP, SPL, generators, OOP |
| `python-pro` | Python 3.12+, async, performance, modern tooling |
| `rust-pro` | Rust async and systems programming |
| `sql-pro` | SQL design, query tuning, analytical workloads |
| `typescript-pro` | Advanced TypeScript and strict typing |

### Product, UX, AI, and Workflow

| Agent | Focus |
|------|-------|
| `design-system-architect` | Tokens, theming, component library design |
| `ui-designer` | UI implementation, layouts, visual design |
| `ai-engineer` | Production LLM apps, RAG systems, agent orchestration, multimodal AI |
| `prompt-engineer` | Prompt design, review, and optimization |
| `tdd-orchestrator` | Red-green-refactor workflow and TDD governance |

### Documentation

| Agent | Focus |
|------|-------|
| `api-documenter` | OpenAPI 3.1, SDK generation, interactive API docs, developer portals |

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
| `responsive-design` | Modern adaptive layout patterns and responsive UI guidance |
| `security-suite` | Unified security workflow from threat modeling to hardening |
| `seo-suite` | SEO optimization across structure, snippets, freshness, and authority |
| `tdd` | Test-driven development practices and reference materials |

### Notable Skill Suites

- `i18n` is the primary localization skill in this repository.
- `i18n` explicitly prefers domain-based message files such as `locales/en/common.json`.
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
