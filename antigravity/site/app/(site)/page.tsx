import Link from "next/link";
import { ArrowRight, TrendingUp, Globe, Target, Sparkles, BookOpen } from "lucide-react";
import { siteConfig } from "@/lib/site-config";
import { getFeaturedPosts } from "@/lib/posts";
import { PostCard } from "@/components/blog/post-card";

const iconMap = {
  TrendingUp,
  Globe,
  Target,
} as const;

export default async function HomePage() {
  const featuredPosts = getFeaturedPosts(2);

  return (
    <>
      {/* ── Hero Section ─────────────────────────────────── */}
      <section className="bg-bg px-4 py-16 sm:px-6 sm:py-24 lg:px-8 lg:py-32">
        <div className="mx-auto max-w-[1200px]">
          <div className="mx-auto max-w-2xl text-center">
            {/* TODO_COPY: Replace headline and subheadline */}
            <h1 className="font-heading text-3xl font-bold tracking-tight text-text sm:text-4xl lg:text-5xl">
              Grow Your Business with
              <span className="text-accent"> Strategy That Works</span>
            </h1>
            <p className="mt-6 text-lg leading-relaxed text-text-muted">
              Practical insights on growth strategy, digital presence, and brand
              positioning — delivered straight to your inbox every week.
            </p>

            {/* CTA buttons */}
            <div className="mt-8 flex flex-col items-center gap-3 sm:flex-row sm:justify-center">
              <Link
                href="/newsletter"
                className="inline-flex items-center gap-2 rounded-[var(--radius-sm)] bg-accent px-6 py-3 text-sm font-medium text-accent-foreground transition-colors duration-150 hover:bg-accent-hover"
              >
                Subscribe Free
                <ArrowRight size={16} />
              </Link>
              <Link
                href="/services"
                className="inline-flex items-center gap-2 rounded-[var(--radius-sm)] border border-border px-6 py-3 text-sm font-medium text-text transition-colors duration-150 hover:bg-surface"
              >
                See Services
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* ── Social Proof Strip ───────────────────────────── */}
      <section className="border-y border-border bg-surface px-4 py-8 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-[1200px] text-center">
          {/* TODO_COPY: Replace with real stats or client logos */}
          <p className="text-sm font-medium text-text-muted">
            Trusted by founders and teams building the next generation of
            businesses
          </p>
          <div className="mt-4 flex flex-wrap items-center justify-center gap-8 text-text-muted">
            <div className="text-center">
              <p className="text-2xl font-bold text-text">50+</p>
              <p className="text-xs text-text-muted">
                Clients Advised
              </p>
            </div>
            <div className="text-center">
              <p className="text-2xl font-bold text-text">35k+</p>
              <p className="text-xs text-text-muted">
                Readers Reached
              </p>
            </div>
            <div className="text-center">
              <p className="text-2xl font-bold text-text">4.9/5</p>
              <p className="text-xs text-text-muted">
                Average Rating
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* ── Services Teaser ──────────────────────────────── */}
      <section className="bg-bg px-4 py-16 sm:px-6 sm:py-24 lg:px-8">
        <div className="mx-auto max-w-[1200px]">
          <div className="text-center">
            <h2 className="font-heading text-2xl font-bold text-text sm:text-3xl">
              How We Help You Grow
            </h2>
            <p className="mt-3 text-text-muted">
              Three core services designed for founders who want results, not
              busywork.
            </p>
          </div>

          <div className="mt-10 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
            {siteConfig.services.map((service) => {
              const Icon = iconMap[service.icon];
              return (
                <div
                  key={service.title}
                  className="group rounded-[var(--radius-lg)] border border-border bg-surface p-6 transition-colors duration-150 hover:border-accent"
                >
                  <div className="mb-4 inline-flex h-10 w-10 items-center justify-center rounded-[var(--radius-sm)] bg-bg text-accent">
                    <Icon size={20} />
                  </div>
                  {/* TODO_COPY: Replace service titles and descriptions */}
                  <h3 className="font-heading text-lg font-semibold text-text">
                    {service.title}
                  </h3>
                  <p className="mt-2 text-sm leading-relaxed text-text-muted">
                    {service.description}
                  </p>
                  <Link
                    href="/services"
                    className="mt-4 inline-flex items-center gap-1 text-sm font-medium text-accent transition-colors duration-150 hover:text-accent-hover"
                  >
                    Learn more
                    <ArrowRight size={14} />
                  </Link>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* ── Featured Articles Section ─────────────────────── */}
      {featuredPosts.length > 0 && (
        <section className="border-t border-border bg-surface px-4 py-16 sm:px-6 sm:py-24 lg:px-8">
          <div className="mx-auto max-w-[1200px]">
            <div className="flex flex-col sm:flex-row sm:items-end sm:justify-between gap-4">
              <div>
                <div className="inline-flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-accent">
                  <BookOpen size={14} />
                  <span>Strategic Insights</span>
                </div>
                <h2 className="mt-2 font-heading text-2xl font-bold text-text sm:text-3xl">
                  Latest From The Journal
                </h2>
              </div>
              <Link
                href="/blog"
                className="inline-flex items-center gap-1.5 text-sm font-medium text-accent hover:text-accent-hover"
              >
                View all articles
                <ArrowRight size={14} />
              </Link>
            </div>

            <div className="mt-10 grid gap-6 sm:grid-cols-2">
              {featuredPosts.map((post) => (
                <PostCard key={post.slug} post={post} />
              ))}
            </div>
          </div>
        </section>
      )}

      {/* ── About Snippet ────────────────────────────────── */}
      <section className="bg-bg px-4 py-16 sm:px-6 sm:py-24 lg:px-8">
        <div className="mx-auto max-w-[1200px]">
          <div className="mx-auto max-w-2xl text-center">
            {/* TODO_COPY: Replace with your story */}
            <h2 className="font-heading text-2xl font-bold text-text sm:text-3xl">
              Built by Someone Who Gets It
            </h2>
            <p className="mt-4 text-text-muted leading-relaxed">
              I started {siteConfig.name} because I saw too many talented
              founders struggle with unclear positioning and scattershot
              marketing. After working with dozens of early-stage businesses, I
              distilled what actually works into a repeatable system.
            </p>
            <Link
              href="/about"
              className="mt-6 inline-flex items-center gap-2 text-sm font-medium text-accent transition-colors duration-150 hover:text-accent-hover"
            >
              Read my story
              <ArrowRight size={14} />
            </Link>
          </div>
        </div>
      </section>

      {/* ── Testimonials ─────────────────────────────────── */}
      <section className="border-t border-border bg-surface px-4 py-16 sm:px-6 sm:py-24 lg:px-8">
        <div className="mx-auto max-w-[1200px]">
          <h2 className="text-center font-heading text-2xl font-bold text-text sm:text-3xl">
            What Clients Say
          </h2>
          <div className="mt-10 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
            {[
              {
                quote:
                  "Meridian helped us productize our consulting services in 6 weeks. Our pipeline is now 3x more predictable and client onboarding is effortless.",
                name: "Sarah Jenkins",
                role: "Founder, Apex Advisory",
              },
              {
                quote:
                  "The positioning overhaul changed everything for our sales calls. We stopped competing on hourly rates and started closing fixed-price sprint contracts.",
                name: "David Chen",
                role: "Managing Director, Kinetic Labs",
              },
              {
                quote:
                  "Outstanding depth of strategic insight and execution. The articles alone have saved us hundreds of hours of trial and error.",
                name: "Marcus Vance",
                role: "CEO, Horizon Ventures",
              },
            ].map((t, i) => (
              <blockquote
                key={i}
                className="rounded-[var(--radius-lg)] border border-border bg-bg p-6"
              >
                <p className="text-sm leading-relaxed text-text-muted italic">
                  &ldquo;{t.quote}&rdquo;
                </p>
                <footer className="mt-4 text-sm">
                  <p className="font-semibold text-text">{t.name}</p>
                  <p className="text-text-muted text-xs">{t.role}</p>
                </footer>
              </blockquote>
            ))}
          </div>
        </div>
      </section>

      {/* ── Final CTA ────────────────────────────────────── */}
      <section className="border-t border-border bg-bg px-4 py-16 sm:px-6 sm:py-24 lg:px-8">
        <div className="mx-auto max-w-2xl text-center">
          <h2 className="font-heading text-2xl font-bold text-text sm:text-3xl">
            Ready to Grow?
          </h2>
          <p className="mt-3 text-text-muted">
            Join our newsletter for weekly insights, or get in touch to discuss
            how we can help your business.
          </p>
          <div className="mt-6 flex flex-col items-center gap-3 sm:flex-row sm:justify-center">
            <Link
              href="/newsletter"
              className="inline-flex items-center gap-2 rounded-[var(--radius-sm)] bg-accent px-6 py-3 text-sm font-medium text-accent-foreground transition-colors duration-150 hover:bg-accent-hover"
            >
              Subscribe Free
              <ArrowRight size={16} />
            </Link>
            <Link
              href="/contact"
              className="inline-flex items-center gap-2 rounded-[var(--radius-sm)] border border-border px-6 py-3 text-sm font-medium text-text transition-colors duration-150 hover:bg-surface"
            >
              Get in Touch
            </Link>
          </div>
        </div>
      </section>
    </>
  );
}
