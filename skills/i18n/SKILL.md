---
name: i18n
description: Unified i18n architecture, localization workflow, and audit toolkit. Invoke when adding translations, fixing hardcoded UI copy, configuring locale routing, or validating locale parity and localized SEO.
---

# I18n Suite

Unified skill for multilingual product architecture, UI localization, and i18n validation.
Prioritize the baseline in this skill before applying framework-specific or product-specific conventions.

## What This Skill Covers

- Locale architecture and deterministic language selection.
- Translation key design, namespaces, and message formatting.
- Framework guidance for Next.js and React i18n codebases.
- Detection of hardcoded strings and locale parity gaps.
- Localized metadata, routing, navigation, and SEO behavior.
- Audit workflows for existing apps that already ship with locale files.

## When To Use

Use this skill when the task involves any of the following:

- adding i18n to a new or existing interface,
- replacing hardcoded UI strings with translation keys,
- designing locale routing, detection, or persistence,
- reviewing locale files for missing keys or bad structure,
- localizing metadata, sitemaps, or `hreflang`,
- auditing a codebase for translation coverage, parity, or formatting issues.

## Core Defaults

Apply these defaults unless the codebase already has a clear established convention:

1. Language selection must be deterministic:
   - URL, user setting, or browser preference in a documented order.
2. All user-facing text must come from translation resources.
3. Locale-aware navigation, metadata, and SEO must stay correct for every locale.
4. Keep locale configuration in one place:
   - `locales`,
   - `defaultLocale`,
   - locale strategy,
   - locale detection policy.
5. For new greenfield multilingual products, the baseline locale set is:
   - `uk`, `en`, `es`, `pt`, `ru`.
6. If the target product already has an established locale matrix, preserve it unless the user asks to expand or change it.
7. Prefer splitting translation resources by domain or namespace instead of one oversized locale file.
   - Example: `locales/en/common.json`, `locales/en/auth.json`, `locales/en/errors.json`.

## Capability Map

| Task | Go To |
|------|-------|
| Locale architecture, routing, metadata, SEO | `references/architecture-and-routing.md` |
| UI key design, locale files, hardcoded string replacement, audits | `references/audit-and-validation.md` |
| General localization patterns, ICU, RTL, formatting | `references/localization-patterns.md` |

## Quick Decision Guide

```text
User wants to...
├── set up i18n for a new app? ───────────────────────── architecture-and-routing.md
├── localize an existing UI or remove hardcoded strings? audit-and-validation.md
├── validate pluralization, RTL, Intl, or locale files? localization-patterns.md
└── do an end-to-end i18n audit? ─────────────────────── Integrated Workflow below
```

## Integrated Workflow

Use this for a full i18n implementation or audit pass.

### Step 1: Identify Context

Collect the minimum useful inputs:

- framework and routing style,
- current i18n state: none, partial, or legacy,
- target locales and default locale,
- translation storage format,
- whether SEO-localized routes and metadata matter,
- whether the codebase already has product-specific conventions.

### Step 2: Choose The Baseline

Apply the strongest matching baseline in this order:

1. Existing project convention that is already implemented.
2. This skill's architecture defaults.
3. Framework-specific best practice from the reference files.

Do not mix conflicting conventions in one implementation pass.

### Step 3: Implement Or Audit

1. Define routing, locale detection, and persistence.
2. Move visible strings into translation resources.
3. Standardize keys, placeholders, and pluralization.
4. Localize metadata and alternate URLs when relevant.
5. Run the bundled checks:
   - `python scripts/i18n_checker.py <project_path>`
   - `python scripts/i18n_audit.py --src <src-root> --locale <file> --locale <file>`

### Step 4: Validate

Treat these as blockers:

- missing translation keys,
- locale file parity drift,
- raw user-facing UI strings,
- broken locale persistence or route handling,
- localized SEO metadata missing where required.

## Non-Negotiable Rules

1. Never hardcode visible UI text in components when the product is meant to be localized.
2. Keep locale files key-identical unless the framework intentionally uses a different split.
3. Use placeholders instead of string concatenation.
4. Prefer library pluralization and formatting APIs over manual branching.
5. Keep locale-aware routing and internal navigation consistent.
6. Exclude API, static assets, and internal framework paths from locale middleware.
7. Do not expose raw backend or exception messages directly in UI; map to localized user-facing messages.
8. Preserve product names, APIs, and technical terms untranslated when that is the established convention.

## Libraries

- Next.js App Router: prefer `next-intl`.
- React apps: prefer `i18next` + `react-i18next`.
- Existing app conventions can justify `FormatJS` or `LinguiJS`, but keep one stack project-wide.

## Expected Output Shape

When using this skill, aim to produce implementation-ready guidance or edits:

- locale strategy,
- file layout,
- translation key changes,
- component integration approach,
- validation steps,
- remaining risks or missing inputs.
