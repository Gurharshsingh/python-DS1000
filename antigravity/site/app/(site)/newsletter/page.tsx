import type { Metadata } from "next";
import { siteConfig } from "@/lib/site-config";
import { NewsletterForm } from "@/components/forms/newsletter-form";

export const metadata: Metadata = {
  title: "Newsletter",
  description: `Subscribe to the ${siteConfig.name} newsletter — ${siteConfig.newsletter.valueProp}`,
};

export default function NewsletterPage() {
  return (
    <section className="bg-bg px-4 py-16 sm:px-6 sm:py-24 lg:px-8">
      <div className="mx-auto max-w-2xl text-center">
        <h1 className="font-heading text-3xl font-bold tracking-tight text-text sm:text-4xl">
          Stay Ahead of the Curve
        </h1>
        <p className="mt-4 text-lg text-text-muted leading-relaxed">
          {siteConfig.newsletter.valueProp}
        </p>

        {/* TODO_COPY: Replace details */}
        <div className="mt-8 rounded-[var(--radius-lg)] border border-border bg-surface p-8 text-left">
          <h2 className="font-heading text-lg font-semibold text-text">
            What You&apos;ll Get
          </h2>
          <ul className="mt-4 space-y-3 text-sm text-text-muted">
            <li className="flex items-start gap-2">
              <span className="mt-1.5 block h-1.5 w-1.5 shrink-0 rounded-full bg-accent" />
              One actionable growth tip you can implement the same week
            </li>
            <li className="flex items-start gap-2">
              <span className="mt-1.5 block h-1.5 w-1.5 shrink-0 rounded-full bg-accent" />
              Curated tools and resources we actually use
            </li>
            <li className="flex items-start gap-2">
              <span className="mt-1.5 block h-1.5 w-1.5 shrink-0 rounded-full bg-accent" />
              Deep-dive articles on strategy, content, and positioning
            </li>
            <li className="flex items-start gap-2">
              <span className="mt-1.5 block h-1.5 w-1.5 shrink-0 rounded-full bg-accent" />
              Sent every {siteConfig.newsletter.frequency.toLowerCase()} — no
              spam, unsubscribe anytime
            </li>
          </ul>

          <div className="mt-8">
            <NewsletterForm variant="page" />
          </div>
        </div>

        <p className="mt-6 text-xs text-text-muted">
          We respect your privacy. Read our{" "}
          <a
            href="/privacy"
            className="text-accent underline underline-offset-2 hover:text-accent-hover"
          >
            Privacy Policy
          </a>
          .
        </p>
      </div>
    </section>
  );
}
