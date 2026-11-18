import { describe, it, expect } from "vitest";
import { newsletterSchema, contactSchema } from "../lib/validators";

describe("Newsletter Validation Schema", () => {
  it("should validate a valid email", () => {
    const result = newsletterSchema.safeParse({
      email: "user@example.com",
    });
    expect(result.success).toBe(true);
  });

  it("should reject an invalid email", () => {
    const result = newsletterSchema.safeParse({
      email: "invalid-email",
    });
    expect(result.success).toBe(false);
  });

  it("should reject empty email", () => {
    const result = newsletterSchema.safeParse({
      email: "",
    });
    expect(result.success).toBe(false);
  });

  it("should detect bot honeypot submission", () => {
    const result = newsletterSchema.safeParse({
      email: "bot@example.com",
      website: "http://spam-link.com",
    });
    expect(result.success).toBe(false);
  });
});

describe("Contact Form Validation Schema", () => {
  it("should validate complete valid contact inquiry", () => {
    const result = contactSchema.safeParse({
      name: "Alex Morgan",
      email: "alex@company.com",
      service: "Growth Strategy",
      budget: "$10,000 – $25,000",
      message: "We need a comprehensive strategic growth sprint for Q3.",
    });
    expect(result.success).toBe(true);
  });

  it("should reject messages that are too short", () => {
    const result = contactSchema.safeParse({
      name: "Alex",
      email: "alex@company.com",
      service: "Growth Strategy",
      message: "Hi",
    });
    expect(result.success).toBe(false);
  });

  it("should reject names that are too short", () => {
    const result = contactSchema.safeParse({
      name: "A",
      email: "alex@company.com",
      service: "Growth Strategy",
      message: "This is a legitimate message with enough characters.",
    });
    expect(result.success).toBe(false);
  });

  it("should detect honeypot company_url", () => {
    const result = contactSchema.safeParse({
      name: "Spam Bot",
      email: "bot@spam.com",
      service: "Growth Strategy",
      message: "This is spam content message.",
      company_url: "https://spam.bot",
    });
    expect(result.success).toBe(false);
  });
});
