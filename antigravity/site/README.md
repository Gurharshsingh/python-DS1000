# Meridian — Strategy & Growth Consultancy

A fast, SEO-friendly service business website built with Next.js, TypeScript, and Tailwind CSS.

## Quick Start

```bash
# 1. Install dependencies
pnpm install

# 2. Copy environment variables
cp .env.example .env.local
# Edit .env.local with your API keys

# 3. Start development server
pnpm dev

# 4. Open http://localhost:3000
```

## Scripts

| Command | Description |
|---|---|
| `pnpm dev` | Start dev server (Turbopack) |
| `pnpm build` | Production build |
| `pnpm start` | Serve production build |
| `pnpm lint` | Run ESLint |
| `pnpm typecheck` | Run TypeScript type checker |
| `pnpm test` | Run tests |

## Project Structure

```
app/           → Pages and API routes (App Router)
components/    → Reusable UI components
  ui/          → shadcn/ui primitives
  layout/      → Header, footer, navigation
  blog/        → Post card, TOC, MDX components
  forms/       → Newsletter and contact forms
content/posts/ → Blog posts (MDX)
lib/           → Utilities, config, validators
public/        → Static assets
tests/         → Unit and E2E tests
docs/          → Project documentation
```

## Environment Variables

See `.env.example` for the full list. Key variables:

- `NEXT_PUBLIC_SITE_URL` — Your production URL
- `BUTTONDOWN_API_KEY` — Newsletter API
- `RESEND_API_KEY` — Transactional email
- `TURNSTILE_SECRET_KEY` — Spam protection
- `UPSTASH_REDIS_REST_*` — Rate limiting

All integrations degrade gracefully in development when keys are missing.

## Writing a Blog Post

Create a new `.mdx` file in `content/posts/`:

```mdx
---
title: "Your Post Title"
description: "A brief description for SEO and social cards."
date: "2024-01-15"
tags: ["strategy", "growth"]
author: "Sourav"
draft: false
---

Your content here using Markdown and MDX components.
```

## Tech Stack

- **Framework:** Next.js 16 (App Router)
- **Language:** TypeScript (strict)
- **Styling:** Tailwind CSS v4
- **UI:** shadcn/ui (Radix primitives)
- **Content:** MDX with gray-matter
- **Forms:** react-hook-form + Zod
- **Email:** Resend
- **Newsletter:** Buttondown
- **Analytics:** Plausible
- **Hosting:** Vercel

## Documentation

- [PRD](docs/PRD.md) — Product requirements
- [Design](docs/DESIGN.md) — Visual system and components
- [Tech Stack](docs/TECH_STACK.md) — Architecture decisions
- [Decisions](docs/DECISIONS.md) — Ambiguity resolutions
- [Plan](docs/PLAN.md) — Implementation phases
- [Launch Checklist](docs/LAUNCH_CHECKLIST.md) — Pre-flight checklist for production deployment

## License

Private. All rights reserved.
