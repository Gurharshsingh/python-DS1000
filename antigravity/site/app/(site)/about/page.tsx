import type { Metadata } from "next";
import Link from "next/link";
import { ArrowRight } from "lucide-react";
import { siteConfig } from "@/lib/site-config";

export const metadata: Metadata = {
  title: "About",
  description: `Learn about ${siteConfig.name} — our story, values, and approach to helping businesses grow.`,
};

export default function AboutPage() {
  return (
    <>
      {/* ── Story ────────────────────────────────────────── */}
      <section className="bg-bg px-4 py-16 sm:px-6 sm:py-24 lg:px-8">
        <div className="mx-auto max-w-3xl">
          <h1 className="font-heading text-3xl font-bold tracking-tight text-text sm:text-4xl">
            About {siteConfig.name}
          </h1>
          {/* TODO_COPY: Replace with your real story */}
          <div className="mt-8 space-y-5 text-text-muted leading-relaxed">
            <p>
              {siteConfig.name} started with a simple observation: most small
              businesses don&apos;t fail because of bad products — they fail
              because no one knows they exist. The gap between a great offering
              and a growing customer base is almost always strategy, not effort.
            </p>
            <p>
              After years of working in growth roles — from early-stage
              startups to established agencies — I kept seeing the same patterns.
              Founders pouring energy into tactics without a clear direction.
              Websites that looked nice but didn&apos;t convert. Content
              calendars that fizzled out after two months.
            </p>
            <p>
              So I built {siteConfig.name} to be the partner I wish those
              businesses had: someone who combines strategic thinking with
              hands-on execution, and who measures success by results, not
              deliverables.
            </p>
          </div>
        </div>
      </section>

      {/* ── Values / Approach ────────────────────────────── */}
      <section className="border-t border-border bg-surface px-4 py-16 sm:px-6 sm:py-24 lg:px-8">
        <div className="mx-auto max-w-3xl">
          <h2 className="font-heading text-2xl font-bold text-text sm:text-3xl">
            Our Approach
          </h2>
          <div className="mt-8 grid gap-6 sm:grid-cols-2">
            {/* TODO_COPY: Replace values */}
            {[
              {
                title: "Clarity Over Complexity",
                description:
                  "We cut through the noise. Every recommendation is specific, actionable, and tied to a measurable outcome.",
              },
              {
                title: "Build for Compounding",
                description:
                  "We prioritize assets that grow in value over time — content, SEO, systems — not one-off campaigns.",
              },
              {
                title: "Data-Informed, Not Data-Paralyzed",
                description:
                  "We use numbers to make better decisions, not to delay them. Ship, measure, improve.",
              },
              {
                title: "Honest Partnership",
                description:
                  "If something won't work for your business, we'll say so. Our goal is your growth, not billable hours.",
              },
            ].map((value) => (
              <div
                key={value.title}
                className="rounded-[var(--radius-lg)] border border-border bg-bg p-6"
              >
                <h3 className="font-heading text-lg font-semibold text-text">
                  {value.title}
                </h3>
                <p className="mt-2 text-sm text-text-muted leading-relaxed">
                  {value.description}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── Credentials ──────────────────────────────────── */}
      <section className="bg-bg px-4 py-16 sm:px-6 sm:py-24 lg:px-8">
        <div className="mx-auto max-w-3xl">
          <h2 className="font-heading text-2xl font-bold text-text sm:text-3xl">
            Credentials
          </h2>
          {/* TODO_COPY: Replace with your real credentials */}
          <ul className="mt-6 space-y-3 text-text-muted">
            <li className="flex items-start gap-2">
              <span className="mt-1.5 block h-1.5 w-1.5 shrink-0 rounded-full bg-accent" />
              [X years of experience in growth / marketing / strategy]
            </li>
            <li className="flex items-start gap-2">
              <span className="mt-1.5 block h-1.5 w-1.5 shrink-0 rounded-full bg-accent" />
              [Worked with N businesses across Y industries]
            </li>
            <li className="flex items-start gap-2">
              <span className="mt-1.5 block h-1.5 w-1.5 shrink-0 rounded-full bg-accent" />
              [Notable achievement or certification]
            </li>
          </ul>
        </div>
      </section>

      {/* ── CTA ──────────────────────────────────────────── */}
      <section className="border-t border-border bg-surface px-4 py-16 sm:px-6 sm:py-24 lg:px-8">
        <div className="mx-auto max-w-2xl text-center">
          <h2 className="font-heading text-2xl font-bold text-text sm:text-3xl">
            Let&apos;s Talk
          </h2>
          <p className="mt-3 text-text-muted">
            Have a project in mind or want to explore how we can work together?
          </p>
          <Link
            href="/contact"
            className="mt-6 inline-flex items-center gap-2 rounded-[var(--radius-sm)] bg-accent px-6 py-3 text-sm font-medium text-accent-foreground transition-colors duration-150 hover:bg-accent-hover"
          >
            Get in Touch
            <ArrowRight size={16} />
          </Link>
        </div>
      </section>
    </>
  );
}
