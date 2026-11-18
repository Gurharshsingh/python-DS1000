import { siteConfig } from "@/lib/site-config";
import type { Post } from "@/lib/posts";

export function OrganizationJsonLd() {
  const schema = {
    "@context": "https://schema.org",
    "@type": "ProfessionalService",
    name: siteConfig.name,
    description: siteConfig.description,
    url: siteConfig.url,
    email: siteConfig.email,
    sameAs: [
      siteConfig.socials.twitter,
      siteConfig.socials.linkedin,
      siteConfig.socials.github,
    ],
  };

  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: JSON.stringify(schema) }}
    />
  );
}

export function ArticleJsonLd({ post }: { post: Post }) {
  const postUrl = `${siteConfig.url}/blog/${post.slug}`;
  const schema = {
    "@context": "https://schema.org",
    "@type": "BlogPosting",
    headline: post.frontmatter.title,
    description: post.frontmatter.description,
    url: postUrl,
    datePublished: post.frontmatter.date,
    dateModified: post.frontmatter.updated || post.frontmatter.date,
    author: {
      "@type": "Person",
      name: post.frontmatter.author?.name || siteConfig.name,
    },
    publisher: {
      "@type": "Organization",
      name: siteConfig.name,
      url: siteConfig.url,
    },
    keywords: post.frontmatter.tags.join(", "),
    mainEntityOfPage: {
      "@type": "WebPage",
      "@id": postUrl,
    },
  };

  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: JSON.stringify(schema) }}
    />
  );
}
