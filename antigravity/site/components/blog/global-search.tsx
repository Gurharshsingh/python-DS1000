"use client";

import { useEffect, useState } from "react";
import { SearchDialog, type SearchPostItem } from "./search-dialog";

export function GlobalSearch() {
  const [items, setItems] = useState<SearchPostItem[]>([]);

  useEffect(() => {
    fetch("/api/search")
      .then((res) => res.json())
      .then((data) => {
        if (Array.isArray(data)) {
          setItems(data);
        }
      })
      .catch((err) => console.error("Failed to load search index:", err));
  }, []);

  return <SearchDialog posts={items} />;
}
