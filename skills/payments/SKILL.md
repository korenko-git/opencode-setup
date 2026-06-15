---
name: "payments"
description: "Payment provider setup for LemonSqueezy and YooKassa with currency routing and webhooks. Invoke when adding checkout, billing, or payment provider logic."
---

# Payments Integration Rule

## Payment Providers

Use the provider that matches the selected currency:
- **LemonSqueezy** for `UAH` and `USD` payments (see `./lemonsqueezy.md`)
- **YooKassa** for `RUB` payments when that market is required (see `./yookassa.md`)

## Currency and Provider Mapping

The user selects a **currency**, not a provider. The backend picks the provider automatically:

| Currency | Provider |
|---|---|
| UAH | LemonSqueezy |
| USD | LemonSqueezy |
| RUB | YooKassa |

## Default Currency per Locale

Each locale (see the `translate` skill) has a default currency pre-selected in the UI:

| Locale | Default currency |
|---|---|
| `uk` | UAH |
| `en` | USD |
| `es` | USD |
| `pt` | USD |
| `ru` | RUB |

## Currency Selector

On every locale the user can switch between `UAH`, `USD`, and `RUB` regardless of the default. The selector is a simple toggle/dropdown in the payment step. It should show the currency only, not the provider name.

## Frontend Behavior

1. On page load, pre-select the default currency based on the current locale.
2. Show a currency selector (`UAH` / `USD` / `RUB`) so the user can override the default.
3. Send the chosen currency to the backend. Do not send provider name — the backend decides.
4. On response, redirect to `confirmation_url` regardless of provider.

## Backend Behavior

1. Receive the chosen currency from the frontend.
2. Pick the provider based on currency:
   - `UAH` → create checkout via LemonSqueezy
   - `USD` → create checkout via LemonSqueezy
   - `RUB` → create payment via YooKassa only when RUB support is enabled for the project
3. Return a unified response shape with `confirmation_url` and `payment_provider` (for frontend logging/analytics only).
4. Handle webhooks on separate endpoints per provider.

---

## Related Provider Guides

- `lemonsqueezy.md` - Provider-specific implementation details for `UAH` and `USD` payments via LemonSqueezy.
- `yookassa.md` - Provider-specific implementation details for `RUB` payments via YooKassa.

