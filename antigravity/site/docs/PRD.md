# Product Requirements Document (PRD)

**Project:** [BRAND NAME] service website with blog and newsletter
**Version:** 1.0 | **Target launch:** 14 days from kickoff
**Owner:** Sourav

> Placeholders in [BRACKETS] must be filled in before or during Phase 0. The agent should ask if any are still empty when it reaches a page that needs them.

---

## 1. Overview

A fast, SEO-friendly website for a service business whose primary goal is to **build an audience** (organic readers and email subscribers) and secondarily to **generate client inquiries**.

## 2. Goals and Success Metrics (first 90 days)

| Goal | Metric | Target |
|---|---|---|
| Build audience | Newsletter subscribers | [100] |
| Attract traffic | Monthly organic visitors | [1,000] |
| Convert clients | Contact form submissions | [10] |
| Engagement | Returning visitor rate | [25%] |
| Quality | Lighthouse (mobile) Performance / SEO / Accessibility | 90+ / 100 / 95+ |

## 3. Target Audience

- **Primary reader:** [e.g. small business owners in India needing X]
- **Their problem:** [describe]
- **Where they are:** [Google search, LinkedIn, Instagram, YouTube, communities]

## 4. Service Offering

- [Service 1: name, one-line outcome]
- [Service 2]
- [Service 3]

## 5. Scope

### In scope (MVP, launch in 2 weeks)

| # | Feature | Priority |
|---|---|---|
| F1 | Home page (value proposition, featured posts, services teaser, newsletter CTA, trust section) | P0 |
| F2 | Services page (offer, process, outcomes, CTA) | P0 |
| F3 | Blog: list page with tag filter and pagination | P0 |
| F4 | Blog post page: MDX content, table of contents, reading time, related posts, share links, author box | P0 |
| F5 | Newsletter signup (header/footer, inline in posts, dedicated /newsletter page), double opt-in | P0 |
| F6 | Contact form with validation, spam protection and email notification | P0 |
| F7 | About page | P0 |
| F8 | SEO: metadata, Open Graph images, sitemap.xml, robots.txt, JSON-LD, RSS feed | P0 |
| F9 | Analytics (privacy-friendly) and Search Console verification | P0 |
| F10 | Legal pages: Privacy Policy, Terms | P0 |
| F11 | Custom 404 page, favicon, responsive layout, dark mode | P1 |
| F12 | Site search across posts (client-side) | P1 |
| F13 | Testimonials section with placeholder data | P1 |

### Out of scope for MVP (backlog)

User accounts, payments, comments, admin CMS UI, multi-language, client portal, booking calendar integration, lead-magnet gated downloads (planned for week 3+).

## 6. Functional Requirements

### 6.1 Blog
- Posts are MDX files in `content/posts/` with frontmatter: `title`, `description`, `date`, `updated`, `tags[]`, `cover`, `draft`, `author`.
- Draft posts are excluded from production builds, lists, sitemap and RSS.
- Auto-generated reading time, heading anchors and table of contents.
- Syntax-highlighted code blocks.
- Related posts by shared tags.
- Ship with 3 sample posts so the layout can be reviewed.

### 6.2 Newsletter
- Email field with client and server validation.
- Server route calls the newsletter provider API; the API key never reaches the browser.
- States: idle, loading, success ("check your inbox to confirm"), error, already subscribed.
- Honeypot field plus rate limiting.
- Same component reused in five placements.

### 6.3 Contact form
- Fields: name, email, service interest (select), message, optional budget range.
- Zod validation shared by client and server.
- Cloudflare Turnstile plus honeypot.
- Sends an email to the owner and an auto-reply to the sender.
- Accessible error and success messages.

### 6.4 SEO
- Per-page `generateMetadata`; canonical URLs; Open Graph and Twitter cards with dynamic OG images for posts.
- JSON-LD: Organization, WebSite, Article, BreadcrumbList.
- `sitemap.xml`, `robots.txt`, `/rss.xml`.

## 7. Non-Functional Requirements

| Area | Requirement |
|---|---|
| Performance | LCP under 2.5s on mobile; CLS under 0.1; minimal client JS |
| Accessibility | WCAG 2.1 AA: keyboard navigation, focus states, contrast, alt text, semantic HTML |
| Security | Secrets in env vars only; input validation; rate limiting; security headers |
| Privacy | No third-party tracking cookies; privacy policy covers form and newsletter data |
| Browser support | Latest two versions of Chrome, Safari, Firefox, Edge; mobile Safari and Chrome |
| Maintainability | TypeScript strict mode; lint and format on commit; README with setup steps |

## 8. Content Requirements

- Launch with 5-6 articles across 2-3 topic clusters: [Topic A], [Topic B], [Topic C].
- The agent creates structure, layouts and 3 sample posts. The owner writes the real articles.
- Tone of voice: [friendly-expert / direct / technical].

## 9. Acceptance Criteria (launch gate)

- All P0 features work on mobile and desktop.
- Newsletter signup and contact form work end to end in production.
- Lighthouse targets met on Home, a blog post and Services.
- No console errors; no broken links; sitemap and robots valid.
- Analytics receiving data; site verified in Search Console.
- Legal pages published.

## 10. Timeline

| Days | Deliverable |
|---|---|
| 1-2 | Setup, design tokens, layout, navigation |
| 3-4 | Home, Services, About |
| 5-6 | Blog engine and post template |
| 7 | Newsletter and contact form |
| 8-9 | SEO, RSS, OG images, search |
| 10-11 | Real content, polish, accessibility, performance |
| 12-13 | QA and fixes |
| 14 | Deploy and launch |

## 11. Risks

| Risk | Mitigation |
|---|---|
| Scope creep | MVP list above is frozen; new ideas go to backlog |
| Content not ready | Write articles in parallel with build |
| Form spam | Turnstile, honeypot, rate limit |
| Low early traffic | Distribution plan (network, communities, social) alongside SEO |

## 12. Open Questions

- [Brand name and domain?]
- [Newsletter provider final choice?]
- [Exact services and pricing display?]
- [Preferred contact email and social links?]
