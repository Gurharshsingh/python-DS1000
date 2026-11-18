import type { Author } from "@/lib/posts";

interface AuthorBoxProps {
  author?: Author;
}

export function AuthorBox({ author }: AuthorBoxProps) {
  if (!author) return null;

  return (
    <div className="flex items-center gap-4 rounded-[var(--radius-lg)] border border-border bg-surface p-6">
      <div className="flex h-14 w-14 shrink-0 items-center justify-center rounded-full bg-accent/15 text-lg font-bold text-accent">
        {author.name
          .split(" ")
          .map((n) => n[0])
          .join("")
          .toUpperCase()}
      </div>
      <div>
        <p className="font-heading font-semibold text-text">{author.name}</p>
        {author.role && (
          <p className="text-xs font-medium text-accent">{author.role}</p>
        )}
        {author.bio && (
          <p className="mt-1.5 text-xs text-text-muted leading-relaxed">
            {author.bio}
          </p>
        )}
      </div>
    </div>
  );
}
