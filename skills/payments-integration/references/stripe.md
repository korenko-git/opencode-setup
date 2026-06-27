# Stripe Integration Guide

Universal guide for integrating payments via Stripe. Supports one-time payments, subscriptions, and custom checkout flows.

## Environment Variables

```
STRIPE_SECRET_KEY      # sk_test_... / sk_live_...
STRIPE_PUBLISHABLE_KEY # pk_test_... / pk_live_...
STRIPE_WEBHOOK_SECRET  # whsec_... for signature verification
```

## Quick Start — Checkout Session (Recommended)

```python
import stripe

stripe.api_key = "sk_test_..."

# Create a checkout session
session = stripe.checkout.Session.create(
    line_items=[{
        'price_data': {
            'currency': 'usd',
            'product_data': {'name': 'Premium Subscription'},
            'unit_amount': 2000,  # $20.00 in cents
            'recurring': {'interval': 'month'},
        },
        'quantity': 1,
    }],
    mode='subscription',  # or 'payment' for one-time
    success_url='https://yourdomain.com/success?session_id={CHECKOUT_SESSION_ID}',
    cancel_url='https://yourdomain.com/cancel',
)

# Redirect user to session.url
print(session.url)
```

## Payment Flows

### Checkout Sessions (Recommended)

- Best for most integrations — lower maintenance burden
- UI modes: Stripe-hosted page, embedded form, or custom UI with Elements (`ui_mode='custom'`)
- Built-in features: line items, discounts, tax, shipping, address collection, saved payment methods

### Payment Intents (Full Control)

- You calculate final amount with taxes, discounts, etc. yourself
- More complex; requires Stripe.js for PCI compliance
- Use when Checkout Sessions don't fit your needs

### Setup Intents (Save Payment Methods)

- Collect payment method without charging
- Used for subscriptions and future payments

## Elements — Custom UI

```python
# Backend: Create session with ui_mode='custom'
session = stripe.checkout.Session.create(
    mode='payment',
    ui_mode='custom',
    line_items=[{
        'price_data': {
            'currency': 'usd',
            'product_data': {'name': 'Product'},
            'unit_amount': 1000,
        },
        'quantity': 1,
    }],
    return_url='https://yourdomain.com/complete?session_id={CHECKOUT_SESSION_ID}'
)
return session.client_secret  # Send to frontend
```

```javascript
// Frontend: Mount Payment Element
const stripe = Stripe("pk_test_...");
const checkout = stripe.initCheckout({ clientSecret, elementsOptions: { theme: "stripe" } });
const result = await checkout.loadActions();

if (result.type === "success") {
  const { actions } = result;
  const paymentElement = checkout.createPaymentElement();
  paymentElement.mount("#payment-element");

  document.getElementById("pay-button").addEventListener("click", () => {
    actions.confirm().then((r) => {
      if (r.type === "error") console.error(r.error.message);
    });
  });
}
```

## Webhooks

### Critical Events

- `payment_intent.succeeded` — payment completed
- `payment_intent.payment_failed` — payment failed
- `customer.subscription.updated` — subscription changed
- `customer.subscription.deleted` — subscription canceled
- `charge.refunded` — refund processed
- `invoice.payment_succeeded` — subscription payment successful

### Verification

```python
import stripe

# In your webhook handler, use the raw body (not parsed JSON)
sig_header = request.headers.get('Stripe-Signature')
event = stripe.Webhook.construct_event(
    payload=raw_body,
    sig_header=sig_header,
    secret='whsec_...'
)

if event.type == 'payment_intent.succeeded':
    intent = event.data.object
    # Process payment
```

## Subscriptions

### Components

- **Product** — what you're selling
- **Price** — how much and how often
- **Subscription** — customer's recurring payment
- **Invoice** — generated for each billing cycle

### Creating a Subscription

```python
subscription = stripe.Subscription.create(
    customer='cus_...',
    items=[{'price': 'price_...'}],  # Price ID from Dashboard or API
)
```

## Testing

```python
# Use test mode keys
stripe.api_key = "sk_test_..."

TEST_CARDS = {
    'success': '4242424242424242',
    'declined': '4000000000000002',
    '3d_secure': '4000002500003155',
    'insufficient_funds': '4000000000009995',
}

def test_payment_flow():
    customer = stripe.Customer.create(email="test@example.com")
    intent = stripe.PaymentIntent.create(
        amount=1000,
        currency='usd',
        customer=customer.id,
        automatic_payment_methods={'enabled': True},
    )
    confirmed = stripe.PaymentIntent.confirm(
        intent.id,
        payment_method='pm_card_visa'
    )
    assert confirmed.status == 'succeeded'
```

## Setup Checklist

- [ ] Get API keys from Stripe Dashboard (test mode first)
- [ ] Set up webhook endpoint with signature verification
- [ ] Configure webhook events in Dashboard
- [ ] Implement checkout flow (Sessions recommended over Intents)
- [ ] Test all scenarios: success, failure, 3D Secure, refunds
