---
name: "notifications"
description: "Defines admin alerts and user notifications across Telegram and email. Invoke when adding failure alerts, transactional emails, or event-driven notifications."
---

# Notifications

Use this skill when the system needs to notify admins or end users.

## Channel Strategy
- Use Telegram for operator/dev alerts: failed jobs, broken webhooks, stuck workers, payment anomalies.
- Use email providers such as Resend or Postmark for user-facing transactional events.
- Keep notification sending behind a small service layer so business code stays clean.

## Admin Alerts
Telegram is a strong default for fast operational alerts.

Recommended uses:
- Worker/job failures after retries exhausted
- Payment webhook verification failures
- Unexpected exceptions in scheduled tasks
- Security-relevant events worth immediate visibility

Example payload shape:

```python
message = (
    "Job failed\n"
    f"job_id={job.id}\n"
    f"type={job.type}\n"
    f"error={job.error_message}"
)
```

## User Notifications
Use email for:
- Payment receipts
- Magic links or auth confirmations
- Long-running job completion
- Invoice and subscription lifecycle events

Rules:
- Use provider templates when possible.
- Keep email content localized if the product is localized.
- Never block critical request paths on email delivery; queue when appropriate.

## Delivery Design
- Centralize message formatting.
- Make notification sends idempotent when repeated events are possible.
- Log notification attempts and provider response IDs.
- Separate retryable provider failures from permanent validation errors.

## Checklist
- [ ] Pick the right channel: Telegram for ops, email for users
- [ ] Add env vars for tokens, chat IDs, sender domains, and API keys
- [ ] Wrap provider calls in a dedicated service
- [ ] Log provider response IDs and failures
- [ ] Make sends safe to retry for repeated events
