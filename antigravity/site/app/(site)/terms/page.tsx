import type { Metadata } from "next";
import { siteConfig } from "@/lib/site-config";

export const metadata: Metadata = {
  title: "Terms of Service",
  description: `Terms of service for ${siteConfig.name}.`,
};

export default function TermsPage() {
  return (
    <section className="bg-bg px-4 py-16 sm:px-6 sm:py-24 lg:px-8">
      <article className="prose mx-auto max-w-3xl">
        <h1>Terms of Service</h1>
        <p className="text-text-muted">
          Last updated: {new Date().toLocaleDateString("en-US", { month: "long", day: "numeric", year: "numeric" })}
        </p>

        {/* TODO_COPY: Replace with your real terms of service */}
        <h2>1. Agreement</h2>
        <p>
          By accessing and using {siteConfig.name}&apos;s website, you agree to
          these terms. If you do not agree, please do not use the site.
        </p>

        <h2>2. Services</h2>
        <p>
          {siteConfig.name} provides consulting services as described on our
          Services page. Specific engagements are governed by separate service
          agreements.
        </p>

        <h2>3. Intellectual Property</h2>
        <p>
          All content on this website — including text, graphics, logos, and
          code — is owned by {siteConfig.name} unless otherwise stated. Blog
          content may be shared with attribution and a link back to the original
          post.
        </p>

        <h2>4. User Submissions</h2>
        <p>
          Information submitted through our contact form or newsletter signup is
          subject to our{" "}
          <a href="/privacy">Privacy Policy</a>. You agree not to submit
          unlawful, harmful, or misleading content.
        </p>

        <h2>5. Disclaimers</h2>
        <p>
          Blog content and newsletter emails are provided for informational
          purposes only and do not constitute professional advice. Results from
          our services may vary.
        </p>

        <h2>6. Limitation of Liability</h2>
        <p>
          {siteConfig.name} is not liable for any indirect, incidental, or
          consequential damages arising from your use of this website or our
          services.
        </p>

        <h2>7. Changes</h2>
        <p>
          We reserve the right to update these terms at any time. Continued use
          of the site after changes constitutes acceptance.
        </p>

        <h2>8. Contact</h2>
        <p>
          Questions about these terms? Email us at{" "}
          <a href={`mailto:${siteConfig.email}`}>{siteConfig.email}</a>.
        </p>
      </article>
    </section>
  );
}
