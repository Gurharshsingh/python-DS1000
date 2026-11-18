"use client";

import { useState } from "react";
import { Link2, Check } from "lucide-react";
import { TwitterIcon, LinkedinIcon } from "@/components/ui/icons";

interface ShareButtonsProps {
  title: string;
  url: string;
}

export function ShareButtons({ title, url }: ShareButtonsProps) {
  const [copied, setCopied] = useState(false);

  const encodedTitle = encodeURIComponent(title);
  const encodedUrl = encodeURIComponent(url);

  const twitterUrl = `https://twitter.com/intent/tweet?text=${encodedTitle}&url=${encodedUrl}`;
  const linkedinUrl = `https://www.linkedin.com/sharing/share-offsite/?url=${encodedUrl}`;

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(url);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (e) {
      console.error("Failed to copy link", e);
    }
  };

  return (
    <div className="flex items-center gap-2">
      <span className="text-xs font-medium text-text-muted mr-1">Share:</span>
      <a
        href={twitterUrl}
        target="_blank"
        rel="noopener noreferrer"
        className="inline-flex h-8 w-8 items-center justify-center rounded-[var(--radius-sm)] border border-border bg-surface text-text-muted transition-colors hover:bg-bg hover:text-text"
        aria-label="Share on Twitter"
      >
        <TwitterIcon size={14} />
      </a>
      <a
        href={linkedinUrl}
        target="_blank"
        rel="noopener noreferrer"
        className="inline-flex h-8 w-8 items-center justify-center rounded-[var(--radius-sm)] border border-border bg-surface text-text-muted transition-colors hover:bg-bg hover:text-text"
        aria-label="Share on LinkedIn"
      >
        <LinkedinIcon size={14} />
      </a>
      <button
        onClick={handleCopy}
        className="inline-flex h-8 w-8 items-center justify-center rounded-[var(--radius-sm)] border border-border bg-surface text-text-muted transition-colors hover:bg-bg hover:text-text relative"
        aria-label="Copy link"
      >
        {copied ? <Check size={14} className="text-emerald-500" /> : <Link2 size={14} />}
      </button>
      {copied && (
        <span className="text-xs text-emerald-500 font-medium animate-fade-in">
          Copied!
        </span>
      )}
    </div>
  );
}
