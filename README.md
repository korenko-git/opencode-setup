<!-- prettier-ignore -->
<div align="center">

# OpenCode Setup

[Snapshot](#snapshot) • [Configuration](#configuration) • [Agents](#agents) • [Slash Commands](#slash-commands) • [Primary Skills](#primary-skills) • [OpenCode Reference](#opencode-reference)

</div>

A curated [OpenCode](https://opencode.ai) configuration focused on high-quality software engineering workflows. It includes reusable subagents, production-ready slash commands, and modular skills for architecture, TDD, security, documentation, UI development, and project maintenance.

## Snapshot
 
| Category | Count | Location |
| --- | --- | --- |
| Subagents | 4 | `agents/` |
| Slash commands | 19 | `commands/` |
| Primary skills | 14 | `skills/` |
| OpenCode reference skills | 7 | `.agents/skills/` |

## Configuration

| File | Purpose |
| --- | --- |
| `opencode.jsonc` | Main OpenCode config using the official config schema |
| `AGENTS.md` | Global instruction router |
| `rules/general-guidelines.md` | Always-loaded execution, style, git, and security rules |
| `docs/architecture-rules.md` | On-demand architecture and reuse rules |

> [!TIP]
> If you run OpenCode from WSL, set your own LM Studio host IP in `opencode.jsonc` instead of `localhost`. WSL usually needs the machine IP available inside your local network.

## Agents

The repository defines three subagents:

| Agent | Purpose |
| --- | --- |
| `implementation` | Makes source changes, inspects the real repository, runs relevant verification, and reports the result |
| `lightweight` | Handles low-cost text-first tasks such as summaries, rewrites, and commit-related text |
| `code-reviewer` | Read-only review agent focused on security, performance, and maintainability |
| `tdd-orchestrator` | Orchestrator for TDD refactor phase |

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

## Primary Skills

Reusable skills under skills/, applicable across projects:

| Skill | Purpose |
|------|---------|
| `accessibility-compliance` | Implement WCAG 2.2 compliant interfaces with mobile accessibility, inclusive design patterns, and assistive technology support. |
| `codebase-design` | Shared vocabulary for designing deeper, more coherent modules |
| `commit-message` | Commit message generation helpers and analysis tooling |
| `create-readme` | Create a README.md file for the project |
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

## OpenCode Reference 

Documentation and skills for working with OpenCode itself, kept separate from the primary, project-facing skills above.

### Skills (`.agents/skills/`)

| Skill | Purpose |
|------|---------|
| `opencode-agents` | Agent creation, modes, tools, and configuration |
| `opencode-commands` | Slash command authoring and command metadata |
| `opencode-config` | `opencode.json/jsonc` structure and precedence |
| `opencode-models` | Model/provider selection and troubleshooting |
| `opencode-rules` | `AGENTS.md`, instructions, and rule precedence |
| `opencode-skills` | Skill authoring, discovery, and permissions |
| `opencode-tools-permissions` | Tool access, approvals, and permission patterns |

### Maintenance

| Command | Purpose |
|--------|---------|
| `/update-opencode-skills` | Refresh local OpenCode reference skills against current docs |

## Related Projects

- [skills.sh](https://www.skills.sh/) - directory of installable skills for coding agents
- [mattpocock/skills](https://github.com/mattpocock/skills) - curated skills for agent workflows
- [wshobson/agents](https://github.com/wshobson/agents) - reference collection of agent definitions
- [sickn33/agentic-awesome-skills](https://github.com/sickn33/agentic-awesome-skills) - community collection of agentic skills
