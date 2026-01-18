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
  import { tabs, activeTabId, activeTab } from "$lib/stores";

  const activeRailItem = writable(null);
  const drawerOpen = writable(false);

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
          <div class="flex flex-col gap-4">
            <p class="text-sm text-zinc-400">
              Preview the current document in a new window.
            </p>
            {#if $activeTab}
              <a 
                href="/preview?filename={encodeURIComponent($activeTab.title)}" 
                target="_blank"
                class="flex items-center justify-center gap-2 p-3 bg-blue-600 hover:bg-blue-500 text-white rounded-lg transition-colors font-medium text-sm"
              >
                <Play size={16} />
                Open Preview
              </a>
            {:else}
              <p class="text-sm text-zinc-500 italic">No document open.</p>
            {/if}
          </div>
        {/if}
      </div>
    </aside>
  {/if}

  <!-- Main Content Area -->
  <main class="flex-1 flex flex-col min-w-0 bg-zinc-950">
    <!-- Tabs Bar -->
    <TabManager />

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
