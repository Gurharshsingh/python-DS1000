"use client";

import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { contactSchema, type ContactInput } from "@/lib/validators";
import { siteConfig } from "@/lib/site-config";
import { CheckCircle2, AlertCircle, Loader2, Send } from "lucide-react";

export function ContactForm() {
  const [isSuccess, setIsSuccess] = useState(false);
  const [serverError, setServerError] = useState("");

  const {
    register,
    handleSubmit,
    reset,
    formState: { errors, isSubmitting },
  } = useForm<ContactInput>({
    resolver: zodResolver(contactSchema),
    defaultValues: {
      name: "",
      email: "",
      service: "",
      budget: "",
      message: "",
      company_url: "",
    },
  });

  const onSubmit = async (data: ContactInput) => {
    setServerError("");

    try {
      const response = await fetch("/api/contact", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      });

      const resData = await response.json();

      if (!response.ok) {
        throw new Error(resData.error || "Failed to submit inquiry.");
      }

      setIsSuccess(true);
      reset();
    } catch (err: unknown) {
      const errorMessage =
        err instanceof Error
          ? err.message
          : "An unexpected error occurred. Please try again.";
      setServerError(errorMessage);
    }
  };

  if (isSuccess) {
    return (
      <div className="rounded-[var(--radius-lg)] border border-emerald-500/30 bg-emerald-500/10 p-8 text-center animate-fade-in">
        <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-emerald-500/20 text-emerald-600 dark:text-emerald-400">
          <CheckCircle2 size={28} />
        </div>
        <h3 className="mt-4 font-heading text-xl font-bold text-text">
          Message Received!
        </h3>
        <p className="mt-2 text-sm text-text-muted max-w-md mx-auto">
          Thank you for reaching out. We have received your inquiry and will
          review your project details and respond within one business day.
        </p>
        <button
          type="button"
          onClick={() => setIsSuccess(false)}
          className="mt-6 inline-flex h-9 items-center justify-center rounded-[var(--radius-sm)] border border-border bg-bg px-4 text-xs font-medium text-text transition-colors hover:bg-surface"
        >
          Send another message
        </button>
      </div>
    );
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-5" noValidate>
      {/* Honeypot field */}
      <div className="sr-only" aria-hidden="true">
        <label htmlFor="company_url">Company URL</label>
        <input
          type="text"
          id="company_url"
          {...register("company_url")}
          tabIndex={-1}
          autoComplete="off"
        />
      </div>

      {serverError && (
        <div
          className="flex items-center gap-2 rounded-[var(--radius-md)] border border-rose-500/30 bg-rose-500/10 p-4 text-sm text-rose-600 dark:text-rose-400"
          role="alert"
        >
          <AlertCircle size={18} className="shrink-0" />
          <span>{serverError}</span>
        </div>
      )}

      {/* Name */}
      <div>
        <label
          htmlFor="name"
          className="mb-1.5 block text-sm font-medium text-text"
        >
          Full Name <span className="text-rose-500">*</span>
        </label>
        <input
          type="text"
          id="name"
          {...register("name")}
          aria-invalid={!!errors.name}
          disabled={isSubmitting}
          className={`h-11 w-full rounded-[var(--radius-sm)] border bg-bg px-3.5 text-sm text-text placeholder:text-text-muted focus:outline-none focus:ring-2 disabled:opacity-60 ${
            errors.name
              ? "border-rose-500 focus:ring-rose-500/20"
              : "border-border focus:border-accent focus:ring-accent/20"
          }`}
          placeholder="e.g. Jane Doe"
        />
        {errors.name && (
          <p className="mt-1 text-xs text-rose-500">{errors.name.message}</p>
        )}
      </div>

      {/* Email */}
      <div>
        <label
          htmlFor="email"
          className="mb-1.5 block text-sm font-medium text-text"
        >
          Work Email <span className="text-rose-500">*</span>
        </label>
        <input
          type="email"
          id="email"
          {...register("email")}
          aria-invalid={!!errors.email}
          disabled={isSubmitting}
          className={`h-11 w-full rounded-[var(--radius-sm)] border bg-bg px-3.5 text-sm text-text placeholder:text-text-muted focus:outline-none focus:ring-2 disabled:opacity-60 ${
            errors.email
              ? "border-rose-500 focus:ring-rose-500/20"
              : "border-border focus:border-accent focus:ring-accent/20"
          }`}
          placeholder="jane@company.com"
        />
        {errors.email && (
          <p className="mt-1 text-xs text-rose-500">{errors.email.message}</p>
        )}
      </div>

      {/* Service interest */}
      <div>
        <label
          htmlFor="service"
          className="mb-1.5 block text-sm font-medium text-text"
        >
          Service Interest <span className="text-rose-500">*</span>
        </label>
        <select
          id="service"
          {...register("service")}
          aria-invalid={!!errors.service}
          disabled={isSubmitting}
          className={`h-11 w-full rounded-[var(--radius-sm)] border bg-bg px-3 text-sm text-text focus:outline-none focus:ring-2 disabled:opacity-60 ${
            errors.service
              ? "border-rose-500 focus:ring-rose-500/20"
              : "border-border focus:border-accent focus:ring-accent/20"
          }`}
        >
          <option value="">Select a service category…</option>
          {siteConfig.services.map((s) => (
            <option key={s.title} value={s.title}>
              {s.title}
            </option>
          ))}
          <option value="Custom Advisory">Custom Advisory / Retainer</option>
          <option value="General Inquiry">General Inquiry / Other</option>
        </select>
        {errors.service && (
          <p className="mt-1 text-xs text-rose-500">{errors.service.message}</p>
        )}
      </div>

      {/* Budget range (optional) */}
      <div>
        <label
          htmlFor="budget"
          className="mb-1.5 block text-sm font-medium text-text"
        >
          Target Budget <span className="text-text-muted font-normal">(optional)</span>
        </label>
        <select
          id="budget"
          {...register("budget")}
          disabled={isSubmitting}
          className="h-11 w-full rounded-[var(--radius-sm)] border border-border bg-bg px-3 text-sm text-text focus:border-accent focus:outline-none focus:ring-2 focus:ring-accent/20 disabled:opacity-60"
        >
          <option value="">Prefer not to disclose</option>
          <option value="Under $5,000">Under $5,000</option>
          <option value="$5,000 – $10,000">$5,000 – $10,000</option>
          <option value="$10,000 – $25,000">$10,000 – $25,000</option>
          <option value="$25,000+">$25,000+</option>
        </select>
      </div>

      {/* Message */}
      <div>
        <label
          htmlFor="message"
          className="mb-1.5 block text-sm font-medium text-text"
        >
          Project Details & Goals <span className="text-rose-500">*</span>
        </label>
        <textarea
          id="message"
          rows={5}
          {...register("message")}
          aria-invalid={!!errors.message}
          disabled={isSubmitting}
          className={`w-full rounded-[var(--radius-sm)] border bg-bg px-3.5 py-3 text-sm text-text placeholder:text-text-muted focus:outline-none focus:ring-2 disabled:opacity-60 ${
            errors.message
              ? "border-rose-500 focus:ring-rose-500/20"
              : "border-border focus:border-accent focus:ring-accent/20"
          }`}
          placeholder="Tell us about your current challenges, timeline, and what success looks like for this project…"
        />
        {errors.message && (
          <p className="mt-1 text-xs text-rose-500">{errors.message.message}</p>
        )}
      </div>

      <button
        type="submit"
        disabled={isSubmitting}
        className="inline-flex h-11 w-full items-center justify-center gap-2 rounded-[var(--radius-sm)] bg-accent px-8 text-sm font-medium text-accent-foreground transition-colors hover:bg-accent-hover disabled:opacity-60 sm:w-auto"
      >
        {isSubmitting ? (
          <>
            <Loader2 size={16} className="animate-spin" />
            <span>Sending Message…</span>
          </>
        ) : (
          <>
            <Send size={15} />
            <span>Send Message</span>
          </>
        )}
      </button>
    </form>
  );
}
