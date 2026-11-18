import type { Metadata } from "next";
import { notFound } from "next/navigation";
import Link from "next/link";
import { siteConfig } from "@/lib/site-config";
import {
  getPostBySlug,
  getPostSlugs,
  getRelatedPosts,
  extractHeadings,
} from "@/lib/posts";
import { MDXContent } from "@/components/blog/mdx-content";
import { TableOfContents } from "@/components/blog/table-of-contents";
import { AuthorBox } from "@/components/blog/author-box";
import { ShareButtons } from "@/components/blog/share-buttons";
import { PostCard } from "@/components/blog/post-card";
import { ArticleJsonLd } from "@/components/seo/json-ld";
import { Calendar, Clock, ArrowLeft, Tag } from "lucide-react";

interface PostPageProps {
  params: Promise<{ slug: string }>;
}

export async function generateStaticParams() {
  const slugs = getPostSlugs();
  return slugs.map((slug) => ({ slug }));
}

export async function generateMetadata({
  params,
}: PostPageProps): Promise<Metadata> {
  const { slug } = await params;
  const post = getPostBySlug(slug);

  if (!post) {
    return {
      title: "Post Not Found",
    };
  }

  const { frontmatter } = post;
  const postUrl = `${siteConfig.url}/blog/${slug}`;

  return {
    title: frontmatter.title,
    description: frontmatter.description,
    authors: [{ name: frontmatter.author?.name || siteConfig.name }],
    openGraph: {
      title: frontmatter.title,
      description: frontmatter.description,
      type: "article",
      publishedTime: frontmatter.date,
      modifiedTime: frontmatter.updated || frontmatter.date,
      authors: [frontmatter.author?.name || siteConfig.name],
      tags: frontmatter.tags,
      url: postUrl,
    },
    twitter: {
      card: "summary_large_image",
      title: frontmatter.title,
      description: frontmatter.description,
    },
    alternates: {
      canonical: postUrl,
    },
  };
}

export default async function BlogPostPage({ params }: PostPageProps) {
  const { slug } = await params;
  const post = getPostBySlug(slug);

  if (!post) {
    notFound();
  }

  const { frontmatter, content, readingTime } = post;
  const headings = extractHeadings(content);
  const relatedPosts = getRelatedPosts(slug, frontmatter.tags, 2);
  const postUrl = `${siteConfig.url}/blog/${slug}`;

  return (
    <article className="bg-bg px-4 py-12 sm:px-6 sm:py-20 lg:px-8">
      <ArticleJsonLd post={post} />
      <div className="mx-auto max-w-[1200px]">
        {/* Back Link */}
        <Link
          href="/blog"
          className="inline-flex items-center gap-1.5 text-sm font-medium text-text-muted transition-colors hover:text-text"
        >
          <ArrowLeft size={16} /> Back to all articles
        </Link>

        {/* Post Header */}
        <header className="mt-8 max-w-4xl">
          {/* Tags */}
          <div className="flex flex-wrap items-center gap-2">
            {frontmatter.tags.map((tag) => (
              <Link
                key={tag}
                href={`/blog/tag/${encodeURIComponent(tag.toLowerCase())}`}
                className="inline-flex items-center gap-1 rounded-full bg-surface border border-border px-3 py-1 text-xs font-medium text-text-muted transition-colors hover:text-text hover:border-accent/40"
              >
                <Tag size={12} className="text-accent" />
                {tag}
              </Link>
            ))}
          </div>

          {/* Title */}
          <h1 className="mt-4 font-heading text-3xl font-bold tracking-tight text-text sm:text-4xl lg:text-5xl lg:leading-[1.15]">
            {frontmatter.title}
          </h1>

          {/* Subtitle / Description */}
          <p className="mt-4 text-lg text-text-muted leading-relaxed sm:text-xl">
            {frontmatter.description}
          </p>

          {/* Meta bar */}
          <div className="mt-6 flex flex-wrap items-center justify-between gap-4 border-y border-border py-4 text-sm text-text-muted">
            <div className="flex items-center gap-6">
              <span className="font-medium text-text">
                {frontmatter.author?.name}
              </span>
              <span className="flex items-center gap-1.5">
                <Calendar size={15} />
                <time dateTime={frontmatter.date}>
                  {new Date(frontmatter.date).toLocaleDateString("en-US", {
                    month: "long",
                    day: "numeric",
                    year: "numeric",
                  })}
                </time>
              </span>
              <span className="flex items-center gap-1.5">
                <Clock size={15} />
                {readingTime}
              </span>
            </div>

            <ShareButtons title={frontmatter.title} url={postUrl} />
          </div>
        </header>

        {/* Main Content & Sidebar */}
        <div className="mt-12 grid gap-12 lg:grid-cols-12">
          {/* Content Body */}
          <div className="lg:col-span-8">
            <MDXContent source={content} />

            {/* Post Footer */}
            <div className="mt-16 space-y-8 border-t border-border pt-8">
              <div className="flex items-center justify-between">
                <span className="text-sm font-semibold uppercase tracking-wider text-text-muted">
                  Enjoyed this article?
                </span>
                <ShareButtons title={frontmatter.title} url={postUrl} />
              </div>

              {/* Author Box */}
              <AuthorBox author={frontmatter.author} />

              {/* Inline Newsletter Box */}
              <div className="rounded-[var(--radius-lg)] border border-accent/20 bg-surface p-6 sm:p-8 text-center">
                <h3 className="font-heading text-xl font-bold text-text">
                  Subscribe to The Meridian Dispatch
                </h3>
                <p className="mt-2 text-sm text-text-muted max-w-md mx-auto">
                  Get high-signal frameworks and essays delivered directly to
                  your inbox twice a month.
                </p>
                <div className="mt-5 flex justify-center">
                  <Link
                    href="/newsletter"
                    className="inline-flex h-10 items-center justify-center rounded-[var(--radius-sm)] bg-accent px-5 text-sm font-medium text-accent-foreground transition-colors hover:bg-accent-hover"
                  >
                    Get Free Insights
                  </Link>
                </div>
              </div>
            </div>
          </div>

          {/* Sidebar */}
          <aside className="space-y-8 lg:col-span-4">
            {/* Sticky Table of Contents */}
            {headings.length > 0 && (
              <div className="sticky top-24">
                <TableOfContents headings={headings} />

                {/* Consultation teaser */}
                <div className="mt-6 rounded-[var(--radius-lg)] border border-border bg-surface p-6">
                  <h4 className="font-heading font-semibold text-text">
                    Ready to scale your firm?
                  </h4>
                  <p className="mt-2 text-xs leading-relaxed text-text-muted">
                    We partner with ambitious founders to productize services and
                    build predictable inbound pipelines.
                  </p>
                  <Link
                    href="/contact"
                    className="mt-4 block text-center rounded-[var(--radius-sm)] bg-accent/10 border border-accent/30 py-2 text-xs font-semibold text-accent transition-colors hover:bg-accent hover:text-accent-foreground"
                  >
                    Schedule a Discovery Call
                  </Link>
                </div>
              </div>
            )}
          </aside>
        </div>

        {/* Related Posts */}
        {relatedPosts.length > 0 && (
          <div className="mt-24 border-t border-border pt-12">
            <h2 className="font-heading text-2xl font-bold text-text">
              Related Articles
            </h2>
            <div className="mt-6 grid gap-6 sm:grid-cols-2">
              {relatedPosts.map((related) => (
                <PostCard key={related.slug} post={related} />
              ))}
            </div>
          </div>
        )}
      </div>
    </article>
  );
}
