<script>
  import { onMount } from 'svelte';
  import { FileText, Folder, RefreshCw } from 'lucide-svelte';
  import { activeTabId, tabs } from '$lib/stores';

  let files = [];
  let loading = false;
  let error = null;

  async function loadFiles() {
    loading = true;
    error = null;
    try {
      const res = await fetch('/api/files');
      if (!res.ok) throw new Error('Failed to load files');
      files = await res.json();
    } catch (e) {
      error = e.message;
    } finally {
      loading = false;
    }
  }

  async function openFile(filename) {
    // Check if tab exists
    let tab = $tabs.find(t => t.title === filename); // Using title as ID/Key for now roughly
    if (tab) {
      activeTabId.set(tab.id);
      return;
    }

    try {
      const res = await fetch(`/api/content?filename=${encodeURIComponent(filename)}`);
      if (!res.ok) throw new Error('Failed to load content');
      const { content } = await res.json();

      const newId = crypto.randomUUID();
      const type = filename.endsWith('.md') ? 'markdown' : 'slides'; // Simple heuristic
      
      tabs.update(t => [...t, { 
        id: newId, 
        title: filename, 
        type, 
        content 
      }]);
      activeTabId.set(newId);
    } catch (e) {
      console.error('Error opening file:', e);
      alert('Error opening file: ' + e.message);
    }
  }

  onMount(loadFiles);
</script>

<div class="flex flex-col h-full">
  <div class="flex items-center justify-between px-2 py-2">
    <span class="text-xs font-semibold text-zinc-500 uppercase">Files</span>
    <button on:click={loadFiles} class="text-zinc-500 hover:text-zinc-300" title="Refresh">
      <RefreshCw size={14} class={loading ? 'animate-spin' : ''} />
    </button>
  </div>

  <div class="space-y-1 flex-1 overflow-y-auto px-2">
    {#if error}
      <div class="text-red-400 text-xs px-2">{error}</div>
    {/if}
    
    {#if files.length === 0 && !loading}
      <div class="text-zinc-500 text-xs px-2">No files found.</div>
    {/if}

    {#each files as item}
      <button 
        class="w-full flex items-center gap-2 px-2 py-1.5 text-zinc-400 hover:bg-zinc-800 rounded transition-colors group"
        on:click={() => item.type === 'file' ? openFile(item.name) : null}
      >
        {#if item.type === 'folder'}
          <Folder size={16} class="text-blue-400" />
        {:else}
          <FileText size={16} class="text-zinc-500 group-hover:text-zinc-300" />
        {/if}
        <span class="text-sm flex-1 text-left truncate">{item.name}</span>
      </button>
    {/each}
  </div>
</div>
