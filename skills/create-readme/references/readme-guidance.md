# README Guidance

Use this reference when deciding how to structure and polish the generated README.

## Design patterns

The inspiration repositories use several effective patterns:

- a centered header for visually oriented applications;
- a small project logo or icon above the title;
- one direct sentence explaining the project;
- a limited set of meaningful badges;
- compact anchor navigation for longer documents;
- an early screenshot, animation, or architecture image when it improves understanding;
- a short overview before implementation details;
- copy-pasteable setup commands;
- explicit local-development and deployment paths;
- short feature lists with bold lead-ins;
- GitHub admonitions for high-value notes rather than decorative callouts.

Use these patterns selectively. Match the project rather than cloning another README's layout.

## Recommended section content

### Header

A header may contain:

```html
<div align="center">
  <img src="./path/to/logo.png" alt="Project logo" height="72" />

  # Project Name

  One sentence explaining the project's purpose.
</div>
```

Do not use an empty `alt` attribute for a meaningful logo.

Only add badges backed by verified project metadata, such as:

- an actual CI workflow;
- a published package version;
- a documented runtime version;
- a real deployment link;
- a valid documentation site.

Avoid decorative badge walls.

### Overview

Answer three questions quickly:

1. What is this project?
2. Who is it for?
3. What problem does it solve?

One to three paragraphs are usually enough.

### Features

Use concrete capabilities rather than vague qualities.

Good:

```markdown
- **Local inference:** Connects to an OpenAI-compatible local model endpoint.
- **Asynchronous processing:** Runs extraction jobs through a worker queue.
```

Weak:

```markdown
- Fast
- Powerful
- Modern
- Easy to use
```

### Architecture

Include architecture only when it helps a reader operate or extend the project.

Prefer a small component list or diagram over a long implementation narrative. Describe:

- major services or packages;
- their responsibilities;
- key data flow;
- external dependencies.

Do not infer architecture solely from framework names.

### Getting started

A reliable setup section typically includes:

1. prerequisites;
2. clone or repository-entry step when useful;
3. dependency installation;
4. environment configuration;
5. required supporting services;
6. database setup or migrations;
7. development command;
8. local URL or expected result, only when verified.

Use one package manager consistently based on the lockfile.

### Configuration

Use a table only when it improves clarity:

```markdown
| Variable | Required | Description |
| --- | --- | --- |
| `DATABASE_URL` | Yes | PostgreSQL connection string. |
| `LOG_LEVEL` | No | Application log level. Defaults to `info`. |
```

Never include real secrets. Use safe examples and preserve exact variable names.

### Commands

A compact command table works well for projects with several scripts:

```markdown
| Command | Description |
| --- | --- |
| `npm run dev` | Start the development server. |
| `npm test` | Run the test suite. |
| `npm run lint` | Run static analysis. |
```

Only document commands that exist.

### Project structure

Include only important directories:

```text
src/          Application source
tests/        Automated tests
docs/         Additional documentation
```

Avoid dumping hundreds of paths.

### Troubleshooting

Add this section only for problems that are:

- documented in the repository;
- implied by required infrastructure;
- likely to block setup;
- accompanied by a verified remedy.

Do not invent troubleshooting advice.

## Tone

Use a professional open-source tone:

- direct;
- technically precise;
- welcoming without being promotional;
- concise;
- free of filler.

Avoid phrases such as:

- “revolutionary”;
- “cutting-edge” unless objectively necessary;
- “seamless”;
- “supercharge”;
- “unlock the power of”;
- “whether you're a beginner or an expert”.

## GitHub Flavored Markdown checks

Confirm:

- tables have header separators;
- task lists use `- [ ]`;
- code fences close correctly;
- nested lists are indented consistently;
- relative links use forward slashes;
- heading anchors are not manually invented unless needed;
- HTML blocks are closed;
- admonition labels use uppercase supported forms.

## Concision test

Remove content that:

- repeats information;
- describes obvious commands without adding context;
- documents internal implementation details irrelevant to setup or use;
- belongs in dedicated documentation;
- makes claims not supported by the repository.

The ideal README gives a new reader enough information to understand, run, and evaluate the project without becoming a complete reference manual.
