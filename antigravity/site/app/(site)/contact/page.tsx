import type { Metadata } from "next";
import { Mail } from "lucide-react";
import { TwitterIcon, LinkedinIcon } from "@/components/ui/icons";
import { ContactForm } from "@/components/forms/contact-form";
import { siteConfig } from "@/lib/site-config";

export const metadata: Metadata = {
  title: "Contact",
  description: `Get in touch with ${siteConfig.name}. Tell us about your project and we'll respond within one business day.`,
};

export default function ContactPage() {
  return (
    <section className="bg-bg px-4 py-16 sm:px-6 sm:py-24 lg:px-8">
      <div className="mx-auto max-w-[1200px]">
        <div className="mx-auto max-w-2xl text-center">
          <h1 className="font-heading text-3xl font-bold tracking-tight text-text sm:text-4xl">
            Get in Touch
          </h1>
          <p className="mt-4 text-text-muted">
            Tell us about your business and goals. We&apos;ll get back to you
            within one business day.
          </p>
        </div>

        <div className="mt-12 grid gap-10 lg:grid-cols-5">
          {/* ── Form ── */}
          <div className="lg:col-span-3">
            <div className="rounded-[var(--radius-lg)] border border-border bg-surface p-6 sm:p-8">
              <ContactForm />
            </div>
          </div>

          {/* ── Contact info sidebar ─────────────────────── */}
          <aside className="lg:col-span-2">
            <div className="rounded-[var(--radius-lg)] border border-border bg-surface p-6">
              <h2 className="font-heading text-lg font-semibold text-text">
                Other Ways to Reach Us
              </h2>

              <div className="mt-6 space-y-4">
                <div className="flex items-start gap-3">
                  <Mail size={18} className="mt-0.5 shrink-0 text-accent" />
                  <div>
                    <p className="text-sm font-medium text-text">Email</p>
                    <a
                      href={`mailto:${siteConfig.email}`}
                      className="text-sm text-accent hover:text-accent-hover"
                    >
                      {siteConfig.email}
                    </a>
                  </div>
                </div>

                <div className="flex items-start gap-3">
                  <TwitterIcon size={18} className="mt-0.5 shrink-0 text-accent" />
                  <div>
                    <p className="text-sm font-medium text-text">Twitter</p>
                    <a
                      href={siteConfig.socials.twitter}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-sm text-accent hover:text-accent-hover"
                    >
                      @example
                    </a>
                  </div>
                </div>

                <div className="flex items-start gap-3">
                  <LinkedinIcon
                    size={18}
                    className="mt-0.5 shrink-0 text-accent"
                  />
                  <div>
                    <p className="text-sm font-medium text-text">LinkedIn</p>
                    <a
                      href={siteConfig.socials.linkedin}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-sm text-accent hover:text-accent-hover"
                    >
                      Connect on LinkedIn
                    </a>
                  </div>
                </div>
              </div>

              <hr className="my-6 border-border" />

              <p className="text-sm text-text-muted">
                We typically respond within one business day. For urgent
                matters, please mention it in your message.
              </p>
            </div>
          </aside>
        </div>
      </div>
    </section>
  );
}
