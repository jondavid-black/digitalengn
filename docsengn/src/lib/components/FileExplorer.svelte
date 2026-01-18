<script>
  import { FileText, Folder } from 'lucide-svelte';

  // Mock data - will be replaced by API calls later
  let files = [
    { name: 'Introduction.md', type: 'markdown' },
    { name: 'Project-Proposal.md', type: 'markdown' },
    { name: 'Slides', type: 'folder', children: [
      { name: 'Weekly-Sync.md', type: 'slides' }
    ]}
  ];
</script>

<div class="space-y-1">
  {#each files as item}
    {#if item.type === 'folder'}
      <div>
        <button class="w-full flex items-center gap-2 px-2 py-1.5 text-zinc-300 hover:bg-zinc-800 rounded transition-colors group">
          <Folder size={16} class="text-blue-400" />
          <span class="text-sm flex-1 text-left">{item.name}</span>
        </button>
        <div class="pl-4 mt-1 space-y-1 border-l border-zinc-800 ml-4">
          {#each item.children as child}
            <button class="w-full flex items-center gap-2 px-2 py-1.5 text-zinc-400 hover:bg-zinc-800 rounded transition-colors group">
              <FileText size={16} class="text-zinc-500 group-hover:text-zinc-300" />
              <span class="text-sm flex-1 text-left truncate">{child.name}</span>
            </button>
          {/each}
        </div>
      </div>
    {:else}
      <button class="w-full flex items-center gap-2 px-2 py-1.5 text-zinc-400 hover:bg-zinc-800 rounded transition-colors group">
        <FileText size={16} class="text-zinc-500 group-hover:text-zinc-300" />
        <span class="text-sm flex-1 text-left truncate">{item.name}</span>
      </button>
    {/if}
  {/each}
</div>
