import { NextResponse } from "next/server";
import { getAllPosts } from "@/lib/posts";

export async function GET() {
  const posts = getAllPosts(false);
  const searchItems = posts.map((p) => ({
    slug: p.slug,
    title: p.frontmatter.title,
    description: p.frontmatter.description,
    tags: p.frontmatter.tags,
    date: p.frontmatter.date,
  }));

  return NextResponse.json(searchItems, {
    headers: {
      "Cache-Control": "public, s-maxage=3600, stale-while-revalidate=86400",
    },
  });
}
