# Launch Checklist

Use this checklist before taking the site live in production.

---

## 1. Environment & API Keys
- [ ] Set `NEXT_PUBLIC_SITE_URL` to your production domain (e.g., `https://example.com`)
- [ ] Set `BUTTONDOWN_API_KEY` for newsletter audience synchronization
- [ ] Set `RESEND_API_KEY`, `CONTACT_TO_EMAIL`, and `CONTACT_FROM_EMAIL` for inquiry delivery
- [ ] (Optional) Configure Cloudflare Turnstile keys: `NEXT_PUBLIC_TURNSTILE_SITE_KEY` and `TURNSTILE_SECRET_KEY`
- [ ] (Optional) Set `NEXT_PUBLIC_PLAUSIBLE_DOMAIN` for privacy-friendly analytics

## 2. Branding & Content Customization
- [ ] Review `lib/site-config.ts`:
  - Update `name`, `tagline`, `description`, and `email`
  - Update social URLs (`twitter`, `linkedin`, `github`)
  - Update service titles, descriptions, and pricing/deliverables
- [ ] Replace sample articles in `content/posts/` with your real articles
- [ ] Update About story and photo on `app/(site)/about/page.tsx`
- [ ] Update client testimonials on `app/(site)/page.tsx`
- [ ] Review Privacy Policy (`app/(site)/privacy/page.tsx`) and Terms (`app/(site)/terms/page.tsx`)

## 3. Pre-Flight Technical Verification
- [x] Run `pnpm typecheck` (zero TypeScript errors)
- [x] Run `pnpm test` (all unit tests passing)
- [x] Run `pnpm build` (all static pages and feeds generated successfully)
- [ ] Test Contact Form submission in staging / preview
- [ ] Test Newsletter subscription in staging / preview
- [ ] Verify `sitemap.xml` renders valid URLs at `/sitemap.xml`
- [ ] Verify `robots.txt` renders valid directives at `/robots.txt`
- [ ] Verify RSS feed loads at `/rss.xml`

## 4. Post-Deploy & Search Engines
- [ ] Submit `https://yourdomain.com/sitemap.xml` to Google Search Console
- [ ] Submit sitemap to Bing Webmaster Tools
- [ ] Run Google Lighthouse audit on mobile and desktop (Target: 95+ SEO, 90+ Performance, 95+ Accessibility)
- [ ] Test social share link previews on Twitter Card Validator & LinkedIn Post Inspector
