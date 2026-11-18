import Link from "next/link";
import { TwitterIcon, LinkedinIcon, GithubIcon } from "@/components/ui/icons";
import { siteConfig } from "@/lib/site-config";
import { NewsletterForm } from "@/components/forms/newsletter-form";

export function Footer() {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="border-t border-border bg-surface" role="contentinfo">
      <div className="mx-auto max-w-[1200px] px-4 py-12 sm:px-6 lg:px-8">
        <div className="grid gap-8 sm:grid-cols-2 lg:grid-cols-4">
          {/* Brand blurb */}
          <div className="sm:col-span-2 lg:col-span-1">
            <Link href="/" className="text-lg font-bold font-heading text-text">
              {siteConfig.name}
            </Link>
            {/* TODO_COPY: Replace with your brand description */}
            <p className="mt-3 text-sm leading-relaxed text-text-muted">
              {siteConfig.description}
            </p>
          </div>

          {/* Pages */}
          <div>
            <h3 className="mb-3 text-sm font-semibold uppercase tracking-wider text-text-muted">
              Pages
            </h3>
            <ul className="space-y-2">
              {siteConfig.footerNav.pages.map((link) => (
                <li key={link.href}>
                  <Link
                    href={link.href}
                    className="text-sm text-text-muted transition-colors duration-150 hover:text-text"
                  >
                    {link.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Legal */}
          <div>
            <h3 className="mb-3 text-sm font-semibold uppercase tracking-wider text-text-muted">
              Legal
            </h3>
            <ul className="space-y-2">
              {siteConfig.footerNav.legal.map((link) => (
                <li key={link.href}>
                  <Link
                    href={link.href}
                    className="text-sm text-text-muted transition-colors duration-150 hover:text-text"
                  >
                    {link.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Social and newsletter */}
          <div>
            <h3 className="mb-3 text-sm font-semibold uppercase tracking-wider text-text-muted">
              Get the Newsletter
            </h3>
            <p className="mb-3 text-xs text-text-muted">
              Weekly frameworks delivered to your inbox.
            </p>
            <NewsletterForm variant="footer" className="mb-4" />
            <div className="flex gap-3 pt-2">
              <a
                href={siteConfig.socials.twitter}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex h-9 w-9 items-center justify-center rounded-[var(--radius-sm)] border border-border text-text-muted transition-colors duration-150 hover:bg-bg hover:text-text"
                aria-label="Twitter"
              >
                <TwitterIcon size={16} />
              </a>
              <a
                href={siteConfig.socials.linkedin}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex h-9 w-9 items-center justify-center rounded-[var(--radius-sm)] border border-border text-text-muted transition-colors duration-150 hover:bg-bg hover:text-text"
                aria-label="LinkedIn"
              >
                <LinkedinIcon size={16} />
              </a>
              <a
                href={siteConfig.socials.github}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex h-9 w-9 items-center justify-center rounded-[var(--radius-sm)] border border-border text-text-muted transition-colors duration-150 hover:bg-bg hover:text-text"
                aria-label="GitHub"
              >
                <GithubIcon size={16} />
              </a>
            </div>
          </div>
        </div>

        {/* Bottom bar */}
        <div className="mt-10 border-t border-border pt-6 text-center text-sm text-text-muted">
          © {currentYear} {siteConfig.name}. All rights reserved.
        </div>
      </div>
    </footer>
  );
}
