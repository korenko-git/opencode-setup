---
name: create-readme
description: Create or rewrite a concise, polished README.md after inspecting the entire project. Use when the user asks to create, generate, improve, refresh, or replace a project README, document repository setup and architecture, or make an open-source project easier to understand and run.
---

# Create README

Create a polished, accurate, and concise `README.md` for the current project.

## Core principles

- Inspect the project before writing. Never produce a generic README from the repository name alone.
- Treat the repository as the source of truth. Do not invent commands, features, environment variables, architecture, deployment steps, URLs, or badges.
- Prefer useful specifics over broad marketing language.
- Keep the document easy to scan and reasonably short.
- Use GitHub Flavored Markdown.
- Use GitHub admonitions only when they make an important warning, note, or tip easier to notice.
- Do not overuse emojis.
- Do not add `License`, `Contributing`, or `Changelog` sections when dedicated files already cover them.
- Preserve correct existing information when rewriting an established README.

## Workflow

### 1. Inspect the workspace

Review the full project structure before editing.

At minimum, inspect:

- the current `README.md`, if present;
- package manifests and lockfiles;
- build, run, test, lint, format, migration, and deployment scripts;
- application entry points;
- configuration files;
- `.env.example` or equivalent environment templates;
- Docker, Compose, CI, infrastructure, and deployment files;
- documentation directories;
- public assets that may contain a project logo, icon, screenshot, or demo;
- license, contribution, and changelog files only to avoid duplicating them;
- the main source directories sufficiently to understand what the project actually does.

Use targeted searches after the initial tree review. Do not read generated directories, dependency folders, build output, caches, vendored code, or large binary files unless they are directly relevant.

Typical exclusions include:

```text
.git
node_modules
.next
dist
build
coverage
vendor
.venv
venv
__pycache__
target
out
.cache
```

### 2. Establish verified project facts

Before drafting, determine as many of these as the repository supports:

- project name and purpose;
- intended users;
- core features;
- primary technologies;
- high-level architecture or major components;
- prerequisites;
- installation procedure;
- local development command;
- production build and run commands;
- tests, linting, formatting, and type-checking commands;
- required services and environment variables;
- deployment path;
- important limitations or caveats;
- documentation links;
- project status or maturity, when explicitly evident.

If a fact cannot be verified, omit it or mark it clearly as unresolved. Do not guess.

### 3. Find header assets

Search for a suitable project logo or icon in common locations such as:

```text
public/
static/
assets/
docs/
.github/
src/assets/
app/
```

Prefer an existing project-specific logo over a framework logo.

When a suitable asset exists:

- reference it with a repository-relative path;
- include meaningful alt text;
- keep dimensions reasonable;
- place it in a centered header only when that presentation suits the project.

Do not create a fake logo or use an unrelated image.

### 4. Choose the README structure

Adapt the structure to the project. A strong default is:

1. Header with logo, project name, and one-sentence value proposition
2. Relevant badges, only when their targets and values are verifiable
3. Compact navigation links for longer READMEs
4. Overview
5. Features
6. Architecture or project structure, when useful
7. Getting started
8. Configuration
9. Development commands
10. Deployment, when supported
11. Troubleshooting or important notes, when necessary
12. Additional documentation or resources

Do not force every section into every README.

For small libraries or CLI tools, prioritize:

- what it does;
- installation;
- minimal usage example;
- options or API surface;
- development commands.

For applications, prioritize:

- purpose and screenshots;
- architecture;
- prerequisites;
- configuration;
- local startup;
- deployment.

For monorepos, explain the packages or services and how they work together.

See [README guidance](references/readme-guidance.md) for detailed structural patterns and quality rules.

### 5. Write the README

Use direct, concrete language.

Prefer:

```markdown
Run the development server:

```bash
npm run dev
```
```

Avoid:

```markdown
In order to begin your exciting development journey, you will first want to...
```

Requirements:

- use correct heading hierarchy;
- add a blank line around headings, lists, code fences, and admonitions;
- specify a language for code fences;
- use repository-relative links for local files;
- keep shell commands copy-pasteable;
- explain where commands must be run when the repository has multiple packages;
- document placeholders explicitly;
- avoid giant file-tree dumps;
- avoid repeating the same setup instructions in multiple sections;
- avoid unsupported performance, security, scalability, or production-readiness claims.

Use GitHub admonitions sparingly:

```markdown
> [!NOTE]
> Explain context that materially affects setup or usage.

> [!TIP]
> Surface a useful shortcut or local-development option.

> [!WARNING]
> Highlight a destructive operation or a serious compatibility issue.
```

### 6. Validate against the repository

Before finishing:

1. Re-check every documented command against scripts or configuration.
2. Re-check every path and local link.
3. Confirm environment variable names and distinguish required from optional values.
4. Confirm prerequisites and version constraints.
5. Confirm that no dedicated-file sections were duplicated.
6. Confirm that badges resolve to real workflows, packages, or project metadata.
7. Confirm that the README does not expose secrets.
8. Confirm that the content reflects the current repository rather than stale comments or archived files.
9. Review the rendered Markdown structure mentally for broken fences, malformed tables, and bad nesting.
10. Keep the final document concise enough that a new contributor can find setup instructions quickly.

If feasible, run the project's existing Markdown formatter or linter. Do not install new dependencies solely to format the README unless the user requested it.

## Editing behavior

- Create `README.md` when it does not exist.
- Rewrite it when the existing file is substantially inaccurate, incomplete, or poorly structured.
- Prefer focused edits when the existing README is already strong.
- Do not modify unrelated files.
- Do not create `LICENSE`, `CONTRIBUTING`, or `CHANGELOG` files.
- Do not commit changes unless explicitly requested.

## Completion response

After writing, report:

- that `README.md` was created or updated;
- the major sections included;
- any important facts that could not be verified;
- validation commands run, if any.

Keep the completion response brief. The README itself is the deliverable.
