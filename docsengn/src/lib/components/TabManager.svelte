<script>
  import { PlusSquare, X } from 'lucide-svelte';
  import { tabs, activeTabId } from '$lib/stores';

  function addTab() {
    const id = globalThis.crypto.randomUUID();
    tabs.update(t => [...t, { id, title: 'New Doc.md', type: 'markdown', content: '' }]);
    activeTabId.set(id);
  }

  function closeTab(id) {
    tabs.update(t => {
      const filtered = t.filter(tab => tab.id !== id);
      if (filtered.length === 0) {
        const newId = globalThis.crypto.randomUUID();
        activeTabId.set(newId);
        return [{ id: newId, title: 'Untitled.md', type: 'markdown', content: '' }];
      }
      return filtered;
    });
    activeTabId.update(current => {
      if (current === id) {
        let lastTab;
        tabs.subscribe(v => lastTab = v[v.length - 1])();
        return lastTab.id;
      }
      return current;
    });
  }
</script>

<div class="h-10 border-b border-zinc-800 bg-zinc-900 flex items-center px-2 gap-1 overflow-x-auto">
  {#each $tabs as tab (tab.id)}
    <button
      on:click={() => activeTabId.set(tab.id)}
      class="px-3 py-1 text-sm flex items-center gap-2 min-w-[120px] max-w-[200px] border-t-2 transition-colors {tab.id === $activeTabId ? 'bg-zinc-800 border-blue-500 text-zinc-100' : 'bg-transparent border-transparent text-zinc-500 hover:bg-zinc-800 hover:text-zinc-300'}"
    >
      <span class="truncate">{tab.title}</span>
      <button 
        on:click|stopPropagation={() => closeTab(tab.id)}
        class="p-0.5 rounded-full hover:bg-zinc-700 transition-colors ml-auto"
      >
        <X size={14} />
      </button>
    </button>
  {/each}
  <button 
    on:click={addTab}
    class="p-1.5 text-zinc-500 hover:text-zinc-300 hover:bg-zinc-800 rounded-md transition-colors"
    title="New Document"
  >
    <PlusSquare size={18} />
  </button>
</div>
