# OpenCode Configuration

Personal OpenCode AI setup with custom agents, commands, and skills.

## Structure

```
.opencode/
├── opencode.jsonc          # OpenCode configuration
├── AGENTS.md               # Agent instructions (minimal)
├── package.json            # Plugin dependency
├── agents/                 # Custom agent definitions
├── commands/               # Slash commands
├── skills/                 # Reusable skill modules
└── node_modules/           # Dependencies
```

**Totals**: 63 agents (61 custom + 2 built-in) · 35 commands · 102 skills

---

## Python

| Type | Name | Description |
|------|------|-------------|
| Agent | `python-pro` | Master Python 3.12+ with modern features, async programming, performance optimization, and production-ready practices |
| Agent | `fastapi-pro` | Build high-performance async APIs with FastAPI, SQLAlchemy 2.0, and Pydantic V2 |
| Command | `/python-scaffold` | Python project scaffolding (FastAPI/Django/lib/CLI) |
| Command | `/refactor-clean` | Refactoring with SOLID principles and clean code |
| Skill | `async-python-patterns` | Python asyncio, concurrent programming, and async/await patterns |
| Skill | `fastapi-design` | FastAPI patterns and best practices |
| Skill | `pydantic` | Pydantic models and validation |
| Skill | `python-anti-patterns` | Common Python anti-patterns to avoid |
| Skill | `python-background-jobs` | Task queues, workers, and event-driven architecture |
| Skill | `python-code-style` | Linting, formatting, naming conventions, doc standards |
| Skill | `python-configuration` | Environment variables and typed settings |
| Skill | `python-design-patterns` | KISS, Separation of Concerns, composition over inheritance |
| Skill | `python-error-handling` | Input validation, exception hierarchies, partial failure handling |
| Skill | `python-observability` | Structured logging, metrics, distributed tracing |
| Skill | `python-packaging` | Distributable packages, pyproject.toml, PyPI publishing |
| Skill | `python-performance-optimization` | cProfile, memory profilers, performance best practices |
| Skill | `python-project-structure` | Module architecture, public API design |
| Skill | `python-resilience` | Retries, exponential backoff, timeouts, fault-tolerant decorators |
| Skill | `python-resource-management` | Context managers, cleanup patterns, streaming |
| Skill | `python-testing-patterns` | pytest, fixtures, mocking, TDD |
| Skill | `python-type-safety` | Type hints, generics, protocols, mypy/pyright |
| Skill | `ruff-linter` | Ruff linter configuration and usage |
| Skill | `uv-package-manager` | uv for fast Python dependency management and virtual environments |

## JavaScript & TypeScript

| Type | Name | Description |
|------|------|-------------|
| Agent | `javascript-pro` | Master modern JavaScript with ES6+, async patterns, and Node.js APIs |
| Agent | `typescript-pro` | Master TypeScript with advanced types, generics, and strict type safety |
| Skill | `modern-javascript-patterns` | ES6+ features, async/await, destructuring, modules, functional programming |
| Skill | `typescript-advanced-types` | Generics, conditional types, mapped types, template literals, utility types |
| Skill | `javascript-testing-patterns` | Jest, Vitest, Testing Library — unit, integration, e2e testing |

## Go & Rust

| Type | Name | Description |
|------|------|-------------|
| Agent | `golang-pro` | Master Go 1.21+ with modern patterns, advanced concurrency, generics, workspaces |
| Agent | `rust-pro` | Master Rust 1.75+ with Tokio, axum, async patterns, production-ready systems programming |
| Command | `/rust-project` | Rust project scaffolding with Cargo |
| Skill | `go-concurrency-patterns` | Goroutines, channels, sync primitives, context |
| Skill | `rust-async-patterns` | Tokio, async traits, error handling, concurrent patterns |
| Skill | `memory-safety-patterns` | RAII, ownership, smart pointers across Rust, C++, C |

## Other Languages

| Type | Name | Description |
|------|------|-------------|
| Agent | `bash-pro` | Defensive Bash scripting for production automation, CI/CD, system utilities |
| Agent | `c-pro` | Efficient C code with memory management, pointer arithmetic, system calls |
| Agent | `cpp-pro` | Idiomatic C++ with RAII, smart pointers, STL algorithms, move semantics |
| Agent | `elixir-pro` | Idiomatic Elixir with OTP patterns, supervision trees, Phoenix LiveView |
| Agent | `haskell-pro` | Advanced type systems, pure functional design, high-reliability software |
| Agent | `php-pro` | Idiomatic PHP with generators, iterators, SPL data structures, modern OOP |
| Agent | `posix-shell-pro` | Strict POSIX sh scripting for maximum portability |
| Agent | `ruby-pro` | Idiomatic Ruby with metaprogramming, Rails patterns, performance optimization |
| Skill | `bash-defensive-patterns` | Defensive Bash for production-grade scripts |
| Skill | `bats-testing-patterns` | Bash Automated Testing System for shell script testing |
| Skill | `shellcheck-configuration` | ShellCheck static analysis for shell script quality |

## Web Frameworks

| Type | Name | Description |
|------|------|-------------|
| Agent | `frontend-developer` | React components, responsive layouts, client-side state management |
| Agent | `mobile-developer` | React Native, Flutter, or native mobile apps with modern architecture |
| Agent | `django-pro` | Django 5.x with async views, DRF, Celery, Django Channels |
| Command | `/component-scaffold` | React/React Native component scaffolding |
| Command | `/create-component` | Guided component creation with proper patterns |
| Command | `/typescript-scaffold` | TypeScript project scaffolding (pnpm, Vite, Next.js) |
| Skill | `angular-migration` | AngularJS to Angular migration with hybrid mode |
| Skill | `nextjs-app-router-patterns` | Next.js 14+ App Router, Server Components, streaming |
| Skill | `nodejs-backend-patterns` | Express/Fastify middleware, error handling, auth, API design |
| Skill | `react-modernization` | Upgrade React, migrate class components to hooks, concurrent features |
| Skill | `react-native-architecture` | Expo, navigation, native modules, offline sync |
| Skill | `react-native-design` | Styling, navigation, Reanimated animations |
| Skill | `react-state-management` | Redux Toolkit, Zustand, Jotai, React Query |
| Skill | `web-component-design` | React, Vue, Svelte component patterns, CSS-in-JS |

## Backend & Architecture

| Type | Name | Description |
|------|------|-------------|
| Agent | `architect-review` | Clean architecture, microservices, event-driven systems, DDD |
| Agent | `backend-architect` | Scalable API design, microservices, distributed systems |
| Agent | `backend-security-coder` | Input validation, authentication, API security |
| Agent | `event-sourcing-architect` | Event sourcing, CQRS, saga orchestration, eventual consistency |
| Agent | `graphql-architect` | GraphQL federation, performance optimization, enterprise security |
| Agent | `legacy-modernizer` | Refactor legacy codebases, migrate outdated frameworks |
| Agent | `temporal-python-pro` | Temporal workflow orchestration, saga patterns, distributed transactions |
| Command | `/feature-development` | End-to-end feature dev from requirements to deployment |
| Command | `/full-stack-feature` | Full-stack feature across backend, frontend, DB, infra |
| Command | `/code-migrate` | Migration plans between frameworks/languages |
| Command | `/legacy-modernize` | Legacy system modernization (strangler fig pattern) |
| Command | `/tech-debt` | Technical debt analysis and remediation |
| Skill | `api-design` | REST/OpenAPI conventions, versioning, response structure |
| Skill | `api-design-principles` | REST and GraphQL API design principles |
| Skill | `architecture-decision-records` | ADR documentation following best practices |
| Skill | `architecture-patterns` | Clean Architecture, Hexagonal, Domain-Driven Design |
| Skill | `auth` | Google OAuth, JWT, user tables, FastAPI dependencies, React auth state |
| Skill | `cqrs-implementation` | Command Query Responsibility Segregation |
| Skill | `microservices-patterns` | Service boundaries, event-driven communication, resilience |
| Skill | `openapi-spec-generation` | OpenAPI 3.1 specs from code or design-first |
| Skill | `workflow-orchestration-patterns` | Temporal durable workflows, saga patterns, determinism |

## Frontend & Mobile

| Type | Name | Description |
|------|------|-------------|
| Agent | `accessibility-expert` | WCAG compliance, inclusive design, assistive technology |
| Agent | `design-system-architect` | Design tokens, component libraries, theming infrastructure |
| Agent | `ui-designer` | Component creation, layout systems, visual design implementation |
| Command | `/design-system-setup` | Initialize design system with tokens |
| Command | `/design-review` | Review existing UI for issues and improvements |
| Command | `/accessibility-audit` | Audit UI for WCAG compliance |
| Skill | `accessibility-compliance` | WCAG 2.2 compliant interfaces, ARIA, screen readers |
| Skill | `analytics` | Plausible, GTM, Yandex.Metrika with consent gating |
| Skill | `design-system-patterns` | Design tokens, theming, component architecture |
| Skill | `interaction-design` | Microinteractions, motion design, transitions |
| Skill | `mobile-android-design` | Material Design 3, Jetpack Compose |
| Skill | `mobile-ios-design` | iOS Human Interface Guidelines, SwiftUI |
| Skill | `responsive-design` | Container queries, fluid typography, CSS Grid |
| Skill | `tailwind-design-system` | Tailwind CSS v4, design tokens, component libraries |
| Skill | `visual-design-foundations` | Typography, color theory, spacing, iconography |

## Data & Databases

| Type | Name | Description |
|------|------|-------------|
| Agent | `database-admin` | Cloud databases, automation, HA, DR, compliance |
| Agent | `database-architect` | Data layer design, schema modeling, technology selection |
| Agent | `database-optimizer` | Query optimization, indexing, caching, partitioning |
| Agent | `data-engineer` | Spark, dbt, Airflow, streaming, cloud-native data platforms |
| Command | `/sql-migrations` | SQL migrations with zero-downtime strategies |
| Command | `/data-pipeline` | Data pipeline architecture (ETL/ELT/Lambda/Kappa) |
| Command | `/data-driven-feature` | Features guided by data insights and A/B testing |
| Command | `/migration-observability` | Migration monitoring, CDC, observability |
| Skill | `airflow-dag-patterns` | Production Airflow DAGs — operators, sensors, testing |
| Skill | `database` | Async database access, migrations, indexing, query rules |
| Skill | `data-quality-frameworks` | Great Expectations, dbt tests, data contracts |
| Skill | `dbt-transformation-patterns` | dbt model organization, testing, documentation |
| Skill | `jobs` | Async job processing with PostgreSQL queue, retries |
| Skill | `postgresql` | PostgreSQL schema design, data types, indexing, performance |
| Skill | `spark-optimization` | Spark partitioning, caching, shuffle, memory tuning |

## AI/ML & Search

| Type | Name | Description |
|------|------|-------------|
| Agent | `ai-engineer` | LLM applications, RAG systems, intelligent agents, multimodal AI |
| Agent | `prompt-engineer` | Chain-of-thought, constitutional AI, production prompt strategies |
| Agent | `vector-database-engineer` | Pinecone, Weaviate, Qdrant, Milvus, pgvector for semantic search |
| Command | `/ai-assistant` | Build AI assistant applications with NLU and dialog management |
| Command | `/langchain-agent` | LangGraph-based agent creation |
| Command | `/prompt-optimize` | Optimize prompts for production with CoT, few-shot |
| Command | `/context-restore` | Semantic memory rehydration for multi-agent workflows |
| Skill | `embedding-strategies` | Embedding model selection, chunking, quality optimization |
| Skill | `hybrid-search-implementation` | Vector + keyword search for improved retrieval |
| Skill | `langchain-architecture` | LangChain 1.x and LangGraph for agents, memory, tools |
| Skill | `llm-evaluation` | Automated metrics, human feedback, benchmarking for LLMs |
| Skill | `prompt-engineering-patterns` | Advanced prompting techniques for production LLM applications |
| Skill | `rag-implementation` | RAG systems with vector databases and semantic search |
| Skill | `similarity-search-patterns` | Efficient similarity search with vector databases |
| Skill | `vector-index-tuning` | HNSW parameters, quantization, scaling vector search |

## Security

| Type | Name | Description |
|------|------|-------------|
| Agent | `firmware-analyst` | Embedded systems, IoT security, hardware reverse engineering |
| Agent | `frontend-security-coder` | XSS prevention, output sanitization, client-side security |
| Agent | `malware-analyst` | Malware research, sandbox analysis, threat intelligence |
| Agent | `mobile-security-coder` | Input validation, WebView security, mobile-specific patterns |
| Agent | `reverse-engineer` | Binary analysis, disassembly, IDA Pro, Ghidra |
| Agent | `security-auditor` | DevSecOps, OWASP, compliance (GDPR/HIPAA/SOC2) |
| Agent | `threat-modeling-expert` | STRIDE, PASTA, attack trees, risk assessment |
| Command | `/security-hardening` | Defense-in-depth security across all layers |
| Command | `/security-sast` | Static Application Security Testing |
| Command | `/security-dependencies` | Dependency vulnerability scanning and SBOM |
| Command | `/xss-scan` | XSS vulnerability detection in frontend code |
| Skill | `anti-reversing-techniques` | Anti-debugging, obfuscation, CTF protections |
| Skill | `attack-tree-construction` | Visualize threat paths, identify defense gaps |
| Skill | `binary-analysis-patterns` | Disassembly, decompilation, control flow analysis |
| Skill | `memory-forensics` | Memory acquisition, process analysis, artifact extraction |
| Skill | `pci-compliance` | PCI DSS compliance for payment card data |
| Skill | `protocol-reverse-engineering` | Packet analysis, protocol dissection, documentation |
| Skill | `sast-configuration` | SAST tools for automated vulnerability detection |
| Skill | `security-requirement-extraction` | Derive security requirements from threat models |
| Skill | `stride-analysis-patterns` | STRIDE methodology for systematic threat identification |
| Skill | `threat-mitigation-mapping` | Map threats to security controls and mitigations |

## DevOps & Infrastructure

| Type | Name | Description |
|------|------|-------------|
| Agent | `deployment-engineer` | CI/CD pipelines, GitOps, progressive delivery, platform engineering |
| Agent | `performance-engineer` | Observability, OpenTelemetry, load testing, Core Web Vitals |
| Skill | `caching` | Redis patterns, TTL policies, cache invalidation |
| Skill | `ci-cd` | GitHub Actions pipelines — linting, tests, Docker, deployment |
| Skill | `docker` | Dockerfile, docker-compose, healthcheck standards |
| Skill | `env-config` | Environment variable conventions, secrets, startup validation |
| Skill | `logging` | Structured logs, levels, correlation IDs |
| Skill | `notifications` | Admin alerts and user notifications (Telegram, email) |

## Testing & Quality

| Type | Name | Description |
|------|------|-------------|
| Agent | `code-reviewer` | AI-powered code analysis, security vulns, performance optimization |
| Agent | `debugger` | Error debugging, test failure analysis |
| Agent | `tdd-orchestrator` | Red-green-refactor discipline, multi-agent TDD coordination |
| Agent | `test-automator` | AI-powered test automation, self-healing tests |
| Command | `/tdd-cycle` | Full TDD workflow with red-green-refactor and checkpoints |
| Command | `/tdd-red` | Write comprehensive failing tests (TDD red phase) |
| Command | `/tdd-green` | Implement minimal code to make failing tests pass |
| Command | `/tdd-refactor` | Refactor code with comprehensive test safety net |
| Command | `/test-generate` | Automated unit test generation with coverage analysis |
| Skill | `temporal-python-testing` | Test Temporal workflows with pytest, time-skipping |
| Skill | `tests` | Unit, integration, frontend testing and coverage workflows |

## Documentation

| Type | Name | Description |
|------|------|-------------|
| Agent | `api-documenter` | OpenAPI 3.1, AI-powered tools, SDK generation, developer portals |
| Agent | `docs-architect` | Comprehensive technical documentation from codebases |
| Agent | `mermaid-expert` | Mermaid diagrams — flowcharts, sequences, ERDs, architectures |
| Agent | `reference-builder` | Exhaustive technical references and API documentation |
| Agent | `tutorial-engineer` | Step-by-step tutorials and educational content from code |
| Command | `/doc-generate` | Automated documentation generation (API, architecture, guides) |
| Command | `/code-explain` | Code explanation with visual diagrams and step-by-step breakdown |
| Skill | `hads` | Technical docs readable by both humans and AI models |

## Payments & Billing

| Type | Name | Description |
|------|------|-------------|
| Agent | `payment-integration` | Stripe, PayPal integration — checkout, subscriptions, webhooks, PCI |
| Skill | `billing-automation` | Recurring payments, invoicing, subscription lifecycle, dunning |
| Skill | `limits-and-credits` | Credit-based billing with ledger balance, payment webhooks |
| Skill | `paypal-integration` | PayPal express checkout, subscriptions, refund management |
| Skill | `payments` | LemonSqueezy and YooKassa setup with currency routing |
| Skill | `stripe-integration` | Stripe checkout, subscriptions, webhooks, PCI-compliant flows |

## SEO

| Type | Name | Description |
|------|------|-------------|
| Agent | `seo-authority-builder` | Analyze E-E-A-T signals, build authority and trust |
| Agent | `seo-cannibalization-detector` | Identify keyword overlap and cannibalization issues |
| Agent | `seo-content-refresher` | Identify outdated content, suggest freshness updates |
| Agent | `seo-keyword-strategist` | Keyword density, semantic variations, LSI keywords |
| Agent | `seo-meta-optimizer` | Optimized meta titles, descriptions, URL suggestions |
| Agent | `seo-snippet-hunter` | Format content for featured snippets and SERP features |
| Agent | `seo-structure-architect` | Header hierarchy, schema markup, internal linking |

## Dev Workflows

| Type | Name | Description |
|------|------|-------------|
| Command | `/deps-audit` | Dependency audit for vulnerabilities, licenses, supply chain risks |
| Command | `/deps-upgrade` | Safe incremental dependency upgrades with migration paths |
| Skill | `changelog-automation` | Changelog generation from commits, PRs, releases |
| Skill | `commit-message` | Conventional commit message generation |
| Skill | `dependency-upgrade` | Major dependency upgrades with compatibility analysis |

## Misc

| Type | Name | Description |
|------|------|-------------|
| Agent | `general` | General-purpose agent for complex questions and multi-step tasks |
| Agent | `explore` | Fast codebase exploration — find files, search code |
| Skill | `error-handling` | Python error handling for FastAPI, Pydantic, asyncio |
| Skill | `translate` | Multilingual app architecture with URL locales and translation files |

## Configuration

| File | Purpose |
|------|---------|
| `opencode.jsonc` | Main OpenCode config (schema: `https://opencode.ai/config.json`) |
| `package.json` | Plugin dependency: `@opencode-ai/plugin@1.17.7` |
| `AGENTS.md` | Global agent instructions |

## Key Patterns

- **Orchestrator Commands**: Complex commands (`feature-development`, `tdd-cycle`, `security-hardening`) use state machines with phase checkpoints, state files in hidden directories, and multi-agent Task tool delegation.
- **State Management**: Each orchestrator maintains a `state.json` with session tracking, resumability, and completion status.
- **Checkpoint Discipline**: Commands stop at phase boundaries and require explicit user approval before proceeding.
- **Agent Delegation**: Commands dispatch work to specialized agents via the `Task` tool with detailed prompts.
