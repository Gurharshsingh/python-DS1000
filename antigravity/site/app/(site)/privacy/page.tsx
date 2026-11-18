import type { Metadata } from "next";
import { siteConfig } from "@/lib/site-config";

export const metadata: Metadata = {
  title: "Privacy Policy",
  description: `Privacy policy for ${siteConfig.name} — how we handle your data.`,
};

export default function PrivacyPage() {
  return (
    <section className="bg-bg px-4 py-16 sm:px-6 sm:py-24 lg:px-8">
      <article className="prose mx-auto max-w-3xl">
        <h1>Privacy Policy</h1>
        <p className="text-text-muted">
          Last updated: {new Date().toLocaleDateString("en-US", { month: "long", day: "numeric", year: "numeric" })}
        </p>

        {/* TODO_COPY: Replace with your real privacy policy */}
        <h2>1. Information We Collect</h2>
        <p>
          When you use our website, we may collect the following information:
        </p>
        <ul>
          <li>
            <strong>Contact form:</strong> Name, email address, and message
            content when you submit our contact form.
          </li>
          <li>
            <strong>Newsletter:</strong> Email address when you subscribe to our
            newsletter.
          </li>
          <li>
            <strong>Analytics:</strong> Anonymous usage data (pages visited,
            browser type, country) via privacy-friendly analytics. We do not use
            cookies for tracking.
          </li>
        </ul>

        <h2>2. How We Use Your Information</h2>
        <ul>
          <li>To respond to your inquiries via the contact form.</li>
          <li>To send you our newsletter (if you subscribed).</li>
          <li>To improve our website and content based on aggregate usage data.</li>
        </ul>

        <h2>3. Data Sharing</h2>
        <p>
          We do not sell your personal information. We share data only with
          service providers necessary to operate the site:
        </p>
        <ul>
          <li>
            <strong>Email delivery:</strong> Resend (for contact form
            notifications) and Buttondown (for newsletter delivery).
          </li>
          <li>
            <strong>Hosting:</strong> Vercel.
          </li>
          <li>
            <strong>Analytics:</strong> Plausible Analytics (privacy-friendly, no
            cookies, GDPR-compliant).
          </li>
        </ul>

        <h2>4. Data Retention</h2>
        <p>
          Contact form submissions are retained for as long as needed to respond.
          Newsletter subscriptions are retained until you unsubscribe.
        </p>

        <h2>5. Your Rights</h2>
        <p>
          You may request access to, correction of, or deletion of your personal
          data at any time by contacting us at{" "}
          <a href={`mailto:${siteConfig.email}`}>{siteConfig.email}</a>.
        </p>

        <h2>6. Newsletter</h2>
        <p>
          You can unsubscribe from our newsletter at any time by clicking the
          &quot;unsubscribe&quot; link in any email, or by contacting us directly.
        </p>

        <h2>7. Changes</h2>
        <p>
          We may update this policy from time to time. Changes will be posted on
          this page with an updated revision date.
        </p>

        <h2>8. Contact</h2>
        <p>
          Questions about this policy? Email us at{" "}
          <a href={`mailto:${siteConfig.email}`}>{siteConfig.email}</a>.
        </p>
      </article>
    </section>
  );
}
