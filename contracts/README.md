# Contract Templates

Fill-in templates for Pinnacle Designs client agreements. Each file uses bracket placeholders (e.g. `[CLIENT LEGAL NAME]`) — replace them before sending for signature.

| Template | Service |
|----------|---------|
| [base-camp-website-agreement.docx](./base-camp-website-agreement.docx) | Base Camp — $500 down + $99/mo |
| [ascent-website-agreement.docx](./ascent-website-agreement.docx) | Ascent — $1,000 down + $199/mo |
| [summit-website-agreement.docx](./summit-website-agreement.docx) | Summit — $2,500+ down + $299+/mo |
| [management-software-early-access-agreement.docx](./management-software-early-access-agreement.docx) | Industry management software — early access |

Markdown sources (`.md`) are kept in sync for editing. After changing a `.md` file, regenerate Word docs:

```bash
python scripts/md-to-docx.py
```

## How to use

1. Open the `.docx` for the plan the client selected (or copy the markdown and regenerate).
2. Replace every `[PLACEHOLDER]` with client-specific details.
3. For **Summit** and **software** plans, complete the custom-pricing or industry-specific sections.
4. Send for e-signature or print for wet signature.
5. Keep a signed copy on file; note the **Agreement ID** in your project tracker.

## Not legal advice

These templates are starting points for your business. Have a licensed attorney in Tennessee review them before regular use, especially payment, termination, and liability sections.
