"use client";

import { useEffect, useState } from "react";
import type { TocHeading } from "@/lib/posts";

interface TableOfContentsProps {
  headings: TocHeading[];
}

export function TableOfContents({ headings }: TableOfContentsProps) {
  const [activeId, setActiveId] = useState<string>("");

  useEffect(() => {
    if (!headings.length) return;

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            setActiveId(entry.target.id);
          }
        });
      },
      { rootMargin: "0px 0px -80% 0px", threshold: 0.1 }
    );

    headings.forEach((h) => {
      const el = document.getElementById(h.id);
      if (el) observer.observe(el);
    });

    return () => observer.disconnect();
  }, [headings]);

  if (!headings.length) return null;

  return (
    <nav aria-label="Table of Contents" className="rounded-[var(--radius-lg)] border border-border bg-surface p-5">
      <p className="font-heading text-sm font-semibold tracking-wide text-text uppercase">
        Table of Contents
      </p>
      <ul className="mt-4 space-y-2 text-sm">
        {headings.map((heading) => {
          const isActive = activeId === heading.id;
          return (
            <li
              key={heading.id}
              className={`${heading.level === 3 ? "pl-4 text-xs" : "font-medium"}`}
            >
              <a
                href={`#${heading.id}`}
                className={`block transition-colors duration-150 ${
                  isActive
                    ? "text-accent font-semibold"
                    : "text-text-muted hover:text-text"
                }`}
              >
                {heading.text}
              </a>
            </li>
          );
        })}
      </ul>
    </nav>
  );
}
