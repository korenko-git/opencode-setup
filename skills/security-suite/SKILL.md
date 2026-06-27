---
name: security-suite
description: >
  Unified security suite for comprehensive application security. Use PROACTIVELY whenever the user
  mentions security, vulnerabilities, audits, hardening, XSS, injection, authentication, dependencies,
  SAST, compliance (OWASP/GDPR/SOC2/PCI-DSS), or secure coding. Covers the full security lifecycle:
  threat modeling → vulnerability scanning → secure coding (backend/frontend/mobile) → dependency
  auditing → hardening orchestration → compliance validation.
---

# Security Suite

Unified security toolkit covering the full application security lifecycle — from threat modeling
and vulnerability scanning to secure coding, dependency auditing, and compliance validation.

## Capability Map

| Task | Go To |
|------|-------|
| Security audit, threat modeling, DevSecOps, compliance | → `references/auditor.md` |
| Secure backend code, API security, authentication, DB | → `references/backend.md` |
| XSS prevention, CSP, DOM security, frontend code | → `references/frontend.md` |
| Mobile security, WebView, biometrics, certificate pinning | → `references/mobile.md` |
| SAST scanning, static analysis, multi-language tools | → `references/sast.md` |
| XSS scanning specifically | → `references/xss-scan.md` |
| Dependency CVE scanning, SBOM, supply chain | → `references/deps.md` |
| Full hardening orchestration (multi-phase pipeline) | → `references/hardening.md` |
| Security requirements from threat models | → below (inline) |

---

## Quick Decision Guide

```
User wants to...
├── Audit / assess / threat model / compliance? ──────────── auditor.md
├── Write or fix secure code?
│   ├── Backend (API, DB, auth, server)? ─────────────────── backend.md
│   ├── Frontend (React/Vue/JS, DOM, CSP)? ───────────────── frontend.md
│   └── Mobile (iOS/Android, WebView)? ────────────────────── mobile.md
├── Scan code for vulnerabilities?
│   ├── General SAST (multi-language)? ────────────────────── sast.md
│   └── XSS specifically? ──────────────────────────────────── xss-scan.md
├── Check/fix dependencies (CVE, licenses, SBOM)? ─────────── deps.md
├── Run full hardening pipeline (13-step orchestration)? ──── hardening.md
└── Extract security requirements from threats? ────────────── (inline below)
```

---

## Security Requirement Extraction (inline)

Use when translating threat models or business context into actionable security requirements,
user stories, or test cases.

### Requirement Categories

```
Business Requirement  →  Security Requirement   →  Technical Control
"Protect user data"      "Encrypt PII at rest"     "AES-256 + KMS rotation"
```

### Requirement Types

| Type | Focus | Example |
|------|-------|---------|
| **Functional** | What system must do | "Must authenticate all API requests" |
| **Non-functional** | How it performs | "Auth must complete in <2s" |
| **Constraint** | Imposed limits | "Must use approved crypto libraries" |

### Required Attributes per Requirement

- **Traceability** — links to a specific threat or compliance control
- **Testability** — can be verified (automated or manual)
- **Priority** — business criticality (Critical / High / Medium / Low)
- **Acceptance Criteria** — definition of "done"

### Template

```markdown
## REQ-[ID]: [Short Title]

**Category**: Functional | Non-functional | Constraint
**Priority**: Critical | High | Medium | Low
**Source Threat**: [STRIDE category or threat ID]
**Compliance**: [OWASP ASVS / GDPR / SOC2 / PCI-DSS control]

**Requirement**:
[System/Component] MUST [action] WHEN [condition] IN ORDER TO [security goal].

**Acceptance Criteria**:
- [ ] [Specific, testable criterion]
- [ ] [Another criterion]

**Technical Controls**:
- [Concrete implementation — algorithm, library, config]
```

### Anti-patterns to Avoid

- ❌ "Be secure" — not a requirement
- ❌ "Use strong encryption" — not specific (name the algorithm)
- ❌ No acceptance criteria — can't verify it's done
- ❌ Not traced to a threat — can't justify priority

---

## Best Practices (Cross-Cutting)

These apply regardless of which reference you load:

1. **Defense in depth** — never rely on a single control
2. **Principle of least privilege** — everywhere, always
3. **Fail securely** — default deny, graceful degradation
4. **Validate all inputs** — allowlist, not denylist
5. **Shift left** — security in CI/CD, not just at release
6. **Never trust user input** — validate at every layer
7. **Audit logging** — all auth events, all failures, no secrets in logs
8. **Dependency hygiene** — scan daily, patch patch-versions automatically
9. **Secrets out of code** — env vars, Vault, cloud secret managers
10. **Test security controls** — SAST + DAST + manual pen test

---

## Reference Files

Load only the file relevant to the current task. Each file is self-contained.

- `references/auditor.md` — Security auditor: DevSecOps, compliance, threat modeling, pen test planning
- `references/backend.md` — Backend secure coder: API, DB, auth, CSRF, headers, secrets
- `references/frontend.md` — Frontend secure coder: XSS, CSP, DOM, clickjacking, redirects
- `references/mobile.md` — Mobile secure coder: WebView, biometrics, cert pinning, storage
- `references/sast.md` — SAST scanner: multi-language static analysis, tool configs, CI/CD integration
- `references/xss-scan.md` — XSS scanner: framework-specific detection, reporting, prevention
- `references/deps.md` — Dependency scanner: CVE lookup, SBOM, supply chain, auto-remediation
- `references/hardening.md` — Hardening orchestrator: 13-step phased pipeline with checkpoints
