"use client";

import { useState, useEffect, useRef } from "react";
import { useRouter } from "next/navigation";
import { Search, X, FileText, ArrowRight, Tag } from "lucide-react";
import Fuse from "fuse.js";

export interface SearchPostItem {
  slug: string;
  title: string;
  description: string;
  tags: string[];
  date: string;
}

interface SearchDialogProps {
  posts: SearchPostItem[];
}

export function SearchDialog({ posts }: SearchDialogProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<SearchPostItem[]>([]);
  const router = useRouter();
  const inputRef = useRef<HTMLInputElement>(null);

  // Initialize Fuse instance
  const fuse = new Fuse(posts, {
    keys: [
      { name: "title", weight: 0.5 },
      { name: "tags", weight: 0.3 },
      { name: "description", weight: 0.2 },
    ],
    threshold: 0.4,
    ignoreLocation: true,
  });

  // Handle keyboard shortcut Cmd+K / Ctrl+K
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === "k") {
        e.preventDefault();
        setIsOpen((prev) => !prev);
      }
      if (e.key === "Escape" && isOpen) {
        setIsOpen(false);
      }
    };

    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [isOpen]);

  useEffect(() => {
    if (isOpen) {
      setTimeout(() => inputRef.current?.focus(), 50);
    } else {
      setQuery("");
      setResults([]);
    }
  }, [isOpen]);

  useEffect(() => {
    if (!query.trim()) {
      setResults(posts.slice(0, 5));
    } else {
      const res = fuse.search(query).map((item) => item.item);
      setResults(res);
    }
  }, [query, posts]);

  const handleSelect = (slug: string) => {
    setIsOpen(false);
    router.push(`/blog/${slug}`);
  };

  return (
    <>
      {/* Search trigger button */}
      <button
        type="button"
        onClick={() => setIsOpen(true)}
        className="inline-flex h-9 items-center gap-2 rounded-[var(--radius-sm)] border border-border bg-surface px-3 text-xs text-text-muted transition-colors hover:border-accent/40 hover:text-text"
        aria-label="Search articles"
      >
        <Search size={14} className="text-accent" />
        <span>Search articles…</span>
        <kbd className="hidden sm:inline-block rounded border border-border bg-bg px-1.5 py-0.5 text-[10px] font-semibold text-text-muted">
          ⌘K
        </kbd>
      </button>

      {/* Modal Dialog */}
      {isOpen && (
        <div
          className="fixed inset-0 z-50 flex items-start justify-center bg-black/60 p-4 pt-20 backdrop-blur-sm animate-fade-in"
          onClick={() => setIsOpen(false)}
        >
          <div
            className="w-full max-w-xl rounded-[var(--radius-lg)] border border-border bg-surface shadow-2xl overflow-hidden"
            onClick={(e) => e.stopPropagation()}
          >
            {/* Search Input Bar */}
            <div className="flex items-center border-b border-border px-4 py-3">
              <Search size={18} className="text-accent mr-3 shrink-0" />
              <input
                ref={inputRef}
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Search by topic, keyword, or title…"
                className="w-full bg-transparent text-sm text-text placeholder:text-text-muted focus:outline-none"
              />
              <button
                onClick={() => setIsOpen(false)}
                className="text-text-muted hover:text-text p-1"
                aria-label="Close search"
              >
                <X size={16} />
              </button>
            </div>

            {/* Results List */}
            <div className="max-h-80 overflow-y-auto p-2">
              {results.length > 0 ? (
                <div className="space-y-1">
                  <p className="px-3 py-1.5 text-[11px] font-semibold uppercase tracking-wider text-text-muted">
                    {query.trim() ? "Search Results" : "Recent Articles"}
                  </p>
                  {results.map((post) => (
                    <button
                      key={post.slug}
                      onClick={() => handleSelect(post.slug)}
                      className="group flex w-full items-start justify-between rounded-[var(--radius-md)] p-3 text-left transition-colors hover:bg-bg"
                    >
                      <div className="flex items-start gap-3">
                        <FileText size={16} className="mt-0.5 shrink-0 text-accent" />
                        <div>
                          <p className="text-sm font-semibold text-text group-hover:text-accent transition-colors">
                            {post.title}
                          </p>
                          <p className="mt-1 text-xs text-text-muted line-clamp-1">
                            {post.description}
                          </p>
                          <div className="mt-2 flex items-center gap-2">
                            {post.tags.slice(0, 2).map((tag) => (
                              <span
                                key={tag}
                                className="inline-flex items-center gap-0.5 rounded bg-surface border border-border px-1.5 py-0.5 text-[10px] text-text-muted"
                              >
                                <Tag size={10} /> {tag}
                              </span>
                            ))}
                          </div>
                        </div>
                      </div>
                      <ArrowRight
                        size={14}
                        className="opacity-0 group-hover:opacity-100 transition-opacity text-accent shrink-0 mt-1"
                      />
                    </button>
                  ))}
                </div>
              ) : (
                <div className="p-8 text-center text-sm text-text-muted">
                  No articles found matching &ldquo;{query}&rdquo;
                </div>
              )}
            </div>

            {/* Modal Footer */}
            <div className="flex items-center justify-between border-t border-border bg-bg/50 px-4 py-2 text-[11px] text-text-muted">
              <span>Navigate with mouse or touch</span>
              <kbd className="rounded border border-border bg-bg px-1.5 py-0.5 text-[10px]">
                ESC to close
              </kbd>
            </div>
          </div>
        </div>
      )}
    </>
  );
}
