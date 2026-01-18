<script>
  import "../app.css";
  import { ChevronLeft } from "lucide-svelte";
  import FileExplorer from "$lib/components/FileExplorer.svelte";
  import TabManager from "$lib/components/TabManager.svelte";
  import Toolbar from "$lib/components/Toolbar.svelte";
  import { drawerOpen } from "$lib/stores";

  function toggleDrawer() {
    drawerOpen.update(v => !v);
  }
</script>

<div class="flex h-screen w-full bg-zinc-950 text-zinc-100 overflow-hidden font-sans flex-col">
  <!-- Top Toolbar -->
  <Toolbar />

  <div class="flex-1 flex min-h-0">
    <!-- Drawer (File Explorer) -->
    {#if $drawerOpen}
      <aside class="w-72 border-r border-zinc-800 bg-zinc-900 flex flex-col z-40 shrink-0">
        <div class="p-4 border-b border-zinc-800 flex items-center justify-between bg-zinc-900/50">
          <h2 class="text-xs font-bold uppercase tracking-widest text-zinc-500">
            File Explorer
          </h2>
          <button on:click={toggleDrawer} class="p-1 text-zinc-500 hover:text-zinc-300 hover:bg-zinc-800 rounded transition-colors">
            <ChevronLeft size={18} />
          </button>
        </div>
        
        <div class="flex-1 overflow-y-auto p-4 custom-scrollbar">
          <FileExplorer />
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

