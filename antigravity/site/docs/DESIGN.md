# Design Document

**Project:** [BRAND NAME]
**Design goal:** Look credible and calm, read beautifully, and make two actions obvious: **subscribe** and **get in touch**.

---

## 1. Design Principles

1. **Readability first.** This is a content site; typography drives everything.
2. **One clear action per section.** Never compete two equal CTAs in the same view.
3. **Quiet confidence.** Generous whitespace, restrained color, no decoration that does not carry meaning.
4. **Mobile first.** Design at 375px, then scale up.
5. **Fast by default.** Minimal imagery weight, system-friendly fonts, no heavy animation.

## 2. Brand Direction (edit to taste)

- **Personality:** [professional yet approachable, practical, modern]
- **Voice:** clear, direct, no jargon
- **Reference feel:** editorial blog crossed with a clean SaaS landing page

## 3. Color System

Define as CSS variables / Tailwind theme tokens. Values below are a starting palette; change the accent to match the brand.

| Token | Light | Dark | Use |
|---|---|---|---|
| `--bg` | #FFFFFF | #0B0F14 | Page background |
| `--surface` | #F6F7F9 | #121821 | Cards, sections |
| `--border` | #E3E6EB | #232B36 | Dividers |
| `--text` | #0F172A | #E6EAF0 | Body text |
| `--text-muted` | #5B6472 | #9AA5B4 | Secondary text |
| `--accent` | #2563EB | #5B8CFF | Primary CTA, links |
| `--accent-hover` | #1D4ED8 | #7AA2FF | Hover |
| `--success` | #16A34A | #4ADE80 | Success states |
| `--danger` | #DC2626 | #F87171 | Errors |

Rules: text contrast at least 4.5:1; never use color alone to convey state; the accent is used sparingly.

## 4. Typography

| Role | Font | Notes |
|---|---|---|
| Headings | Inter or Plus Jakarta Sans (via `next/font`) | Weight 600-700, tight tracking |
| Body | Inter | 17-18px on desktop, 16px on mobile, line-height 1.7 |
| Code | JetBrains Mono | Only in posts |

**Scale (rem):** 0.875, 1, 1.125, 1.25, 1.5, 1.875, 2.25, 3, 3.75.
**Article measure:** 65-72 characters per line (max-width about 720px).

## 5. Layout and Spacing

- 8px spacing scale (4, 8, 12, 16, 24, 32, 48, 64, 96).
- Container: max-width 1200px; article column 720px; side padding 16px mobile, 24px tablet, 32px desktop.
- Section vertical padding: 64px mobile, 96px desktop.
- Breakpoints: 640, 768, 1024, 1280.
- Radius: 8px inputs and buttons, 16px cards.
- Shadows: subtle only; prefer borders.

## 6. Components

| Component | Behavior and notes |
|---|---|
| **Header** | Sticky, logo left, nav center or right, "Subscribe" (secondary) and "Contact" (primary) buttons; mobile drawer menu |
| **Footer** | Short brand blurb, nav, social links, newsletter mini-form, legal links |
| **Button** | Variants: primary, secondary, ghost; sizes sm/md/lg; visible focus ring; loading state |
| **Newsletter form** | Inline (email + button), states idle/loading/success/error; used in hero, post end, footer, dedicated page |
| **Post card** | Cover image (16:9), tags, title, excerpt, date and reading time; hover lifts border color, not size |
| **Tag chip** | Small pill, links to tag filter |
| **Service card** | Icon, title, outcome sentence, "Learn more" link |
| **Testimonial** | Quote, name, role; 1 to 3 columns |
| **Table of contents** | Sticky on desktop right rail; collapsible on mobile |
| **Callout** | Info/warning/tip blocks inside MDX |
| **Form fields** | Visible labels, helper text, inline error text, min 44px touch target |
| **Toast/inline alerts** | For form feedback, `aria-live` polite |

## 7. Page Wireframes (structure)

### Home
1. Hero: headline (outcome for reader), subheadline, email signup, secondary link "See services"
2. Social proof strip: logos or short stat line
3. Featured posts (3 cards) plus "All articles" link
4. Services teaser (3 cards)
5. About snippet with photo
6. Testimonials
7. Final CTA: newsletter and contact

### Services
Intro, list of services (detailed), process steps (1-2-3-4), FAQ (accordion), CTA to contact.

### Blog list
Page title, tag filter, search, post grid (1/2/3 columns), pagination.

### Blog post
Title, meta row (date, reading time, tags), cover image, body with TOC, inline newsletter callout mid-article, end-of-post signup, author box, related posts.

### About
Story, values or approach, credentials, photo, CTA.

### Contact
Two columns: form left, direct email and social right; response-time note.

### Newsletter page
What subscribers get, frequency, sample topics, signup form, privacy note.

## 8. Interaction and Motion

- Transitions 150-200ms, ease-out, on color and border only.
- Subtle fade-in on scroll for sections, disabled when `prefers-reduced-motion`.
- No autoplay, parallax or heavy animations.

## 9. Imagery and Iconography

- Icons: Lucide, 1.5px stroke.
- Photos: real photo of the owner on About; optimized WebP/AVIF via `next/image`.
- Post covers: consistent style (generated OG-style cards with title on brand background is acceptable for MVP).
- Always provide alt text.

## 10. Accessibility Checklist

- Semantic landmarks (`header`, `nav`, `main`, `footer`), one `h1` per page.
- Skip-to-content link.
- Visible focus for all interactive elements.
- Forms: labels, `aria-describedby` for errors, no placeholder-only labels.
- Color contrast meets AA in both themes.
- Full keyboard navigation for menu, accordion and forms.

## 11. Dark Mode

Supported via `prefers-color-scheme` with a manual toggle in the header; preference saved in localStorage; no flash of wrong theme on load.

## 12. Design Deliverables for the Agent

- `globals.css` / Tailwind theme with all tokens above.
- A `/styleguide` route (hidden from sitemap, `noindex`) showing colors, type, buttons, forms and cards, used for review.
