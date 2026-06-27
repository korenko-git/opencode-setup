---
name: payments-integration
description: Integrate Stripe, PayPal, LemonSqueezy, and YooKassa payment processors. Handles checkout flows, subscriptions, webhooks, currency routing, and PCI compliance. Use PROACTIVELY when implementing payments, billing, or subscription features.
---

# Payments Integration

Master payment processing integration across multiple providers: Stripe, PayPal, LemonSqueezy, and YooKassa. Covers checkout flows, subscriptions, recurring billing, webhooks, refunds, currency routing, and PCI compliance.

## When to Use This Skill

- Implementing payment processing in web/mobile applications
- Setting up subscription billing systems
- Handling one-time payments and recurring charges
- Processing refunds and disputes
- Managing customer payment methods
- Building marketplace payment flows (Stripe Connect)
- Routing payments by currency (UAH, USD, RUB)
- Implementing SCA for European payments

## Provider Quick Reference

| Provider | Best For | Currencies | Key Features |
|---|---|---|---|
| **Stripe** | General purpose, global | All major currencies | Checkout, subscriptions, Connect, Elements |
| **PayPal** | Express checkout, guest payments | USD, EUR, GBP + many more | Smart buttons, payouts, subscriptions |
| **LemonSqueezy** | Link-in-bio, simple products | UAH, USD | Tax handling, one-click setup |
| **YooKassa** | Russian market | RUB | Local payment methods, fiscalization |

## Currency and Provider Mapping

The user selects a **currency**, not a provider. The backend picks the provider automatically:

| Currency | Provider |
|---|---|
| UAH | LemonSqueezy |
| USD | LemonSqueezy or Stripe |
| RUB | YooKassa |

### Default Currency per Locale

| Locale | Default currency |
|---|---|
| `uk` | UAH |
| `en` | USD |
| `es` | USD |
| `pt` | USD |
| `ru` | RUB |

### Frontend Behavior

1. On page load, pre-select the default currency based on the current locale.
2. Show a currency selector (`UAH` / `USD` / `RUB`) so the user can override the default.
3. Send the chosen currency to the backend. Do not send provider name — the backend decides.
4. On response, redirect to `confirmation_url` regardless of provider.

### Backend Behavior

1. Receive currency from frontend.
2. Pick provider based on currency mapping.
3. Return unified response: `{ confirmation_url, payment_provider }`.
4. Handle webhooks on separate endpoints per provider.

---

## Critical Requirements — Webhook Security & Idempotency

- **Signature Verification**: ALWAYS verify webhook signatures using official SDKs (Stripe, LemonSqueezy use HMAC). Never process unverified webhooks.
- **Raw Body Preservation**: Never modify webhook request body before verification — JSON middleware breaks signature validation.
- **Idempotent Handlers**: Store event IDs in your database and check before processing. Webhooks retry on failure; providers don't guarantee single delivery.
- **Quick Response**: Return `2xx` within 200ms, BEFORE expensive operations. Timeouts trigger retries and duplicate processing.
- **Server Validation**: Re-fetch payment status from provider API. Never trust webhook payload or client response alone.

### PCI Compliance Essentials

- **Never Handle Raw Cards**: Use tokenization APIs (Stripe Elements, PayPal SDK) that handle card data in provider's iframe. NEVER store, process, or transmit raw card numbers.
- **Server-Side Validation**: All payment verification must happen server-side via direct API calls to the payment provider.
- **Environment Separation**: Test credentials must fail in production. Misconfigured gateways commonly accept test cards on live sites.

---

## Provider Details

Provider-specific implementation details are in `references/`:

- `stripe.md` — Checkout Sessions, Payment Intents, Elements, subscriptions, webhooks, test cards
- `paypal.md` — Smart Buttons, REST API orders/captures, IPN handling, subscriptions
- `lemonsqueezy.md` — Checkout creation, webhook signature verification, UAH/USD setup
- `yookassa.md` — Payment creation with Idempotence-Key, webhook verification via API, RUB payments

Read the relevant reference file when implementing a specific provider.

---

## Common Failures

**Real-world examples from Stripe, PayPal, OWASP:**

- Payment processor collapse during traffic spike → webhook queue backups, revenue loss
- Out-of-order webhooks breaking functions (no idempotency) → production failures
- Malicious price manipulation on unencrypted payment buttons → fraudulent payments
- Test cards accepted on live sites due to misconfiguration → PCI violations
- Webhook signature skipped → system flooded with malicious requests

---

## Output

When implementing a payment feature, always provide:

- Payment integration code with error handling
- Webhook endpoint implementations with security verification
- Database schema for payment records (if needed)
- Security checklist (PCI compliance points)
- Test payment scenarios and edge cases
- Environment variable configuration

Always use official SDKs. Include both server-side and client-side code where needed.
