import type { Metadata } from "next";
import Link from "next/link";
import {
  ArrowRight,
  TrendingUp,
  Globe,
  Target,
  CheckCircle2,
} from "lucide-react";
import { siteConfig } from "@/lib/site-config";

export const metadata: Metadata = {
  title: "Services",
  description:
    "Growth strategy, digital presence, and brand positioning services for founders and small businesses.",
};

const iconMap = { TrendingUp, Globe, Target } as const;

const processSteps = [
  {
    step: "1",
    title: "Discovery",
    description:
      "We start with a deep-dive into your business, audience, and goals to understand where you are and where you want to go.",
  },
  {
    step: "2",
    title: "Strategy",
    description:
      "Based on our findings, we build a clear, actionable roadmap tailored to your growth stage and resources.",
  },
  {
    step: "3",
    title: "Execution",
    description:
      "We implement the plan together — whether that means building, writing, optimizing, or advising.",
  },
  {
    step: "4",
    title: "Iteration",
    description:
      "We track results, learn from the data, and refine the approach to keep momentum going.",
  },
];

/* TODO_COPY: Replace with real FAQ content */
const faqItems = [
  {
    question: "How long does a typical engagement last?",
    answer:
      "[Placeholder — describe your typical timeline, e.g. 'Most projects run 4-8 weeks, but we also offer ongoing advisory retainers.']",
  },
  {
    question: "Do you work with early-stage startups?",
    answer:
      "[Placeholder — describe your ideal client stage and any minimums.]",
  },
  {
    question: "What industries do you specialize in?",
    answer:
      "[Placeholder — list your areas of expertise or note that your approach is industry-agnostic.]",
  },
  {
    question: "How do we get started?",
    answer:
      "Fill out the contact form or send us an email. We'll schedule a free 30-minute call to see if we're a good fit.",
  },
];

export default function ServicesPage() {
  return (
    <>
      {/* ── Intro ────────────────────────────────────────── */}
      <section className="bg-bg px-4 py-16 sm:px-6 sm:py-24 lg:px-8">
        <div className="mx-auto max-w-[1200px]">
          <div className="mx-auto max-w-2xl text-center">
            <h1 className="font-heading text-3xl font-bold tracking-tight text-text sm:text-4xl">
              Services
            </h1>
            {/* TODO_COPY: Replace intro paragraph */}
            <p className="mt-4 text-lg text-text-muted leading-relaxed">
              We offer three focused services designed to help founders and small
              teams grow with clarity — no fluff, no busywork.
            </p>
          </div>
        </div>
      </section>

      {/* ── Service Cards (Detailed) ─────────────────────── */}
      <section className="border-t border-border bg-surface px-4 py-16 sm:px-6 sm:py-24 lg:px-8">
        <div className="mx-auto max-w-[1200px] space-y-8">
          {siteConfig.services.map((service, i) => {
            const Icon = iconMap[service.icon];
            const outcomes = [
              "[Outcome 1 — replace with a specific result clients can expect]",
              "[Outcome 2 — replace]",
              "[Outcome 3 — replace]",
            ];
            return (
              <div
                key={service.title}
                className="rounded-[var(--radius-lg)] border border-border bg-bg p-8 sm:p-10"
              >
                <div className="flex flex-col gap-6 sm:flex-row sm:items-start">
                  <div className="inline-flex h-12 w-12 shrink-0 items-center justify-center rounded-[var(--radius-sm)] bg-surface text-accent">
                    <Icon size={24} />
                  </div>
                  <div className="flex-1">
                    <h2 className="font-heading text-xl font-bold text-text sm:text-2xl">
                      {service.title}
                    </h2>
                    <p className="mt-2 text-text-muted leading-relaxed">
                      {service.description}
                    </p>
                    {/* TODO_COPY: Replace outcomes */}
                    <ul className="mt-4 space-y-2">
                      {outcomes.map((outcome, j) => (
                        <li
                          key={j}
                          className="flex items-start gap-2 text-sm text-text-muted"
                        >
                          <CheckCircle2
                            size={16}
                            className="mt-0.5 shrink-0 text-success"
                          />
                          {outcome}
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </section>

      {/* ── Process ──────────────────────────────────────── */}
      <section className="bg-bg px-4 py-16 sm:px-6 sm:py-24 lg:px-8">
        <div className="mx-auto max-w-[1200px]">
          <h2 className="text-center font-heading text-2xl font-bold text-text sm:text-3xl">
            How We Work
          </h2>
          <div className="mt-10 grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
            {processSteps.map((step) => (
              <div key={step.step} className="text-center">
                <div className="mx-auto mb-4 flex h-10 w-10 items-center justify-center rounded-full bg-accent text-sm font-bold text-accent-foreground">
                  {step.step}
                </div>
                <h3 className="font-heading text-lg font-semibold text-text">
                  {step.title}
                </h3>
                <p className="mt-2 text-sm text-text-muted">{step.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── FAQ ──────────────────────────────────────────── */}
      <section className="border-t border-border bg-surface px-4 py-16 sm:px-6 sm:py-24 lg:px-8">
        <div className="mx-auto max-w-3xl">
          <h2 className="text-center font-heading text-2xl font-bold text-text sm:text-3xl">
            Frequently Asked Questions
          </h2>
          <div className="mt-10 space-y-4">
            {faqItems.map((item, i) => (
              <details
                key={i}
                className="group rounded-[var(--radius-sm)] border border-border bg-bg"
              >
                <summary className="flex cursor-pointer items-center justify-between px-6 py-4 text-sm font-medium text-text [&::-webkit-details-marker]:hidden">
                  {item.question}
                  <span className="ml-4 text-text-muted transition-transform duration-150 group-open:rotate-45">
                    +
                  </span>
                </summary>
                <div className="px-6 pb-4 text-sm text-text-muted leading-relaxed">
                  {item.answer}
                </div>
              </details>
            ))}
          </div>
        </div>
      </section>

      {/* ── CTA ──────────────────────────────────────────── */}
      <section className="bg-bg px-4 py-16 sm:px-6 sm:py-24 lg:px-8">
        <div className="mx-auto max-w-2xl text-center">
          <h2 className="font-heading text-2xl font-bold text-text sm:text-3xl">
            Ready to Get Started?
          </h2>
          <p className="mt-3 text-text-muted">
            Tell us about your business and goals. We&apos;ll respond within one
            business day.
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
