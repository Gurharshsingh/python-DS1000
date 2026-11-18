import Link from "next/link";
import { Calendar, Clock, ArrowRight } from "lucide-react";
import type { Post } from "@/lib/posts";

interface PostCardProps {
  post: Post;
  featured?: boolean;
}

export function PostCard({ post, featured = false }: PostCardProps) {
  const { slug, frontmatter, readingTime } = post;

  return (
    <article
      className={`group relative flex flex-col justify-between rounded-[var(--radius-lg)] border border-border bg-surface p-6 transition-all duration-200 hover:-translate-y-1 hover:border-accent/40 hover:shadow-md ${
        featured ? "md:p-8 bg-surface/90 border-accent/30" : ""
      }`}
    >
      <div>
        {/* Tags & Featured pill */}
        <div className="flex flex-wrap items-center gap-2">
          {featured && (
            <span className="rounded-full bg-accent/15 px-2.5 py-0.5 text-xs font-semibold text-accent">
              Featured
            </span>
          )}
          {frontmatter.tags.slice(0, 3).map((tag) => (
            <Link
              key={tag}
              href={`/blog/tag/${encodeURIComponent(tag.toLowerCase())}`}
              className="z-10 rounded-full bg-bg px-2.5 py-0.5 text-xs font-medium text-text-muted transition-colors hover:text-text"
            >
              {tag}
            </Link>
          ))}
        </div>

        {/* Title */}
        <h3
          className={`mt-4 font-heading font-bold text-text group-hover:text-accent transition-colors duration-150 ${
            featured ? "text-2xl sm:text-3xl" : "text-xl"
          }`}
        >
          <Link href={`/blog/${slug}`} className="focus:outline-none">
            <span className="absolute inset-0" aria-hidden="true" />
            {frontmatter.title}
          </Link>
        </h3>

        {/* Description */}
        <p className="mt-3 text-sm leading-relaxed text-text-muted line-clamp-3">
          {frontmatter.description}
        </p>
      </div>

      {/* Footer Meta */}
      <div className="mt-6 flex items-center justify-between border-t border-border pt-4 text-xs text-text-muted">
        <div className="flex items-center gap-4">
          <span className="flex items-center gap-1.5">
            <Calendar size={14} className="shrink-0" />
            <time dateTime={frontmatter.date}>
              {new Date(frontmatter.date).toLocaleDateString("en-US", {
                month: "short",
                day: "numeric",
                year: "numeric",
              })}
            </time>
          </span>
          <span className="flex items-center gap-1.5">
            <Clock size={14} className="shrink-0" />
            {readingTime}
          </span>
        </div>

        <span className="flex items-center gap-1 font-medium text-accent opacity-0 transition-opacity duration-150 group-hover:opacity-100">
          Read article <ArrowRight size={14} />
        </span>
      </div>
    </article>
  );
}
