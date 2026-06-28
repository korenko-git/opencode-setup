# Architecture And Routing

Use this reference for greenfield i18n setup, locale routing, and localized metadata.

## Goal

Build a multilingual interface where:

- language is selected deterministically by URL, user setting, or browser preference,
- all user-facing text comes from translation files,
- navigation, metadata, and SEO stay correct for each locale.

## Baseline Locale Policy

- For new multilingual products, ship with `uk`, `en`, `es`, `pt`, `ru`.
- When a product has region-specific defaults, use the order: Ukraine first, international second, Russia third.
- If the codebase already uses a narrower locale matrix, preserve that unless the user asks to expand it.

## Recommended Architecture

1. Keep locale configuration in one place:
   - `locales`,
   - `defaultLocale`,
   - locale strategy such as `always in URL` or `as-needed`,
   - locale detection policy.
2. Use URL-based locales for web apps whenever SEO or shareability matters.
   - Example: `/uk/...`, `/en/...`.
3. Separate translation resources from UI logic.
   - Store messages per locale and per domain.
   - Group domains by namespaces such as `common`, `auth`, `checkout`, `profile`, `errors`.
4. Load translations close to render time.
   - Server-side for server-rendered pages and metadata.
   - Client-side hooks for interactive components.

## Generic Folder Structure

```text
app/
  [locale]/
    layout.tsx
    page.tsx
    ...feature pages
  sitemap.ts
i18n/
  routing.ts
  request.ts
  middleware.ts
locales/
  uk/
    common.json
    auth.json
    errors.json
  en/
    common.json
    auth.json
    errors.json
  es/
    common.json
    auth.json
    errors.json
  pt/
    common.json
    auth.json
    errors.json
  ru/
    common.json
    auth.json
    errors.json
```

Equivalent structures are fine if responsibilities stay split:

- routing config,
- request or locale resolution,
- middleware,
- translation dictionaries,
- locale-aware pages and layouts.

Prefer domain-split locale files over one giant `messages/<locale>.json` file because it scales better for feature ownership, audits, and partial loading.

## Routing And Navigation Rules

1. Use locale-aware link and router helpers for internal navigation.
2. Keep locale when changing routes.
3. Validate locale from URL and fall back to `defaultLocale` when invalid.
4. Exclude API, static, and internal asset paths from locale middleware.

## Components

1. Client components use i18n hooks such as `useTranslations` or `useTranslation`.
2. Server pages and layouts use the server translation API.
3. Keep locale-dependent logic explicit:
   - currency,
   - support links,
   - legal copy,
   - date formatting.

## SEO And Metadata

1. Localize metadata:
   - `title`,
   - `description`,
   - OpenGraph,
   - Twitter cards,
   - JSON-LD where relevant.
2. Provide `hreflang` alternates for each locale and `x-default`.
3. Generate locale-specific sitemap entries.
4. Keep canonical and alternate URLs consistent with the locale strategy.

## Rollout Checklist

1. Define locales and fallback rules.
2. Set up locale-aware routing.
3. Add translation provider and request-level locale loading.
4. Migrate visible strings to translation keys.
5. Localize metadata and sitemap.
6. Add CI checks for translation completeness.
7. Test all locales for navigation, SEO tags, and runtime behavior.
