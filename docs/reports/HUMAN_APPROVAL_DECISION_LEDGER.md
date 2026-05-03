# Human Approval Decision Ledger

Default state: **closed until human yes**.

This launch package can be finalized and prepared autonomously, but external actions stay closed while the operator is asleep.

## Decision slots

- `approve_public_posting` — approve exact public release/social/newsletter copy and destinations.
- `approve_video_recording_upload` — approve exact recording/upload destination and media rights.
- `approve_payment_or_offer` — approve price, payment platform, and support/refund terms.
- `approve_gpu_video_private_media` — approve budget/time/input/output for GPU/video/private-media work.
- `approve_outreach` — approve recipients, exact message, and send window.

## Closed without approval

No autonomous job may post publicly, send outreach, create payment links, record/upload private media, start GPU/video/Matrix jobs, expose secrets, or create recursive cron jobs.

## Manual wake-up template

- Decision:
- Approved lane:
- Exact copy/media/input:
- Destination:
- Budget/time cap if any:
- Stop condition:
