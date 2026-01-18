import { writable, derived } from "svelte/store";

export interface Tab {
  id: string;
  title: string;
  type: "markdown" | "slides";
  content: string;
}

export const tabs = writable<Tab[]>([
  {
    id: "1",
    title: "Introduction.md",
    type: "markdown",
    content: "# Welcome to DocsEngn\n\nThis is a Tiptap based markdown editor.",
  },
]);

export const activeTabId = writable<string>("1");

export const activeTab = derived([tabs, activeTabId], ([$tabs, $activeTabId]) =>
  $tabs.find((t) => t.id === $activeTabId),
);

export function updateTabContent(id: string, content: string) {
  tabs.update((t) =>
    t.map((tab) => (tab.id === id ? { ...tab, content } : tab)),
  );
}

export const editorAction = writable<{ type: string; payload?: any } | null>(
  null,
);

export const drawerOpen = writable(false);
