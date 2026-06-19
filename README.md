# Pinnacle Designs

Marketing website for Pinnacle Designs — web design and Website-as-a-Service (WaaS) for small businesses in Erwin, TN and the Tri-Cities area.

## Run locally

Open `index.html` in a browser, or use a simple local server:

```bash
npx serve .
```

## Structure

- `index.html` — single-page site (hero, about, pricing, WaaS comparison, service area, contact)
- `styles.css` — black background, logo-matched blue palette
- `main.js` — mobile nav, back-to-top, and Formspree contact form handler
- `assets/logo.png` — brand logo
- `robots.txt` / `sitemap.xml` — search engine crawling

## Google Analytics

The site uses measurement ID `G-Y3XVJXG5KW` in `index.html`.

This domain is on **Cloudflare**. For best detection and ad-blocker resilience, enable **[Google Tag Gateway](https://developers.cloudflare.com/google-tag-gateway/)**:

1. **Dashboard (easiest):** Cloudflare → **Google Tag Gateway** → select `pinnacle-designs.com` → enable → ID `G-Y3XVJXG5KW` → path `/metrics` → Save
2. **API:** run `scripts/configure-cloudflare-gtag-gateway.ps1` with a `CLOUDFLARE_API_TOKEN` that has Zone:Edit

After gateway is on, Cloudflare proxies tag requests through your domain (`pinnacle-designs.com/metrics/...`). Confirm in GA4 **Reports → Realtime**.

## Customize

The contact form posts to [Formspree](https://formspree.io) at `https://formspree.io/f/xojbzjog`. Submissions are managed in your Formspree dashboard.
