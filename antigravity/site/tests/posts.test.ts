import { describe, it, expect } from "vitest";
import {
  getAllPosts,
  getPostBySlug,
  getFeaturedPosts,
  getAllTags,
  getPostsByTag,
  getRelatedPosts,
  extractHeadings,
} from "../lib/posts";

describe("Post Utilities", () => {
  it("should retrieve all posts", () => {
    const posts = getAllPosts(true);
    expect(posts.length).toBeGreaterThan(0);
    expect(posts[0]).toHaveProperty("slug");
    expect(posts[0].frontmatter).toHaveProperty("title");
    expect(posts[0].frontmatter).toHaveProperty("date");
  });

  it("should get single post by slug", () => {
    const post = getPostBySlug("growth-strategy-frameworks-for-founders");
    expect(post).not.toBeNull();
    expect(post?.frontmatter.title).toBe(
      "The 3-Pillar Growth Framework for Early-Stage Service Businesses"
    );
    expect(post?.readingTime).toBeDefined();
    expect(post?.wordCount).toBeGreaterThan(0);
  });

  it("should return null for non-existent post", () => {
    const post = getPostBySlug("non-existent-slug-12345");
    expect(post).toBeNull();
  });

  it("should return featured posts", () => {
    const featured = getFeaturedPosts(2);
    expect(featured.length).toBeLessThanOrEqual(2);
    expect(featured.length).toBeGreaterThan(0);
  });

  it("should aggregate tags and counts", () => {
    const tags = getAllTags();
    expect(tags.length).toBeGreaterThan(0);
    expect(tags[0]).toHaveProperty("tag");
    expect(tags[0]).toHaveProperty("count");
    expect(tags[0].count).toBeGreaterThan(0);
  });

  it("should filter posts by tag", () => {
    const strategyPosts = getPostsByTag("Strategy");
    expect(strategyPosts.length).toBeGreaterThan(0);
    strategyPosts.forEach((p) => {
      expect(
        p.frontmatter.tags.map((t) => t.toLowerCase())
      ).toContain("strategy");
    });
  });

  it("should find related posts based on shared tags", () => {
    const related = getRelatedPosts(
      "growth-strategy-frameworks-for-founders",
      ["Growth Strategy", "Consulting"],
      2
    );
    expect(related).toBeDefined();
  });

  it("should extract markdown headings for Table of Contents", () => {
    const sampleMarkdown = `
# Title
Intro text

## First Section
Section 1 text

### Subsection 1.1
Subtext

## Second Section
Section 2 text
`;
    const headings = extractHeadings(sampleMarkdown);
    expect(headings.length).toBe(3);
    expect(headings[0]).toEqual({
      id: "first-section",
      text: "First Section",
      level: 2,
    });
    expect(headings[1]).toEqual({
      id: "subsection-11",
      text: "Subsection 1.1",
      level: 3,
    });
    expect(headings[2]).toEqual({
      id: "second-section",
      text: "Second Section",
      level: 2,
    });
  });
});
