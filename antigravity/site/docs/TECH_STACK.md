# Tech Stack

**Principle:** the smallest stack that delivers a fast, SEO-strong content site plus two forms, and can grow later without a rewrite. Use the latest stable versions of everything and pin them in `package.json`.

---

## 1. Core

| Layer | Choice | Reason |
|---|---|---|
| Framework | **Next.js (App Router)** | SSG/ISR for SEO and speed; Route Handlers for forms; you already know it |
| Language | **TypeScript (strict)** | Catches errors early, better agent output |
| Styling | **Tailwind CSS** | Fast to build, tokens map to the design doc |
| UI primitives | **shadcn/ui (Radix)** | Accessible components you own, no lock-in |
| Icons | **lucide-react** | Consistent, tree-shakeable |
| Fonts | **next/font** (Inter, JetBrains Mono) | Self-hosted, no layout shift |
| Theming | **next-themes** | Dark mode without flash |

## 2. Content

| Need | Choice |
|---|---|
| Posts | MDX files in `content/posts/` |
| Parsing | `gray-matter` (frontmatter) plus `next-mdx-remote` or `@next/mdx` |
| MDX plugins | `remark-gfm`, `rehype-slug`, `rehype-autolink-headings`, `rehype-pretty-code` (Shiki) |
| Reading time | `reading-time` |
| Search | Client-side using `fuse.js` over a build-time JSON index |
| RSS | Generated in a Route Handler (`/rss.xml`) |

Why not a CMS at launch: Git-based content removes a database, a login and a cost. A headless CMS (Sanity, Payload) can be added later without changing the frontend much.

## 3. Forms and Email

| Need | Choice |
|---|---|
| Validation | **Zod** (shared client and server schemas) |
| Form state | **react-hook-form** with `@hookform/resolvers` |
| Server logic | Next.js Route Handlers or Server Actions |
| Transactional email | **Resend** (contact notification and auto-reply) |
| Newsletter | **Buttondown** (simple API, double opt-in, RSS-to-email); alternatives: Brevo, Mailchimp |
| Spam protection | **Cloudflare Turnstile** plus honeypot field |
| Rate limiting | Upstash Redis (`@upstash/ratelimit`) or an in-memory fallback for development |

## 4. SEO and Analytics

| Need | Choice |
|---|---|
| Metadata | Next.js Metadata API |
| OG images | `next/og` (`ImageResponse`) |
| Structured data | JSON-LD via a small helper component |
| Sitemap / robots | `app/sitemap.ts`, `app/robots.ts` |
| Analytics | **Plausible** (or GA4 if preferred) |
| Search visibility | Google Search Console and Bing Webmaster Tools |

## 5. Quality and Tooling

| Need | Choice |
|---|---|
| Lint / format | ESLint and Prettier (or Biome) |
| Git hooks | Husky and lint-staged |
| Unit tests | Vitest for utilities and schemas |
| E2E tests | Playwright for smoke tests (home, blog, forms) |
| Performance | Lighthouse CI or manual Lighthouse runs |
| Package manager | pnpm |

## 6. Hosting and Infrastructure

| Need | Choice |
|---|---|
| Hosting | **Vercel** (free tier is enough at launch) |
| Domain / DNS | Registrar of choice; Cloudflare DNS optional |
| Environments | `development`, `preview` (per PR), `production` |
| Uptime monitoring | UptimeRobot (free) |
| Error tracking (optional) | Sentry free tier |

## 7. Environment Variables

Provide `.env.example`; never commit `.env.local`.

```
NEXT_PUBLIC_SITE_URL=
NEXT_PUBLIC_TURNSTILE_SITE_KEY=
TURNSTILE_SECRET_KEY=
RESEND_API_KEY=
CONTACT_TO_EMAIL=
CONTACT_FROM_EMAIL=
BUTTONDOWN_API_KEY=
UPSTASH_REDIS_REST_URL=
UPSTASH_REDIS_REST_TOKEN=
NEXT_PUBLIC_PLAUSIBLE_DOMAIN=
```

## 8. Project Structure

```
.
├── app/
│   ├── (site)/
│   │   ├── page.tsx                 # Home
│   │   ├── services/page.tsx
│   │   ├── about/page.tsx
│   │   ├── contact/page.tsx
│   │   ├── newsletter/page.tsx
│   │   ├── blog/page.tsx
│   │   ├── blog/[slug]/page.tsx
│   │   ├── blog/tag/[tag]/page.tsx
│   │   ├── privacy/page.tsx
│   │   └── terms/page.tsx
│   ├── api/
│   │   ├── contact/route.ts
│   │   └── subscribe/route.ts
│   ├── rss.xml/route.ts
│   ├── sitemap.ts
│   ├── robots.ts
│   ├── not-found.tsx
│   ├── layout.tsx
│   └── globals.css
├── components/
│   ├── ui/                          # shadcn primitives
│   ├── layout/                      # header, footer, nav
│   ├── blog/                        # post-card, toc, mdx components
│   └── forms/                       # newsletter-form, contact-form
├── content/posts/                   # *.mdx
├── lib/
│   ├── posts.ts                     # load and parse MDX
│   ├── seo.ts                       # metadata and JSON-LD helpers
│   ├── validators.ts                # zod schemas
│   ├── rate-limit.ts
│   └── site-config.ts               # name, URL, nav, socials
├── public/
├── tests/
├── docs/                            # PRD, DESIGN, TECH_STACK, AGENT_PROMPT
├── .env.example
└── README.md
```

## 9. Security Baseline

- Validate all input on the server with Zod.
- Verify the Turnstile token server-side before sending email or calling the newsletter API.
- Rate limit `/api/contact` and `/api/subscribe` by IP.
- Set security headers in `next.config` (CSP, X-Frame-Options, Referrer-Policy, Permissions-Policy).
- Escape user input in emails; never echo raw input into HTML.
- Keep dependencies updated; run `pnpm audit` before launch.

## 10. Future Upgrades (post-MVP)

| When | Add |
|---|---|
| Content team grows | Headless CMS (Sanity or Payload) |
| Need to store inquiries | PostgreSQL (Neon/Supabase) with Drizzle or Prisma |
| Need logins or a client portal | Auth.js or Clerk, plus FastAPI service if heavy backend logic |
| Need bookings | Cal.com embed |
| Need payments | Stripe or Razorpay |
