import { NextRequest, NextResponse } from "next/server";
import { contactSchema } from "@/lib/validators";
import { rateLimit } from "@/lib/rate-limit";

export async function POST(request: NextRequest) {
  try {
    const ip = request.headers.get("x-forwarded-for") || "127.0.0.1";
    const rl = await rateLimit(`contact:${ip}`, 3, 60 * 1000);

    if (!rl.success) {
      return NextResponse.json(
        { error: "Too many messages sent. Please wait a minute before trying again." },
        { status: 429 }
      );
    }

    const body = await request.json();
    const result = contactSchema.safeParse(body);

    if (!result.success) {
      const errorMsg = result.error.issues?.[0]?.message || "Invalid input";
      return NextResponse.json({ error: errorMsg }, { status: 400 });
    }

    const { name, email, service, budget, message, company_url } = result.data;

    // Honeypot check
    if (company_url && company_url.length > 0) {
      return NextResponse.json({ message: "Thank you for reaching out!" });
    }

    const resendApiKey = process.env.RESEND_API_KEY;
    const contactTo = process.env.CONTACT_TO_EMAIL || "hello@example.com";
    const contactFrom = process.env.CONTACT_FROM_EMAIL || "contact@example.com";

    if (!resendApiKey) {
      console.log(
        `[DEV/PREVIEW] Contact Form Submission:\nFrom: ${name} <${email}>\nService: ${service}\nBudget: ${budget}\nMessage: ${message}`
      );
      return NextResponse.json({
        message: "Thank you for your message! We'll get back to you within one business day.",
        isDemo: true,
      });
    }

    // Call Resend API to send email notification
    const res = await fetch("https://api.resend.com/emails", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${resendApiKey}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        from: contactFrom,
        to: contactTo,
        reply_to: email,
        subject: `[New Inquiry] ${service} from ${name}`,
        text: `Name: ${name}\nEmail: ${email}\nService Interest: ${service}\nBudget: ${budget || "Not specified"}\n\nMessage:\n${message}`,
      }),
    });

    if (!res.ok) {
      console.error("Resend API error:", await res.text());
      return NextResponse.json(
        { error: "Failed to send message via email service. Please try again later." },
        { status: 500 }
      );
    }

    return NextResponse.json({
      message: "Thank you for reaching out! We will respond within one business day.",
    });
  } catch (error) {
    console.error("Contact form error:", error);
    return NextResponse.json(
      { error: "Internal server error. Please try again later." },
      { status: 500 }
    );
  }
}
