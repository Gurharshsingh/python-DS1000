"use client";

import { useState } from "react";
import { ArrowRight, CheckCircle2, AlertCircle, Loader2 } from "lucide-react";

interface NewsletterFormProps {
  variant?: "inline" | "footer" | "hero" | "page";
  className?: string;
}

export function NewsletterForm({
  variant = "inline",
  className = "",
}: NewsletterFormProps) {
  const [email, setEmail] = useState("");
  const [website, setWebsite] = useState(""); // Honeypot
  const [status, setStatus] = useState<"idle" | "loading" | "success" | "error">(
    "idle"
  );
  const [message, setMessage] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!email) return;

    setStatus("loading");
    setMessage("");

    try {
      const res = await fetch("/api/subscribe", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, website }),
      });

      const data = await res.json();

      if (!res.ok) {
        throw new Error(data.error || "Failed to subscribe");
      }

      setStatus("success");
      setMessage(data.message || "Thank you for subscribing!");
      setEmail("");
    } catch (err: unknown) {
      setStatus("error");
      const errorMessage =
        err instanceof Error ? err.message : "Something went wrong. Please try again.";
      setMessage(errorMessage);
    }
  };

  if (status === "success") {
    return (
      <div
        className={`flex items-center gap-2 rounded-[var(--radius-md)] bg-emerald-500/10 border border-emerald-500/30 p-4 text-sm text-emerald-600 dark:text-emerald-400 ${className}`}
        role="alert"
      >
        <CheckCircle2 size={18} className="shrink-0" />
        <span>{message}</span>
      </div>
    );
  }

  const isFooter = variant === "footer";
  const isHero = variant === "hero";

  return (
    <form onSubmit={handleSubmit} className={`w-full ${className}`}>
      {/* Honeypot field — hidden from humans */}
      <div className="sr-only" aria-hidden="true">
        <label htmlFor={`nl-website-${variant}`}>Leave this field blank</label>
        <input
          type="text"
          id={`nl-website-${variant}`}
          name="website"
          value={website}
          onChange={(e) => setWebsite(e.target.value)}
          tabIndex={-1}
          autoComplete="off"
        />
      </div>

      <div
        className={`flex flex-col gap-2.5 ${
          isHero || isFooter ? "sm:flex-row sm:items-center" : "sm:flex-row"
        }`}
      >
        <div className="relative flex-1">
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            placeholder="Enter your email"
            aria-label="Email address for newsletter"
            disabled={status === "loading"}
            className="h-11 w-full rounded-[var(--radius-sm)] border border-border bg-bg px-3.5 text-sm text-text placeholder:text-text-muted focus:border-accent focus:outline-none focus:ring-2 focus:ring-accent/20 disabled:opacity-60"
          />
        </div>

        <button
          type="submit"
          disabled={status === "loading"}
          className="inline-flex h-11 items-center justify-center gap-2 rounded-[var(--radius-sm)] bg-accent px-5 text-sm font-medium text-accent-foreground transition-colors hover:bg-accent-hover disabled:opacity-60 shrink-0"
        >
          {status === "loading" ? (
            <>
              <Loader2 size={16} className="animate-spin" />
              <span>Subscribing…</span>
            </>
          ) : (
            <>
              <span>Subscribe</span>
              <ArrowRight size={14} />
            </>
          )}
        </button>
      </div>

      {status === "error" && (
        <div
          className="mt-2.5 flex items-center gap-1.5 text-xs text-rose-500"
          role="alert"
        >
          <AlertCircle size={14} className="shrink-0" />
          <span>{message}</span>
        </div>
      )}

      <p className="mt-2 text-[11px] text-text-muted">
        No spam. Unsubscribe with one click anytime.
      </p>
    </form>
  );
}
