"""Generate Pinnacle Designs pitch deck PDF (16:9 slide format)."""

from __future__ import annotations

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "pitch-deck" / "pinnacle-designs-pitch-deck.pdf"
LOGO = ROOT / "assets" / "logo.png"

PAGE_W = 13.333 * inch
PAGE_H = 7.5 * inch

BLACK = colors.HexColor("#000000")
BG_CARD = colors.HexColor("#0f1018")
BG_ELEVATED = colors.HexColor("#0a0a0f")
WHITE = colors.HexColor("#ffffff")
MUTED = colors.HexColor("#a1a1aa")
ACCENT = colors.HexColor("#3b82f6")
ACCENT_BRIGHT = colors.HexColor("#60a5fa")
ACCENT_DEEP = colors.HexColor("#2563eb")
PERIWINKLE = colors.HexColor("#818cf8")


def new_page(c: canvas.Canvas) -> None:
    c.setPageSize((PAGE_W, PAGE_H))
    c.setFillColor(BLACK)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)


def accent_bar(c: canvas.Canvas, bottom: bool = False) -> None:
    h = 0.35 * inch
    y = 0 if not bottom else PAGE_H - h
    c.setFillColor(ACCENT_DEEP)
    c.rect(0, y, PAGE_W, h, fill=1, stroke=0)


def footer(c: canvas.Canvas, text: str = "pinnacle-designs.com") -> None:
    if not text:
        return
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 9)
    c.drawRightString(PAGE_W - 0.5 * inch, 0.45 * inch, text)


def label(c: canvas.Canvas, text: str) -> None:
    c.setFillColor(ACCENT_BRIGHT)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(0.75 * inch, PAGE_H - 0.65 * inch, text.upper())


def title(c: canvas.Canvas, text: str, size: int = 28, y: float | None = None) -> None:
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", size)
    ty = y if y is not None else PAGE_H - 1.15 * inch
    c.drawString(0.75 * inch, ty, text)


def wrap_text(
    c: canvas.Canvas,
    text: str,
    x: float,
    y: float,
    width: float,
    style: ParagraphStyle,
) -> float:
    p = Paragraph(text, style)
    w, h = p.wrap(width, PAGE_H)
    p.drawOn(c, x, y - h)
    return y - h


def bullet_block(
    c: canvas.Canvas,
    items: list[str],
    y_start: float,
    width: float = 11.5 * inch,
    size: int = 13,
) -> None:
    style = ParagraphStyle(
        "bullet",
        fontName="Helvetica",
        fontSize=size,
        leading=size + 6,
        textColor=MUTED,
        leftIndent=14,
        bulletIndent=0,
        spaceAfter=8,
    )
    y = y_start
    for item in items:
        y = wrap_text(c, f"• {item}", 0.75 * inch, y, width, style)


def draw_card(
    c: canvas.Canvas,
    x: float,
    y: float,
    w: float,
    h: float,
    border: colors.Color = colors.HexColor("#3c3c46"),
) -> None:
    c.setFillColor(BG_CARD)
    c.setStrokeColor(border)
    c.setLineWidth(1)
    c.roundRect(x, y, w, h, 6, fill=1, stroke=1)


def build_pdf() -> Path:
    c = canvas.Canvas(str(OUT), pagesize=(PAGE_W, PAGE_H))
    styles = getSampleStyleSheet()
    body_white = ParagraphStyle(
        "bodyw",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=14,
        leading=20,
        textColor=WHITE,
    )
    body_muted = ParagraphStyle(
        "bodym",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=13,
        leading=18,
        textColor=MUTED,
    )
    center_muted = ParagraphStyle(
        "centerm",
        parent=body_muted,
        alignment=TA_CENTER,
        fontSize=12,
    )

    # Slide 1 — Title
    new_page(c)
    accent_bar(c, bottom=True)
    if LOGO.exists():
        logo_w = 4.5 * inch
        logo_h = logo_w * (397 / 560)
        c.drawImage(
            str(LOGO),
            (PAGE_W - logo_w) / 2,
            PAGE_H - logo_h - 1.4 * inch,
            width=logo_w,
            height=logo_h,
            mask="auto",
        )
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 12)
    tag = "WEB DESIGN. "
    tw = c.stringWidth(tag, "Helvetica-Bold", 12)
    accent_w = c.stringWidth("ELEVATED.", "Helvetica-Bold", 12)
    tx = (PAGE_W - tw - accent_w) / 2
    c.drawString(tx, PAGE_H - 5.1 * inch, tag)
    c.setFillColor(ACCENT_BRIGHT)
    c.drawString(tx + tw, PAGE_H - 5.1 * inch, "ELEVATED.")
    wrap_text(
        c,
        "Website-as-a-Service &amp; industry management software<br/>for East Tennessee small businesses",
        0.75 * inch,
        PAGE_H - 5.65 * inch,
        PAGE_W - 1.5 * inch,
        center_muted,
    )
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 10)
    c.drawCentredString(PAGE_W / 2, 0.9 * inch, "Erwin, TN · Tri-Cities · 2026")
    c.showPage()

    # Slide 2 — Problem
    new_page(c)
    accent_bar(c)
    label(c, "The Problem")
    title(c, "Local businesses are losing customers online")
    bullet_block(
        c,
        [
            "Many shops rely only on Facebook — no owned digital storefront",
            "Outdated websites hurt credibility and fail on mobile",
            "Traditional agencies charge $3,000–$10,000+ upfront",
            "Owners are left to update hosting, security, and content themselves",
            "Generic software stacks don't fit how local industries actually operate",
        ],
        PAGE_H - 2.0 * inch,
    )
    footer(c)
    c.showPage()

    # Slide 3 — Opportunity
    new_page(c)
    accent_bar(c)
    label(c, "Market Opportunity")
    title(c, "East Tennessee's underserved small-business market", size=24)
    bullet_block(
        c,
        [
            "Target: plumbers, HVAC, roofers, restaurants, boutiques, and professional services",
            "Service area: Erwin, Unicoi County, Johnson City, Jonesborough, Kingsport",
            "High-intent local search: web design Erwin TN, affordable web developer Johnson City",
            "WaaS model lowers barrier to entry and creates predictable recurring revenue",
            "Expansion path: industry-specific management software beyond websites",
        ],
        PAGE_H - 2.0 * inch,
        size=12,
    )
    footer(c)
    c.showPage()

    # Slide 4 — Solution
    new_page(c)
    accent_bar(c)
    label(c, "Our Solution")
    title(c, "Website-as-a-Service (WaaS)", size=26)
    wrap_text(
        c,
        "Pinnacle Designs builds conversion-focused websites for local businesses — then acts as the outsourced webmaster: hosting, SSL, security, SEO, and done-for-you updates every month.",
        0.75 * inch,
        PAGE_H - 2.05 * inch,
        11.5 * inch,
        body_white,
    )
    bullet_block(
        c,
        [
            "Small down payment + flat monthly subscription",
            "Text us when prices or photos change — we handle the rest",
            "Continuous maintenance so sites never go stale in ~2 years",
            "Zero tech headaches for the business owner",
        ],
        PAGE_H - 3.35 * inch,
    )
    footer(c)
    c.showPage()

    # Slide 5 — Compare
    new_page(c)
    accent_bar(c)
    label(c, "Why Pinnacle")
    title(c, "The old way vs. the Pinnacle way", size=24)
    col_w = 5.6 * inch
    col_h = 4.2 * inch
    y0 = 1.35 * inch
    draw_card(c, 0.75 * inch, y0, col_w, col_h, colors.HexColor("#505058"))
    draw_card(c, 6.95 * inch, y0, col_w, col_h, ACCENT)
    c.setFillColor(MUTED)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(1.0 * inch, y0 + col_h - 0.45 * inch, "Traditional Agencies")
    c.setFillColor(ACCENT_BRIGHT)
    c.drawString(7.2 * inch, y0 + col_h - 0.45 * inch, "Pinnacle Designs")
    old_items = [
        "Huge $3,000+ upfront cost",
        "You update the site yourself",
        "Pay extra for hosting & security",
        "Site goes out of date in ~2 years",
    ]
    new_items = [
        "Affordable down payment from $500",
        "We make updates for you",
        "Hosting & security included",
        "Continuously maintained & modern",
    ]
    c.setFont("Helvetica", 11)
    oy = y0 + col_h - 0.85 * inch
    for item in old_items:
        c.setFillColor(MUTED)
        c.drawString(1.0 * inch, oy, f"✗  {item}")
        oy -= 0.38 * inch
    oy = y0 + col_h - 0.85 * inch
    for item in new_items:
        c.setFillColor(WHITE)
        c.drawString(7.2 * inch, oy, f"✓  {item}")
        oy -= 0.38 * inch
    footer(c)
    c.showPage()

    # Slide 6 — Pricing
    new_page(c)
    accent_bar(c)
    label(c, "Services & Pricing")
    title(c, "Three plans. One simple model.", size=24)
    plans = [
        ("Base Camp", "New businesses & contractors", "$500", "$99", ["3–5 page site", "Basic SEO", "Hosting & SSL", "1 hr/mo updates"], False),
        ("Ascent", "Established local shops", "$1,000", "$199", ["Up to 10 pages", "Google Business Profile", "Analytics", "2 hrs/mo updates"], True),
        ("Summit", "Retailers selling online", "$2,500+", "$299+", ["Full store setup", "Payment gateways", "Priority support", "Catalog updates"], False),
    ]
    card_w = 3.75 * inch
    card_h = 4.4 * inch
    for i, (tier, aud, down, mo, feats, featured) in enumerate(plans):
        x = 0.75 * inch + i * (card_w + 0.25 * inch)
        y = 1.45 * inch
        c.setFillColor(BG_ELEVATED if featured else BG_CARD)
        c.setStrokeColor(ACCENT if featured else colors.HexColor("#3c3c46"))
        c.setLineWidth(2 if featured else 1)
        c.roundRect(x, y, card_w, card_h, 6, fill=1, stroke=1)
        c.setFillColor(ACCENT_BRIGHT if featured else WHITE)
        c.setFont("Helvetica-Bold", 14)
        c.drawString(x + 0.2 * inch, y + card_h - 0.4 * inch, tier)
        c.setFillColor(MUTED)
        c.setFont("Helvetica", 9)
        c.drawString(x + 0.2 * inch, y + card_h - 0.65 * inch, aud)
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 15)
        c.drawString(x + 0.2 * inch, y + card_h - 1.0 * inch, f"{down} down")
        c.setFont("Helvetica-Bold", 12)
        c.drawString(x + 0.2 * inch, y + card_h - 1.3 * inch, f"+ {mo}/mo")
        fy = y + card_h - 1.65 * inch
        c.setFont("Helvetica", 9)
        c.setFillColor(MUTED)
        for f in feats:
            c.drawString(x + 0.2 * inch, fy, f"• {f}")
            fy -= 0.28 * inch
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 9)
    c.drawString(0.75 * inch, 0.75 * inch, "Design fee + monthly retainer. Larger add-ons quoted separately in contract.")
    footer(c)
    c.showPage()

    # Slide 7 — Outcomes
    new_page(c)
    accent_bar(c)
    label(c, "Client Outcomes")
    title(c, "What clients get", size=26)
    outcomes = [
        ("Never worry about hacks", "Security scanning and managed hosting."),
        ("Show up locally", "Mobile-friendly design and SEO for the Tri-Cities."),
        ("Unlimited peace of mind", "Monthly updates keep content current."),
    ]
    for i, (head, body) in enumerate(outcomes):
        x = 0.75 * inch + i * 4.05 * inch
        y = 1.55 * inch
        draw_card(c, x, y, 3.75 * inch, 2.6 * inch, ACCENT)
        c.setFillColor(ACCENT_BRIGHT)
        c.setFont("Helvetica", 10)
        c.drawString(x + 0.2 * inch, y + 2.2 * inch, "◆")
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 12)
        c.drawString(x + 0.2 * inch, y + 1.85 * inch, head)
        wrap_text(c, body, x + 0.2 * inch, y + 1.55 * inch, 3.35 * inch, body_muted)
    c.setFillColor(BG_ELEVATED)
    c.setStrokeColor(PERIWINKLE)
    c.roundRect(0.75 * inch, 0.85 * inch, 11.85 * inch, 0.65 * inch, 6, fill=1, stroke=1)
    c.setFillColor(WHITE)
    c.setFont("Helvetica", 11)
    c.drawCentredString(
        PAGE_W / 2,
        1.05 * inch,
        "If you don't love the design we present, you don't pay the down payment. Zero risk to get started.",
    )
    footer(c)
    c.showPage()

    # Slide 8 — Software
    new_page(c)
    accent_bar(c)
    label(c, "Growth — Management Software")
    title(c, "Beyond websites: tools built per industry", size=22)
    wrap_text(
        c,
        "In active development — industry-specific management software so local businesses handle jobs, customers, and operations without juggling a dozen apps.",
        0.75 * inch,
        PAGE_H - 2.0 * inch,
        11.5 * inch,
        body_muted,
    )
    verticals = [
        ("Home Services", "Scheduling, customer records, follow-ups"),
        ("Retail & Boutiques", "Inventory, customers, sales tracking"),
        ("Restaurants", "Menus, order flow, staff coordination"),
        ("Professional Services", "Intake, booking, project tracking"),
    ]
    for i, (name, desc) in enumerate(verticals):
        col = i % 2
        row = i // 2
        x = 0.75 * inch + col * 6.1 * inch
        y = PAGE_H - 3.0 * inch - row * 1.55 * inch
        draw_card(c, x, y - 1.2 * inch, 5.6 * inch, 1.2 * inch)
        c.setFillColor(ACCENT_BRIGHT)
        c.setFont("Helvetica-Bold", 12)
        c.drawString(x + 0.2 * inch, y - 0.45 * inch, name)
        c.setFillColor(MUTED)
        c.setFont("Helvetica", 10)
        c.drawString(x + 0.2 * inch, y - 0.75 * inch, desc)
    c.setFillColor(ACCENT_BRIGHT)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(0.75 * inch, 0.75 * inch, "IN DEVELOPMENT — Early access waitlist open")
    footer(c)
    c.showPage()

    # Slide 9 — Business model
    new_page(c)
    accent_bar(c)
    label(c, "Business Model")
    title(c, "Predictable revenue, low client friction", size=24)
    bullet_block(
        c,
        [
            "Revenue stream 1: One-time design & setup fees ($500 – $2,500+)",
            "Revenue stream 2: Recurring monthly management ($99 – $299+/mo)",
            "Revenue stream 3: Out-of-scope projects (new pages, integrations, e-commerce add-ons)",
            "Revenue stream 4 (future): Management software subscriptions by vertical",
            "Low CAC: Local SEO, referrals, Facebook, and Tri-Cities networking",
            "High retention: Ongoing updates create sticky, long-term client relationships",
        ],
        PAGE_H - 2.0 * inch,
        size=12,
    )
    footer(c)
    c.showPage()

    # Slide 10 — Traction
    new_page(c)
    accent_bar(c)
    label(c, "Traction & Readiness")
    title(c, "Built to scale locally", size=26)
    stats = [("$500", "Starting down payment"), ("24/7", "Digital storefront"), ("0", "Tech headaches")]
    for i, (val, lbl) in enumerate(stats):
        x = 0.75 * inch + i * 4.05 * inch
        y = 2.2 * inch
        c.setFillColor(BG_ELEVATED)
        c.setStrokeColor(ACCENT)
        c.roundRect(x, y, 3.75 * inch, 1.7 * inch, 6, fill=1, stroke=1)
        c.setFillColor(ACCENT_BRIGHT)
        c.setFont("Helvetica-Bold", 28)
        c.drawCentredString(x + 1.875 * inch, y + 1.05 * inch, val)
        c.setFillColor(MUTED)
        c.setFont("Helvetica", 10)
        c.drawCentredString(x + 1.875 * inch, y + 0.55 * inch, lbl)
    bullet_block(
        c,
        [
            "Live brand & marketing site at pinnacle-designs.com",
            "Contract templates ready for Base Camp, Ascent, Summit, and software beta",
            "Formspree contact pipeline and Google Analytics in place",
            "Cloudflare-hosted with SEO, FAQ schema, and local landing content",
        ],
        PAGE_H - 2.85 * inch,
        size=12,
    )
    footer(c)
    c.showPage()

    # Slide 11 — Ask
    new_page(c)
    accent_bar(c)
    label(c, "The Ask")
    title(c, "Partner with Pinnacle Designs", size=26)
    bullet_block(
        c,
        [
            "For clients: Start with a free conversation — pick Base Camp, Ascent, or Summit",
            "For software beta: Request early access for your industry vertical",
            "For partners & investors: Let's talk about scaling WaaS and software across East TN",
        ],
        PAGE_H - 2.1 * inch,
        size=13,
    )
    c.setFillColor(BG_ELEVATED)
    c.setStrokeColor(ACCENT)
    c.roundRect(0.75 * inch, 1.55 * inch, 11.85 * inch, 1.75 * inch, 6, fill=1, stroke=1)
    c.setFillColor(ACCENT_BRIGHT)
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(PAGE_W / 2, 2.75 * inch, "david@pinnacle-designs.com")
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 13)
    c.drawCentredString(PAGE_W / 2, 2.35 * inch, "pinnacle-designs.com")
    c.drawCentredString(PAGE_W / 2, 1.95 * inch, "facebook.com/profile.php?id=61590691171007")
    if LOGO.exists():
        lw = 2.0 * inch
        lh = lw * (397 / 560)
        c.drawImage(str(LOGO), (PAGE_W - lw) / 2, 0.55 * inch, width=lw, height=lh, mask="auto")
    c.showPage()

    OUT.parent.mkdir(parents=True, exist_ok=True)
    c.save()
    return OUT


if __name__ == "__main__":
    path = build_pdf()
    print(f"Created {path}")
