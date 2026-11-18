import type { Metadata } from "next";
import Link from "next/link";
import { siteConfig } from "@/lib/site-config";
import { getAllPosts, getAllTags } from "@/lib/posts";
import { PostCard } from "@/components/blog/post-card";
import { Sparkles, BookOpen } from "lucide-react";

export const metadata: Metadata = {
  title: "Blog & Strategic Insights",
  description:
    "Actionable frameworks, teardowns, and guides on growth strategy, digital presence, and brand positioning.",
};

export default async function BlogPage() {
  const posts = getAllPosts();
  const tags = getAllTags();

  const featuredPost = posts.find((p) => p.frontmatter.featured) || posts[0];
  const regularPosts = posts.filter((p) => p.slug !== featuredPost?.slug);

  return (
    <div className="bg-bg px-4 py-16 sm:px-6 sm:py-24 lg:px-8">
      <div className="mx-auto max-w-[1200px]">
        {/* Page Header */}
        <div className="max-w-2xl">
          <div className="inline-flex items-center gap-2 rounded-full border border-border bg-surface px-3 py-1 text-xs font-medium text-accent">
            <BookOpen size={14} />
            <span>The Meridian Journal</span>
          </div>
          <h1 className="mt-4 font-heading text-4xl font-bold tracking-tight text-text sm:text-5xl">
            Articles & Frameworks
          </h1>
          <p className="mt-4 text-lg text-text-muted">
            Tactical essays on building audience leverage, productizing services,
            and commanding premium market positioning.
          </p>
        </div>

        {/* Tag Filters */}
        {tags.length > 0 && (
          <div className="mt-10 flex flex-wrap items-center gap-2 border-b border-border pb-6">
            <span className="text-xs font-semibold uppercase tracking-wider text-text-muted mr-2">
              Topics:
            </span>
            <Link
              href="/blog"
              className="rounded-full bg-accent px-3 py-1 text-xs font-medium text-accent-foreground"
            >
              All ({posts.length})
            </Link>
            {tags.map(({ tag, count }) => (
              <Link
                key={tag}
                href={`/blog/tag/${encodeURIComponent(tag)}`}
                className="rounded-full border border-border bg-surface px-3 py-1 text-xs font-medium text-text-muted transition-colors hover:border-accent/40 hover:text-text"
              >
                {tag} ({count})
              </Link>
            ))}
          </div>
        )}

        {/* Featured Post (Hero) */}
        {featuredPost && (
          <div className="mt-12">
            <div className="mb-4 flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-accent">
              <Sparkles size={14} />
              Featured Insight
            </div>
            <PostCard post={featuredPost} featured={true} />
          </div>
        )}

        {/* Regular Posts Grid */}
        <div className="mt-16">
          <h2 className="font-heading text-xl font-bold text-text mb-6">
            Latest Articles
          </h2>
          {regularPosts.length > 0 ? (
            <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-2">
              {regularPosts.map((post) => (
                <PostCard key={post.slug} post={post} />
              ))}
            </div>
          ) : (
            <p className="text-sm text-text-muted">
              More articles coming soon. Subscribe to our newsletter to get notified.
            </p>
          )}
        </div>

        {/* Newsletter Box */}
        <div className="mt-20 rounded-[var(--radius-xl)] border border-accent/20 bg-surface p-8 sm:p-12 text-center">
          <h3 className="font-heading text-2xl font-bold text-text sm:text-3xl">
            Get practical growth tactics in your inbox
          </h3>
          <p className="mx-auto mt-3 max-w-xl text-sm text-text-muted">
            Join founders and agency leaders receiving our bi-weekly breakdown of
            what is working in modern service growth. No spam, unsubscribe anytime.
          </p>
          <div className="mt-6 flex justify-center">
            <Link
              href="/newsletter"
              className="inline-flex h-11 items-center justify-center rounded-[var(--radius-sm)] bg-accent px-6 text-sm font-medium text-accent-foreground transition-colors hover:bg-accent-hover"
            >
              Subscribe to Newsletter
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
