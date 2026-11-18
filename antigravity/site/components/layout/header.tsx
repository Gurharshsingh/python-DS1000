"use client";

import { useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { Menu, X } from "lucide-react";
import { siteConfig } from "@/lib/site-config";
import { ThemeToggle } from "./theme-toggle";
import { GlobalSearch } from "@/components/blog/global-search";

export function Header() {
  const [mobileOpen, setMobileOpen] = useState(false);
  const pathname = usePathname();

  const isActive = (href: string) => {
    if (href === "/") return pathname === "/";
    return pathname.startsWith(href);
  };

  return (
    <header className="sticky top-0 z-50 border-b border-border bg-bg/80 backdrop-blur-lg">
      <div className="mx-auto flex h-16 max-w-[1200px] items-center justify-between px-4 sm:px-6 lg:px-8">
        {/* Logo */}
        <Link
          href="/"
          className="text-lg font-bold tracking-tight font-heading text-text transition-colors hover:text-accent"
        >
          {siteConfig.name}
        </Link>

        {/* Desktop nav */}
        <nav className="hidden items-center gap-1 md:flex" aria-label="Main navigation">
          {siteConfig.nav.map((link) => (
            <Link
              key={link.href}
              href={link.href}
              className={`rounded-[var(--radius-sm)] px-3 py-2 text-sm font-medium transition-colors duration-150 ${
                isActive(link.href)
                  ? "bg-surface text-text"
                  : "text-text-muted hover:bg-surface hover:text-text"
              }`}
            >
              {link.label}
            </Link>
          ))}
        </nav>

        {/* Desktop actions */}
        <div className="hidden items-center gap-2 md:flex">
          <GlobalSearch />
          <ThemeToggle />
          <Link
            href={siteConfig.cta.subscribe.href}
            className="rounded-[var(--radius-sm)] border border-border px-4 py-2 text-sm font-medium text-text transition-colors duration-150 hover:bg-surface"
          >
            {siteConfig.cta.subscribe.label}
          </Link>
          <Link
            href={siteConfig.cta.contact.href}
            className="rounded-[var(--radius-sm)] bg-accent px-4 py-2 text-sm font-medium text-accent-foreground transition-colors duration-150 hover:bg-accent-hover"
          >
            {siteConfig.cta.contact.label}
          </Link>
        </div>

        {/* Mobile controls */}
        <div className="flex items-center gap-2 md:hidden">
          <GlobalSearch />
          <ThemeToggle />
          <button
            onClick={() => setMobileOpen(!mobileOpen)}
            className="inline-flex h-9 w-9 items-center justify-center rounded-[var(--radius-sm)] border border-border text-text-muted transition-colors hover:bg-surface hover:text-text"
            aria-label={mobileOpen ? "Close menu" : "Open menu"}
            aria-expanded={mobileOpen}
          >
            {mobileOpen ? <X size={18} /> : <Menu size={18} />}
          </button>
        </div>
      </div>

      {/* Mobile drawer */}
      {mobileOpen && (
        <div className="border-t border-border bg-bg md:hidden">
          <nav
            className="mx-auto max-w-[1200px] space-y-1 px-4 py-4 sm:px-6"
            aria-label="Mobile navigation"
          >
            {siteConfig.nav.map((link) => (
              <Link
                key={link.href}
                href={link.href}
                onClick={() => setMobileOpen(false)}
                className={`block rounded-[var(--radius-sm)] px-3 py-2.5 text-sm font-medium transition-colors duration-150 ${
                  isActive(link.href)
                    ? "bg-surface text-text"
                    : "text-text-muted hover:bg-surface hover:text-text"
                }`}
              >
                {link.label}
              </Link>
            ))}
            <hr className="my-2 border-border" />
            <Link
              href={siteConfig.cta.subscribe.href}
              onClick={() => setMobileOpen(false)}
              className="block rounded-[var(--radius-sm)] border border-border px-3 py-2.5 text-center text-sm font-medium text-text transition-colors duration-150 hover:bg-surface"
            >
              {siteConfig.cta.subscribe.label}
            </Link>
            <Link
              href={siteConfig.cta.contact.href}
              onClick={() => setMobileOpen(false)}
              className="block rounded-[var(--radius-sm)] bg-accent px-3 py-2.5 text-center text-sm font-medium text-accent-foreground transition-colors duration-150 hover:bg-accent-hover"
            >
              {siteConfig.cta.contact.label}
            </Link>
          </nav>
        </div>
      )}
    </header>
  );
}
