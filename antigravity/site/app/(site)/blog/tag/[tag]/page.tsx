import type { Metadata } from "next";
import Link from "next/link";
import { getAllTags, getPostsByTag } from "@/lib/posts";
import { PostCard } from "@/components/blog/post-card";
import { ArrowLeft, Tag as TagIcon } from "lucide-react";

interface TagPageProps {
  params: Promise<{ tag: string }>;
}

export async function generateStaticParams() {
  const tags = getAllTags();
  return tags.map(({ tag }) => ({ tag: encodeURIComponent(tag) }));
}

export async function generateMetadata({
  params,
}: TagPageProps): Promise<Metadata> {
  const { tag } = await params;
  const decodedTag = decodeURIComponent(tag);
  const formattedTag =
    decodedTag.charAt(0).toUpperCase() + decodedTag.slice(1);

  return {
    title: `Articles tagged "${formattedTag}"`,
    description: `Browse all articles, frameworks, and insights categorized under ${formattedTag}.`,
  };
}

export default async function TagPage({ params }: TagPageProps) {
  const { tag } = await params;
  const decodedTag = decodeURIComponent(tag);
  const posts = getPostsByTag(decodedTag);
  const allTags = getAllTags();

  return (
    <div className="bg-bg px-4 py-16 sm:px-6 sm:py-24 lg:px-8">
      <div className="mx-auto max-w-[1200px]">
        {/* Back link */}
        <Link
          href="/blog"
          className="inline-flex items-center gap-1.5 text-sm font-medium text-text-muted transition-colors hover:text-text"
        >
          <ArrowLeft size={16} /> Back to all articles
        </Link>

        {/* Header */}
        <div className="mt-8 max-w-2xl">
          <div className="inline-flex items-center gap-2 rounded-full border border-accent/30 bg-accent/10 px-3 py-1 text-xs font-semibold text-accent">
            <TagIcon size={14} />
            <span>Topic Archive</span>
          </div>
          <h1 className="mt-4 font-heading text-3xl font-bold tracking-tight text-text sm:text-4xl">
            Articles tagged with &ldquo;{decodedTag}&rdquo;
          </h1>
          <p className="mt-3 text-text-muted">
            Found {posts.length} {posts.length === 1 ? "article" : "articles"} in this category.
          </p>
        </div>

        {/* Other Tags Bar */}
        {allTags.length > 1 && (
          <div className="mt-8 flex flex-wrap items-center gap-2 border-b border-border pb-6">
            <span className="text-xs font-semibold uppercase tracking-wider text-text-muted mr-2">
              Other Topics:
            </span>
            <Link
              href="/blog"
              className="rounded-full border border-border bg-surface px-3 py-1 text-xs font-medium text-text-muted hover:text-text"
            >
              All Articles
            </Link>
            {allTags
              .filter((t) => t.tag !== decodedTag.toLowerCase())
              .map(({ tag: otherTag, count }) => (
                <Link
                  key={otherTag}
                  href={`/blog/tag/${encodeURIComponent(otherTag)}`}
                  className="rounded-full border border-border bg-surface px-3 py-1 text-xs font-medium text-text-muted transition-colors hover:border-accent/40 hover:text-text"
                >
                  {otherTag} ({count})
                </Link>
              ))}
          </div>
        )}

        {/* Posts List */}
        <div className="mt-12">
          {posts.length > 0 ? (
            <div className="grid gap-6 sm:grid-cols-2">
              {posts.map((post) => (
                <PostCard key={post.slug} post={post} />
              ))}
            </div>
          ) : (
            <div className="rounded-[var(--radius-lg)] border border-border bg-surface p-12 text-center">
              <p className="text-text-muted">
                No articles found with this tag.
              </p>
              <Link
                href="/blog"
                className="mt-4 inline-block text-sm font-medium text-accent hover:text-accent-hover"
              >
                View all articles →
              </Link>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
