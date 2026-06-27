---
name: seo-suite
description: Unified SEO optimization suite for content strategy, on-page improvements, SERP formatting, freshness, structure, cannibalization, and E-E-A-T. Invoke when the user asks for SEO help or wants to optimize existing/new content.
---

# SEO Suite

Unified SEO toolkit for auditing, improving, and packaging content for search visibility.
Use this skill when the task touches keyword targeting, metadata, snippets, structure, freshness,
authority signals, or overlapping pages.

## Capability Map

| Task | Go To |
|------|--------|
| Keyword targeting, density, entities, semantic coverage | `references/keyword-strategy.md` |
| Meta titles, descriptions, URL slugs, CTR improvements | `references/meta-optimization.md` |
| Featured snippets, PAA blocks, concise answer formatting | `references/snippet-optimization.md` |
| Header hierarchy, schema, internal links, content flow | `references/structure-architecture.md` |
| E-E-A-T, trust signals, author bios, citations | `references/authority.md` |
| Outdated stats, old examples, freshness updates | `references/content-refresh.md` |
| Competing pages, overlap, consolidation decisions | `references/cannibalization.md` |
| Full-page SEO review | `Integrated Audit Workflow` below |

---

## Quick Decision Guide

```text
User wants to...
├── Improve keyword targeting or semantic depth? ─────────── keyword-strategy.md
├── Rewrite title/meta/slug for better CTR? ─────────────── meta-optimization.md
├── Capture featured snippets or PAA? ───────────────────── snippet-optimization.md
├── Fix headings, schema, TOC, or internal links? ───────── structure-architecture.md
├── Add trust, expertise, and E-E-A-T signals? ──────────── authority.md
├── Update aging content with newer info? ───────────────── content-refresh.md
├── Compare multiple similar pages? ─────────────────────── cannibalization.md
└── Audit a page end-to-end? ────────────────────────────── Integrated Audit Workflow
```

---

## Integrated Audit Workflow

Use this when the user asks for a full SEO review of one page or a small page set.

### Step 1: Identify Inputs

Collect what is available:

- URL or page path
- Raw content or markdown
- Current title/meta
- Target keyword(s)
- Search intent or audience
- Competing pages, if overlap is suspected

### Step 2: Classify Intent

Determine whether the page is primarily:

- Informational
- Commercial investigation
- Transactional
- Navigational
- Branded authority content

### Step 3: Run the Relevant Modules

Load only the reference files relevant to the request:

1. `references/keyword-strategy.md`
2. `references/meta-optimization.md`
3. `references/snippet-optimization.md`
4. `references/structure-architecture.md`
5. `references/authority.md`
6. `references/content-refresh.md`
7. `references/cannibalization.md`

### Step 4: Prioritize Recommendations

Use this order unless the user specifies otherwise:

1. Critical correctness issues
2. Search intent mismatch
3. Cannibalization/conflict risk
4. Missing metadata or poor CTR setup
5. Weak structure/snippet formatting
6. Missing authority signals
7. Freshness improvements

### Step 5: Produce Actionable Output

Always deliver concise, implementation-ready recommendations.
Prefer concrete rewrites over abstract advice.

Recommended output shape:

```markdown
## SEO Audit Summary

Primary Intent: [intent]
Primary Keyword: [keyword]
Priority: High / Medium / Low

### Top Issues
- [Issue with impact]
- [Issue with impact]

### Recommended Fixes
1. [Specific change]
2. [Specific change]
3. [Specific change]

### Optional Enhancements
- [Nice-to-have improvement]
```

---

## Best Practices

Apply these across all SEO tasks:

1. Optimize for search intent before keywords
2. Prefer specific rewrites over generic advice
3. Keep recommendations measurable and prioritized
4. Use natural language, not keyword stuffing
5. Improve user clarity first; rankings follow usefulness
6. Recommend schema only when it matches the actual content
7. Treat freshness updates as value-add changes, not cosmetic edits

## Reference Files

Load only the file relevant to the current task. Each file preserves the detailed guidance
from the previous specialized SEO agents.

- `references/keyword-strategy.md` - Density, entities, LSI keywords, semantic coverage
- `references/meta-optimization.md` - Titles, descriptions, URL slugs, CTR variations
- `references/snippet-optimization.md` - Featured snippets, PAA, FAQ/HowTo formatting
- `references/structure-architecture.md` - Headings, schema, TOC, internal linking
- `references/authority.md` - E-E-A-T, trust signals, author credibility, citations
- `references/content-refresh.md` - Freshness updates, stale stats, publishing refreshes
- `references/cannibalization.md` - Overlap analysis, consolidation, canonical strategy

## Default Response Style

When using this skill:

- Be concise, concrete, and implementation-ready
- Show improved copy when possible
- Separate `High Priority` from `Nice to Have`
- Call out assumptions when source inputs are missing
- If multiple pages are involved, compare them explicitly
