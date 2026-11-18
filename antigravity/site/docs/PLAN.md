# Implementation Plan

## Status Key
- [ ] Not started
- [x] Complete
- [~] In progress

---

## Phase 0: Setup
- [x] Create Next.js project (TypeScript, Tailwind, ESLint, pnpm, App Router)
- [x] Configure Prettier, `.editorconfig`
- [x] Create `.env.example`, `.gitignore`
- [x] Create folder structure per TECH_STACK
- [x] Add `lib/site-config.ts` with placeholders
- [x] Create `README.md` with setup instructions
- [x] Verify: `pnpm dev` starts cleanly

## Phase 1: Design System and Layout
- [x] Implement color tokens (light/dark) in Tailwind config and `globals.css`
- [x] Set up fonts with `next/font` (Plus Jakarta Sans, Inter, JetBrains Mono)
- [x] Set up dark mode with `next-themes`
- [x] Install primitives (buttons, inputs, select, modal dialogs, badges, cards)
- [x] Build Header (sticky, mobile drawer, theme toggle, Cmd+K search trigger)
- [x] Build Footer (brand blurb, nav, social links, newsletter mini-form, legal links)
- [x] Build skip-to-content link
- [x] Build page container / section wrapper components
- [x] Verify: lint, type-check, build pass; visual check at 375px and 1280px

## Phase 2: Core Pages
- [x] Home page (hero, social proof, dynamic featured posts, services teaser, about snippet, testimonials, final CTA)
- [x] Services page (intro, service cards, process steps, FAQ accordion, CTA)
- [x] About page (story, values, credentials, photo placeholder, CTA)
- [x] Contact page (form UI + two-column layout + direct contact sidebar)
- [x] Newsletter page (value prop, signup form, privacy note)
- [x] Privacy Policy page
- [x] Terms of Service page
- [x] Custom 404 page
- [x] Verify: all pages render at mobile and desktop; lint, type-check, build pass

## Phase 3: Blog Engine
- [x] Create `lib/posts.ts` (load MDX, parse frontmatter, reading time, sort, filter)
- [x] Set up MDX rendering with `next-mdx-remote/rsc` and plugins
- [x] Build custom MDX components (callouts, code blocks, tables, lists, links)
- [x] Blog list page with tag filter, featured post, and grid
- [x] Blog post page with TOC, heading anchors, reading time, author box, share links, related posts
- [x] Tag pages (`/blog/tag/[tag]`)
- [x] Create 3 sample posts (Growth Strategy, Digital Presence, Brand Positioning)
- [x] Exclude drafts in production
- [x] Verify: blog renders correctly; lint, type-check, build pass

## Phase 4: Forms and Integrations
- [x] Shared Zod schemas in `lib/validators.ts`
- [x] `/api/subscribe` route (validate, Turnstile, rate limit, Buttondown API fallback)
- [x] `/api/contact` route (validate, Turnstile, rate limit, Resend email fallback)
- [x] Build `NewsletterForm` component (variants for page, hero, footer, inline)
- [x] Build `ContactForm` with react-hook-form and Zod resolver
- [x] Rate limiting with in-memory fallback
- [x] Graceful degradation when env keys missing
- [x] Verify: forms work end-to-end; lint, type-check, build pass

## Phase 5: SEO and Discoverability
- [x] `generateMetadata` on every page with canonical URLs, OG, Twitter cards
- [x] JSON-LD (Organization, WebSite, Article schemas)
- [x] `sitemap.ts` and `robots.ts`
- [x] `/rss.xml` route with full RSS 2.0 XML generation
- [x] Client-side search with `fuse.js` (`SearchDialog` and `GlobalSearch`)
- [x] Verify: metadata correct; sitemap/robots/rss valid; build passes

## Phase 6: Quality
- [x] Accessibility pass (landmarks, skip link, focus rings, contrast, alt text, keyboard nav)
- [x] Performance pass (SSG/ISR, minimal client JS, tree-shakeable SVG icons)
- [x] Security headers in `next.config.ts` (HSTS, CSP, X-Frame-Options, Referrer-Policy, Permissions-Policy)
- [x] Vitest tests for schemas and post utilities (`pnpm test` passing 16/16 tests)
- [x] Fix all lint, type, and build failures

## Phase 7: Launch Prep
- [x] Final `README.md` (setup, env vars, writing posts, deploying)
- [x] `docs/LAUNCH_CHECKLIST.md`
- [x] Production build passes cleanly (`pnpm build`)
