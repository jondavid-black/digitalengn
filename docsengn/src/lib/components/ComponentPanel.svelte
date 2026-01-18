<script>
  import { 
    Image as ImageIcon, 
    Table as TableIcon, 
    Square, 
    Circle, 
    Type,
    Quote
  } from 'lucide-svelte';

  const components = [
    { id: 'text', name: 'Text Block', icon: Type, group: 'Basic' },
    { id: 'heading', name: 'Heading', icon: Type, group: 'Basic' },
    { id: 'image', name: 'Image', icon: ImageIcon, group: 'Media' },
    { id: 'table', name: 'Table', icon: TableIcon, group: 'Data' },
    { id: 'quote', name: 'Blockquote', icon: Quote, group: 'Basic' },
    { id: 'rect', name: 'Rectangle', icon: Square, group: 'Shapes' },
    { id: 'circle', name: 'Circle', icon: Circle, group: 'Shapes' }
  ];

  const groups = [...new Set(components.map(c => c.group))];
</script>

<div class="space-y-6">
  {#each groups as group}
    <div class="space-y-2">
      <h3 class="text-xs font-semibold text-zinc-500 uppercase tracking-wider px-2">{group}</h3>
      <div class="grid grid-cols-2 gap-2">
        {#each components.filter(c => c.group === group) as comp}
          <button class="flex flex-col items-center gap-2 p-3 bg-zinc-800/50 border border-zinc-800 rounded-lg hover:bg-zinc-800 hover:border-zinc-700 transition-all group">
            <svelte:component this={comp.icon} size={20} class="text-zinc-400 group-hover:text-blue-400" />
            <span class="text-xs text-zinc-400 group-hover:text-zinc-200">{comp.name}</span>
          </button>
        {/each}
      </div>
    </div>
  {/each}
</div>
