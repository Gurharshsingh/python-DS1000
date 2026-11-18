import { NextResponse } from "next/server";
import { siteConfig } from "@/lib/site-config";
import { getAllPosts } from "@/lib/posts";

export async function GET() {
  const posts = getAllPosts(false);
  const baseUrl = siteConfig.url;

  const rssItems = posts
    .map((post) => {
      const postUrl = `${baseUrl}/blog/${post.slug}`;
      const pubDate = new Date(post.frontmatter.date).toUTCString();
      const author = post.frontmatter.author?.name || siteConfig.name;

      return `
    <item>
      <title><![CDATA[${post.frontmatter.title}]]></title>
      <link>${postUrl}</link>
      <guid isPermaLink="true">${postUrl}</guid>
      <description><![CDATA[${post.frontmatter.description}]]></description>
      <pubDate>${pubDate}</pubDate>
      <author><![CDATA[${author}]]></author>
      ${post.frontmatter.tags
        .map((tag) => `<category><![CDATA[${tag}]]></category>`)
        .join("\n      ")}
    </item>`;
    })
    .join("\n");

  const rssXml = `<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title><![CDATA[${siteConfig.name} - ${siteConfig.tagline}]]></title>
    <link>${baseUrl}</link>
    <description><![CDATA[${siteConfig.description}]]></description>
    <language>en-US</language>
    <lastBuildDate>${new Date().toUTCString()}</lastBuildDate>
    <atom:link href="${baseUrl}/rss.xml" rel="self" type="application/rss+xml"/>
    ${rssItems}
  </channel>
</rss>`;

  return new NextResponse(rssXml.trim(), {
    headers: {
      "Content-Type": "application/xml; charset=utf-8",
      "Cache-Control": "s-maxage=3600, stale-while-revalidate",
    },
  });
}
