import React from "react";
import Link from "next/link";
import { MDXRemote } from "next-mdx-remote/rsc";
import remarkGfm from "remark-gfm";
import rehypeSlug from "rehype-slug";
import rehypeAutolinkHeadings from "rehype-autolink-headings";
import { Callout } from "./callout";

// Custom MDX components mapping
const mdxComponents = {
  Callout,
  a: ({ href = "", children, ...props }: React.AnchorHTMLAttributes<HTMLAnchorElement>) => {
    const isInternal = href.startsWith("/") || href.startsWith("#");
    if (isInternal) {
      return (
        <Link
          href={href}
          className="font-medium text-accent underline underline-offset-4 decoration-accent/40 hover:decoration-accent"
          {...props}
        >
          {children}
        </Link>
      );
    }
    return (
      <a
        href={href}
        target="_blank"
        rel="noopener noreferrer"
        className="font-medium text-accent underline underline-offset-4 decoration-accent/40 hover:decoration-accent"
        {...props}
      >
        {children}
      </a>
    );
  },
  h2: ({ id, children, ...props }: React.HTMLAttributes<HTMLHeadingElement>) => (
    <h2
      id={id}
      className="mt-10 mb-4 font-heading text-2xl font-bold tracking-tight text-text scroll-mt-24 border-b border-border/60 pb-2"
      {...props}
    >
      {children}
    </h2>
  ),
  h3: ({ id, children, ...props }: React.HTMLAttributes<HTMLHeadingElement>) => (
    <h3
      id={id}
      className="mt-8 mb-3 font-heading text-xl font-semibold tracking-tight text-text scroll-mt-24"
      {...props}
    >
      {children}
    </h3>
  ),
  p: ({ children, ...props }: React.HTMLAttributes<HTMLParagraphElement>) => (
    <p className="my-4 text-base leading-relaxed text-text/90" {...props}>
      {children}
    </p>
  ),
  ul: ({ children, ...props }: React.HTMLAttributes<HTMLUListElement>) => (
    <ul className="my-4 ml-6 list-disc space-y-2 text-text/90 text-base" {...props}>
      {children}
    </ul>
  ),
  ol: ({ children, ...props }: React.HTMLAttributes<HTMLOListElement>) => (
    <ol className="my-4 ml-6 list-decimal space-y-2 text-text/90 text-base" {...props}>
      {children}
    </ol>
  ),
  blockquote: ({ children, ...props }: React.HTMLAttributes<HTMLQuoteElement>) => (
    <blockquote
      className="my-6 border-l-4 border-accent pl-4 italic text-text-muted bg-surface/40 py-2 rounded-r-[var(--radius-sm)]"
      {...props}
    >
      {children}
    </blockquote>
  ),
  pre: ({ children, ...props }: React.HTMLAttributes<HTMLPreElement>) => (
    <pre
      className="my-6 overflow-x-auto rounded-[var(--radius-md)] border border-border bg-[#0d1117] p-4 text-sm text-slate-100 font-mono"
      {...props}
    >
      {children}
    </pre>
  ),
  code: ({ className, children, ...props }: React.HTMLAttributes<HTMLElement>) => {
    const isInline = !className;
    if (isInline) {
      return (
        <code
          className="rounded-[var(--radius-sm)] bg-surface px-1.5 py-0.5 text-xs font-mono text-accent border border-border font-semibold"
          {...props}
        >
          {children}
        </code>
      );
    }
    return (
      <code className={className} {...props}>
        {children}
      </code>
    );
  },
  table: ({ children, ...props }: React.TableHTMLAttributes<HTMLTableElement>) => (
    <div className="my-6 overflow-x-auto">
      <table className="w-full text-left text-sm border-collapse border border-border" {...props}>
        {children}
      </table>
    </div>
  ),
  th: ({ children, ...props }: React.ThHTMLAttributes<HTMLTableCellElement>) => (
    <th className="border border-border bg-surface px-4 py-2 font-semibold text-text" {...props}>
      {children}
    </th>
  ),
  td: ({ children, ...props }: React.TdHTMLAttributes<HTMLTableCellElement>) => (
    <td className="border border-border px-4 py-2 text-text/90" {...props}>
      {children}
    </td>
  ),
  hr: (props: React.HTMLAttributes<HTMLHRElement>) => (
    <hr className="my-8 border-border" {...props} />
  ),
};

interface MDXContentProps {
  source: string;
}

export function MDXContent({ source }: MDXContentProps) {
  return (
    <div className="prose-custom max-w-none">
      <MDXRemote
        source={source}
        components={mdxComponents}
        options={{
          mdxOptions: {
            remarkPlugins: [remarkGfm],
            rehypePlugins: [
              rehypeSlug,
              [rehypeAutolinkHeadings, { behavior: "wrap" }],
            ],
          },
        }}
      />
    </div>
  );
}
