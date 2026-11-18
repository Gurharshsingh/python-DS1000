# Decisions Log

Decisions made where the source documents had placeholders or ambiguity.

---

## D1: Brand Name
- **Placeholder:** `[BRAND NAME]`
- **Decision:** Using **"Meridian"** as the working brand name. Tagline: "Strategy & Growth Consultancy".
- **Rationale:** Generic professional name that works for a service business. Easy to find-and-replace later.

## D2: Services
- **Placeholder:** `[Service 1], [Service 2], [Service 3]`
- **Decision:** Three placeholder services:
  1. **Growth Strategy** — Data-driven plans to scale your business sustainably.
  2. **Digital Presence** — Websites, SEO and content that attract the right audience.
  3. **Brand Positioning** — Clarify your message so customers choose you first.
- **Rationale:** Realistic consultancy services that fit the "service business" model. Owner will replace with real offerings.

## D3: Target Audience
- **Placeholder:** `[e.g. small business owners in India needing X]`
- **Decision:** "Founders and small business owners looking to grow their online presence and attract clients through content and strategy."
- **Rationale:** Broad enough for placeholder copy; owner will narrow down.

## D4: Tone of Voice
- **Placeholder:** `[friendly-expert / direct / technical]`
- **Decision:** **Friendly-expert** — professional but approachable, no jargon, practical.
- **Rationale:** Best fit for a consultancy targeting SMBs.

## D5: Content Topics
- **Placeholder:** `[Topic A], [Topic B], [Topic C]`
- **Decision:** Sample posts will cover: Growth Strategy, Content Marketing, Business Tools.
- **Rationale:** Aligns with the service offerings.

## D6: Heading Font
- **Docs say:** "Inter or Plus Jakarta Sans"
- **Decision:** Using **Plus Jakarta Sans** for headings, **Inter** for body.
- **Rationale:** Provides visual distinction between headings and body while staying within the approved options.

## D7: Newsletter Provider
- **Placeholder:** `[Newsletter provider final choice?]`
- **Decision:** **Buttondown** as specified in TECH_STACK. Code will degrade gracefully when API key is missing.

## D8: Contact Email and Socials
- **Placeholder:** `[Preferred contact email and social links?]`
- **Decision:** Using placeholder values in `site-config.ts` marked with `TODO` comments. Social links: Twitter/X, LinkedIn, GitHub.

## D9: MDX Processing
- **Docs say:** "`next-mdx-remote` or `@next/mdx`"
- **Decision:** Using **next-mdx-remote/rsc** for RSC-compatible MDX rendering.
- **Rationale:** Better suited for file-system based content loading in App Router with Server Components.
