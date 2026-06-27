# PayPal Integration Guide

Universal guide for integrating payments via PayPal. Supports express checkout, subscriptions, and payouts.

## Environment Variables

```
PAYPAL_CLIENT_ID       # Your PayPal client ID
PAYPAL_CLIENT_SECRET   # Your PayPal client secret
PAYPAL_MODE            # 'sandbox' or 'live'
```

## Quick Start — Smart Buttons

```html
<!-- Frontend -->
<div id="paypal-button-container"></div>

<script src="https://www.paypal.com/sdk/js?client-id=YOUR_CLIENT_ID&currency=USD"></script>
<script>
  paypal.Buttons({
    createOrder: function(data, actions) {
      return fetch('/api/paypal/create-order', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
      }).then(res => res.json()).then(data => data.orderID);
    },
    onApprove: function(data, actions) {
      return fetch('/api/paypal/capture-order', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({orderID: data.orderID}),
      }).then(res => res.json()).then(orderData => {
        // Payment successful
        console.log('Captured:', orderData);
      });
    }
  }).render('#paypal-button-container');
</script>
```

## Server-Side Order Management

```python
import requests

class PayPalClient:
    def __init__(self, client_id, client_secret, mode='sandbox'):
        self.client_id = client_id
        self.client_secret = client_secret
        self.base_url = 'https://api-m.sandbox.paypal.com' if mode == 'sandbox' else 'https://api-m.paypal.com'
        self.access_token = self._get_access_token()

    def _get_access_token(self):
        url = f"{self.base_url}/v1/oauth2/token"
        response = requests.post(
            url,
            headers={"Accept": "application/json", "Accept-Language": "en_US"},
            data={"grant_type": "client_credentials"},
            auth=(self.client_id, self.client_secret),
        )
        return response.json()['access_token']

    def _headers(self):
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.access_token}",
        }

    def create_order(self, amount, currency='USD'):
        payload = {
            "intent": "CAPTURE",
            "purchase_units": [{
                "amount": {"currency_code": currency, "value": str(amount)}
            }]
        }
        res = requests.post(f"{self.base_url}/v2/checkout/orders", headers=self._headers(), json=payload)
        return res.json()

    def capture_order(self, order_id):
        res = requests.post(
            f"{self.base_url}/v2/checkout/orders/{order_id}/capture",
            headers=self._headers(),
        )
        return res.json()

    def get_order(self, order_id):
        res = requests.get(f"{self.base_url}/v2/checkout/orders/{order_id}", headers=self._headers())
        return res.json()
```

## Webhooks (IPN)

PayPal uses webhooks instead of legacy IPN. Set up webhook URLs in your PayPal Dashboard.

### Key Events

- `PAYMENT.CAPTURE.COMPLETED` — payment captured
- `PAYMENT.CAPTURE.DENIED` — payment denied
- `PAYMENT.CAPTURE.REFUNDED` — refund processed
- `BILLING.SUBSCRIPTION.CREATED` — subscription created
- `BILLING.SUBSCRIPTION.CANCELLED` — subscription canceled

### Verification

Always verify webhook events by calling the PayPal Orders API to confirm the status:

```python
# After receiving a webhook, verify the order/capture status via API
def verify_paypal_payment(client, order_id):
    order = client.get_order(order_id)
    # Check order.status and capture details
    return order
```

## Subscriptions

### Creating a Subscription Plan

```python
plan_payload = {
    "product_id": "PROD-...",
    "name": "Monthly Plan",
    "status": "ACTIVE",
    "billing_cycles": [{
        "frequency": {"interval_unit": "MONTH", "interval_count": 1},
        "tenure_type": "REGULAR",
        "sequence": 1,
        "total_cycles": 0,  # 0 = infinite
        "pricing_scheme": {
            "fixed_price": [{"value": "25.00", "currency_code": "USD"}]
        }
    }]
}

res = requests.post(
    f"{client.base_url}/v1/billing/plans",
    headers=client._headers(), json=plan_payload
)
```

## Testing

- Use sandbox credentials
- Create test buyer and seller accounts at developer.paypal.com
- Sandbox supports all payment flows including approvals and captures

## Setup Checklist

- [ ] Get Client ID and Secret from PayPal Developer Dashboard
- [ ] Configure webhook URL in Dashboard, select events
- [ ] Set environment variables (sandbox first)
- [ ] Implement order creation + capture flow
- [ ] Implement webhook handling with API verification
- [ ] Test full flow: create → approve → capture
