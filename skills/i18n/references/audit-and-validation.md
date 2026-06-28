# Audit And Validation

Use this reference when auditing an existing codebase, replacing hardcoded strings, or validating locale coverage.

## Core Capabilities

- Set up or repair an i18n baseline.
- Replace user-facing strings with stable translation keys.
- Validate locale file parity and placeholder consistency.
- Detect raw UI strings and accessibility labels that still need localization.
- Map backend or domain errors to localized user-facing messages.

## Scope Inputs

Ask only if they are unclear:

- framework and routing style,
- current i18n state,
- target locales,
- translation storage format,
- translation quality requirement,
- whether metadata and SEO need localization.

## Workflow

### 1. Confirm Scope

- Identify the i18n framework and locale locations.
- Confirm the target locales.
- Preserve existing locale conventions when the codebase already has them.

### 2. Set Up Baseline If Missing

- Pick a framework-appropriate library.
- Wire the provider at the app root.
- Add language selection and persistence if applicable.
- Establish locale file layout and namespaces.
  - Prefer domain-split files such as `locales/en/common.json`, `locales/en/auth.json`, `locales/en/errors.json`.
- If metadata is user-facing, localize titles and descriptions too.

### 3. Audit Key Usage And Locale Parity

Run:

```bash
python scripts/i18n_audit.py --src <src-root> --locale <path/to/locale.json> --locale <path/to/locale.json>
```

Treat missing keys and parity gaps as blockers.
Manually verify dynamic keys such as `t(variable)` because static extraction may miss them.

### 4. Find Raw User-Facing Strings

Run:

```bash
python scripts/i18n_checker.py <project_path>
```

Also inspect:

- JSX or template text,
- `aria-label`,
- `title`,
- `placeholder`,
- dialogs, menus, and non-web UI surfaces.

### 5. Replace Strings With Keys

- Use `t('namespace.key')` or the framework equivalent.
- Use placeholders for dynamic values.
- Use plural-aware translation keys instead of manual `if` trees.
- Use Intl or framework formatters for date, number, time, and lists.

### 6. Localize Error Handling

- Map error codes to localized keys.
- Show localized user-facing text only.
- Log raw error details internally, not in the UI.
- Add a safe fallback key for unknown failures.

### 7. Update Locale Files

- Add missing keys in every supported locale.
- Preserve placeholders exactly.
- Avoid renaming existing keys unless the user requests a cleanup.

### 8. Validate

- Re-run the audit until missing and parity issues are zero.
- Validate locale file syntax.
- Update nearby tests only when they materially reduce regression risk.

## Quality Gates

1. No raw UI strings in localized surfaces.
2. No missing keys in target locales.
3. No parity drift between locale files.
4. Plurals and formatting verified for the supported locales.
5. Locale switching works and persists.
6. Localized metadata exists where needed.

## CI Recommendations

1. Compare translation key trees across locale files in CI.
2. Add lint or static checks for forbidden hardcoded UI strings.
3. Fail builds when required translation keys are missing.
4. Keep a PR checklist item: new UI text added to all locales.
5. Track untranslated markers explicitly and block release if present.

## Bundled Scripts

- `scripts/i18n_checker.py`: finds probable hardcoded strings and compares locale file completeness.
- `scripts/i18n_audit.py`: extracts `t(...)` usage and reports missing, unused, and parity-drifted keys.
