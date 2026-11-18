import { NextRequest, NextResponse } from "next/server";
import { newsletterSchema } from "@/lib/validators";
import { rateLimit } from "@/lib/rate-limit";

export async function POST(request: NextRequest) {
  try {
    const ip = request.headers.get("x-forwarded-for") || "127.0.0.1";
    const rl = await rateLimit(`subscribe:${ip}`, 5, 60 * 1000);

    if (!rl.success) {
      return NextResponse.json(
        { error: "Too many subscription attempts. Please try again in a minute." },
        { status: 429 }
      );
    }

    const body = await request.json();
    const result = newsletterSchema.safeParse(body);

    if (!result.success) {
      const errorMsg = result.error.issues?.[0]?.message || "Invalid input";
      return NextResponse.json({ error: errorMsg }, { status: 400 });
    }

    const { email, website } = result.data;

    // Honeypot check
    if (website && website.length > 0) {
      // Return 200 silently to prevent bots from discovering honeypot
      return NextResponse.json({ message: "Subscription successful" });
    }

    const apiKey = process.env.BUTTONDOWN_API_KEY;

    if (!apiKey) {
      // In development or when key is not configured, log and return simulated success
      console.log(`[DEV/PREVIEW] Newsletter subscription received for: ${email}`);
      return NextResponse.json({
        message: "Check your inbox to confirm your subscription.",
        isDemo: true,
      });
    }

    // Call Buttondown API
    const response = await fetch("https://api.buttondown.email/v1/subscribers", {
      method: "POST",
      headers: {
        Authorization: `Token ${apiKey}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        email,
        tags: ["website-subscriber"],
      }),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      if (response.status === 400 && JSON.stringify(errorData).includes("already")) {
        return NextResponse.json(
          { message: "You are already subscribed to the newsletter!" },
          { status: 200 }
        );
      }
      return NextResponse.json(
        { error: "Unable to process subscription. Please try again later." },
        { status: response.status }
      );
    }

    return NextResponse.json({
      message: "Check your inbox to confirm your subscription.",
    });
  } catch (error) {
    console.error("Subscription error:", error);
    return NextResponse.json(
      { error: "Internal server error. Please try again later." },
      { status: 500 }
    );
  }
}
