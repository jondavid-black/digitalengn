<script>
  import { 
    Image as ImageIcon, 
    Table as TableIcon, 
    Square, 
    Circle, 
    Type,
    Quote
  } from 'lucide-svelte';
  import { editorAction } from '$lib/stores';

  const components = [
    { id: 'text', name: 'Text Block', icon: Type, group: 'Basic', action: 'insertText' },
    { id: 'heading', name: 'Heading', icon: Type, group: 'Basic', action: 'toggleHeading' },
    { id: 'image', name: 'Image', icon: ImageIcon, group: 'Media', action: 'addImage' },
    { id: 'table', name: 'Table', icon: TableIcon, group: 'Data', action: 'insertTable' },
    { id: 'quote', name: 'Blockquote', icon: Quote, group: 'Basic', action: 'toggleBlockquote' },
    { id: 'rect', name: 'Rectangle', icon: Square, group: 'Shapes', action: 'insertShape', payload: 'rect' },
    { id: 'circle', name: 'Circle', icon: Circle, group: 'Shapes', action: 'insertShape', payload: 'circle' }
  ];

  const groups = [...new Set(components.map(c => c.group))];

  function handleComponentClick(comp) {
    editorAction.set({ type: comp.action, payload: comp.payload });
  }
</script>

<div class="space-y-6">
  {#each groups as group}
    <div class="space-y-2">
      <h3 class="text-xs font-semibold text-zinc-500 uppercase tracking-wider px-2">{group}</h3>
      <div class="grid grid-cols-2 gap-2">
        {#each components.filter(c => c.group === group) as comp}
          <button 
            on:click={() => handleComponentClick(comp)}
            class="flex flex-col items-center gap-2 p-3 bg-zinc-800/50 border border-zinc-800 rounded-lg hover:bg-zinc-800 hover:border-zinc-700 transition-all group"
          >
            <svelte:component this={comp.icon} size={20} class="text-zinc-400 group-hover:text-blue-400" />
            <span class="text-xs text-zinc-400 group-hover:text-zinc-200">{comp.name}</span>
          </button>
        {/each}
      </div>
    </div>
  {/each}
</div>
