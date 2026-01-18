<script>
  import { onMount } from 'svelte';
  import { FileText, Folder, RefreshCw, FilePlus, FolderPlus, MonitorPlay } from 'lucide-svelte';
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

  async function createFolder() {
    const name = prompt('Folder Name:');
    if (!name) return;
    
    try {
      const res = await fetch('/api/files', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ path: name, message: `Create folder ${name}` })
      });
      if (!res.ok) throw new Error('Failed to create folder');
      await loadFiles();
    } catch (e) {
      alert(e.message);
    }
  }

  async function createFile(type) {
    const name = prompt(`File Name (e.g., my-doc${type === 'slides' ? '.slides.md' : '.md'}):`);
    if (!name) return;
    
    // Ensure extension
    let filename = name;
    if (type === 'slides' && !filename.endsWith('.md')) filename += '.md'; // Slidev uses .md too usually
    if (type === 'markdown' && !filename.endsWith('.md')) filename += '.md';

    const content = type === 'slides' 
      ? '# Slide 1\n\nWelcome to Slidev!\n\n---\n\n# Slide 2\n\nSecond slide' 
      : '# New Document\n\nStart writing...';

    try {
      const res = await fetch('/api/content', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          filename, 
          content,
          message: `Create ${filename}` 
        })
      });
      if (!res.ok) throw new Error('Failed to create file');
      await loadFiles();
      await openFile(filename);
    } catch (e) {
      alert(e.message);
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
      // Simple heuristic for slides: if filename contains 'slide' or we decide via metadata later.
      // For now, I'll rely on a naming convention or content check? 
      // Prompt said "Tailored to the type of open document (i.e. document vs slide)".
      // I'll assume if created as slide (via logic above) it might be hard to distinguish just by .md
      // But Slidev files are .md.
      // I'll check if content contains '---' separator as a hint, or just default to markdown.
      // Or maybe creating a file with specific extension like .slides.md is better.
      const isSlides = filename.includes('.slides') || content.includes('\n---\n'); 
      const type = isSlides ? 'slides' : 'markdown';
      
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
  <div class="flex items-center gap-1 px-2 py-2 border-b border-zinc-800 mb-2">
    <button on:click={() => createFile('markdown')} class="p-1.5 text-zinc-400 hover:text-blue-400 hover:bg-zinc-800 rounded transition-colors" title="New Document">
      <FilePlus size={16} />
    </button>
    <button on:click={() => createFile('slides')} class="p-1.5 text-zinc-400 hover:text-green-400 hover:bg-zinc-800 rounded transition-colors" title="New Slides">
      <MonitorPlay size={16} />
    </button>
    <button on:click={createFolder} class="p-1.5 text-zinc-400 hover:text-yellow-400 hover:bg-zinc-800 rounded transition-colors" title="New Folder">
      <FolderPlus size={16} />
    </button>
    <div class="flex-1"></div>
    <button on:click={loadFiles} class="p-1.5 text-zinc-500 hover:text-zinc-300 hover:bg-zinc-800 rounded transition-colors" title="Refresh">
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
