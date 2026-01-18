<script>
  import "../app.css";
  import { 
    Files, 
    PlusSquare, 
    Type, 
    Play, 
    ChevronLeft 
  } from "lucide-svelte";
  import { writable } from "svelte/store";
  import FileExplorer from "$lib/components/FileExplorer.svelte";
  import ComponentPanel from "$lib/components/ComponentPanel.svelte";
  import StylePanel from "$lib/components/StylePanel.svelte";
  import TabManager from "$lib/components/TabManager.svelte";

  const activeRailItem = writable(null);
  const drawerOpen = writable(false);
  const tabs = writable([
    { id: '1', title: 'Introduction.md', type: 'markdown', content: '# Welcome\n\nThis is a Tiptap based markdown editor.' }
  ]);
  const activeTabId = writable('1');

  const railItems = [
    { id: 'files', icon: Files, label: 'File Explorer', component: FileExplorer },
    { id: 'components', icon: PlusSquare, label: 'Components', component: ComponentPanel },
    { id: 'styles', icon: Type, label: 'Styles', component: StylePanel },
    { id: 'preview', icon: Play, label: 'Preview', component: null }
  ];

  function selectRailItem(id) {
    activeRailItem.update(current => {
      if (current === id) {
        drawerOpen.set(false);
        return null;
      } else {
        drawerOpen.set(true);
        return id;
      }
    });
  }

  function toggleDrawer() {
    drawerOpen.update(v => !v);
  }

  $: currentRailItem = railItems.find(i => i.id === $activeRailItem);
</script>

<div class="flex h-screen w-full bg-zinc-950 text-zinc-100 overflow-hidden font-sans">
  <!-- Side Rail -->
  <nav class="w-16 flex flex-col items-center py-4 border-r border-zinc-800 bg-zinc-900 z-50">
    <div class="flex-1 flex flex-col gap-4">
      {#each railItems as item}
        <button
          class="p-3 rounded-xl transition-all duration-200 hover:bg-zinc-800 {$activeRailItem === item.id ? 'bg-zinc-800 text-blue-400' : 'text-zinc-500 hover:text-zinc-300'}"
          on:click={() => selectRailItem(item.id)}
          title={item.label}
        >
          <svelte:component this={item.icon} size={24} strokeWidth={$activeRailItem === item.id ? 2.5 : 2} />
        </button>
      {/each}
    </div>
  </nav>

  <!-- Drawer -->
  {#if $drawerOpen}
    <aside class="w-72 border-r border-zinc-800 bg-zinc-900 flex flex-col z-40">
      <div class="p-4 border-b border-zinc-800 flex items-center justify-between bg-zinc-900/50">
        <h2 class="text-xs font-bold uppercase tracking-widest text-zinc-500">
          {currentRailItem?.label ?? ''}
        </h2>
        <button on:click={toggleDrawer} class="p-1 text-zinc-500 hover:text-zinc-300 hover:bg-zinc-800 rounded transition-colors">
          <ChevronLeft size={18} />
        </button>
      </div>
      
      <div class="flex-1 overflow-y-auto p-4 custom-scrollbar">
        {#if currentRailItem?.component}
          <svelte:component this={currentRailItem.component} />
        {:else if $activeRailItem === 'preview'}
          <div class="text-sm text-zinc-400 italic">Preview mode active. External window will open...</div>
        {/if}
      </div>
    </aside>
  {/if}

  <!-- Main Content Area -->
  <main class="flex-1 flex flex-col min-w-0 bg-zinc-950">
    <!-- Tabs Bar -->
    <TabManager {tabs} {activeTabId} />

    <!-- Editor Pane -->
    <div class="flex-1 overflow-hidden relative">
      <slot />
    </div>
  </main>
</div>

<style>
  :global(.custom-scrollbar::-webkit-scrollbar) {
    width: 6px;
  }
  :global(.custom-scrollbar::-webkit-scrollbar-track) {
    background: transparent;
  }
  :global(.custom-scrollbar::-webkit-scrollbar-thumb) {
    background: #27272a;
    border-radius: 10px;
  }
  :global(.custom-scrollbar::-webkit-scrollbar-thumb:hover) {
    background: #3f3f46;
  }
</style>
