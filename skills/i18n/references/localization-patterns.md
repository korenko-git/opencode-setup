# Localization Patterns

Use this reference for general localization rules, ICU-style messages, formatting, and RTL readiness.

## Core Concepts

| Term | Meaning |
|------|---------|
| `i18n` | Internationalization: making the app translatable |
| `l10n` | Localization: producing locale-specific output |
| `locale` | Language and region, such as `en-US` |
| `RTL` | Right-to-left languages such as Arabic or Hebrew |

## Best Practices

### Do

- Use translation keys instead of raw text.
- Namespace translations by feature or domain area.
- Support pluralization in the i18n layer.
- Format dates, numbers, times, and lists per locale.
- Plan for RTL from the start when RTL locales are in scope.
- Use ICU or equivalent message formatting for complex strings.

### Do Not

- Hardcode strings in components.
- Concatenate translated fragments.
- Assume all languages fit the same length.
- Forget logical CSS when RTL may be added.
- Mix unrelated languages or conventions in the same resource file.

## File Layout Patterns

Any of these are acceptable if the project is consistent:

- per-locale namespace files such as `locales/en/common.json`,
- one file per locale such as `messages/en.json`,
- source locale modules plus generated JSON output.

Prefer per-locale domain files such as `locales/en/common.json`, `locales/en/auth.json`, and `locales/en/errors.json` over a single large locale file.
The key rule is parity and maintainability, not one exact folder shape.

## Formatting Guidance

- Dates: `Intl.DateTimeFormat`
- Numbers and currency: `Intl.NumberFormat`
- Relative time: `Intl.RelativeTimeFormat` or framework equivalent
- Lists: `Intl.ListFormat`

Keep formatting locale-aware instead of manual string assembly.

## RTL Guidance

Only apply RTL support when RTL locales are in scope, but do not block future support with left or right-specific styling.

```css
.container {
  margin-inline-start: 1rem;
  padding-inline-end: 1rem;
}

[dir="rtl"] .icon {
  transform: scaleX(-1);
}
```

## Common Failure Modes

- Missing translations without fallback behavior.
- Hardcoded accessibility labels.
- Broken pluralization rules.
- Incorrect number or date formatting.
- Layout regressions in longer translated strings.
- Incomplete metadata localization.

## Shipping Checklist

- All user-facing strings use translation keys.
- Locale files exist for all supported languages.
- Date and number formatting uses locale-aware APIs.
- RTL layout tested if applicable.
- Fallback locale configured.
- No obvious hardcoded strings remain.
