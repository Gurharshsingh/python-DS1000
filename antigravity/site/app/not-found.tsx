import Link from "next/link";

export default function NotFound() {
  return (
    <section className="flex flex-1 flex-col items-center justify-center bg-bg px-4 py-24 text-center">
      <p className="text-6xl font-bold text-accent">404</p>
      <h1 className="mt-4 font-heading text-2xl font-bold text-text sm:text-3xl">
        Page Not Found
      </h1>
      <p className="mt-3 max-w-md text-text-muted">
        Sorry, the page you&apos;re looking for doesn&apos;t exist or has been
        moved.
      </p>
      <Link
        href="/"
        className="mt-6 inline-flex rounded-[var(--radius-sm)] bg-accent px-6 py-3 text-sm font-medium text-accent-foreground transition-colors duration-150 hover:bg-accent-hover"
      >
        Go Home
      </Link>
    </section>
  );
}
