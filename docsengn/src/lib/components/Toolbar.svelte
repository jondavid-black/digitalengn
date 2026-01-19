<script>
  import { 
    Folder, 
    Play,
    Menu,
    ChevronDown
  } from 'lucide-svelte';
  import { drawerOpen, activeTab } from '$lib/stores';
  import ComponentPanel from './ComponentPanel.svelte';
  import StylePanel from './StylePanel.svelte';

  // We might need to refactor ComponentPanel/StylePanel to accept orientation or class
  // For now, I'll reimplement the tools here or wrapping them.
  // Given "Strictly follow standard process", reusing components is better.
  // I'll create new components `ToolbarTools.svelte` later if needed.
  // For now I'll inline the tools logic or simple buttons for MVP of the toolbar.

  import { 
    Image as ImageIcon, 
    Table as TableIcon, 
    Square, 
    Circle, 
    Type,
    Quote,
    Bold, 
    Italic, 
    Underline,
    AlignLeft,
    AlignCenter,
    AlignRight,
    Strikethrough,
    Code,
    RemoveFormatting,
    Eraser,
    List,
    ListOrdered,
    SquareCode,
    Minus,
    WrapText,
    Undo,
    Redo,
    Palette
  } from 'lucide-svelte';
  import { editorAction } from '$lib/stores';

  function dispatch(type, payload) {
    editorAction.set({ type, payload });
  }

  function toggleDrawer() {
    drawerOpen.update(v => !v);
  }

  let showHeadings = false;
</script>

<div class="h-14 bg-zinc-900 border-b border-zinc-800 flex items-center px-4 gap-4 shrink-0 z-50">
  <!-- Left: File Explorer Toggle -->
  <button 
    on:click={toggleDrawer}
    class="p-2 text-zinc-400 hover:text-zinc-100 hover:bg-zinc-800 rounded-lg transition-colors flex items-center gap-2"
    title="Toggle File Explorer"
  >
    <Menu size={20} />
    <span class="text-sm font-medium">File Explorer</span>
  </button>

  <div class="w-px h-8 bg-zinc-800 mx-2"></div>

  <!-- Middle: Contextual Tools -->
  <div class="flex-1 flex items-center gap-2 overflow-x-visible custom-scrollbar">
    {#if $activeTab?.type === 'markdown' || $activeTab?.type === 'slides'}
      <!-- Formatting Group -->
      <div class="flex items-center gap-1 p-1 bg-zinc-950/50 rounded-lg border border-zinc-800/50">
        <button on:click={() => dispatch('toggleBold')} class="p-1.5 text-zinc-400 hover:text-zinc-100 hover:bg-zinc-800 rounded" title="Bold">
          <Bold size={18} />
        </button>
        <button on:click={() => dispatch('toggleItalic')} class="p-1.5 text-zinc-400 hover:text-zinc-100 hover:bg-zinc-800 rounded" title="Italic">
          <Italic size={18} />
        </button>
        <button on:click={() => dispatch('toggleUnderline')} class="p-1.5 text-zinc-400 hover:text-zinc-100 hover:bg-zinc-800 rounded" title="Underline">
          <Underline size={18} />
        </button>
        <button on:click={() => dispatch('toggleStrike')} class="p-1.5 text-zinc-400 hover:text-zinc-100 hover:bg-zinc-800 rounded" title="Strike">
          <Strikethrough size={18} />
        </button>
        <button on:click={() => dispatch('toggleCode')} class="p-1.5 text-zinc-400 hover:text-zinc-100 hover:bg-zinc-800 rounded" title="Code">
          <Code size={18} />
        </button>
        <button on:click={() => dispatch('setColor', '#958DF1')} class="p-1.5 text-zinc-400 hover:text-zinc-100 hover:bg-zinc-800 rounded" title="Purple">
          <Palette size={18} color="#958DF1" />
        </button>
        <div class="w-px h-4 bg-zinc-800 mx-1"></div>
        <button on:click={() => dispatch('unsetAllMarks')} class="p-1.5 text-zinc-400 hover:text-zinc-100 hover:bg-zinc-800 rounded" title="Clear Marks">
          <Eraser size={18} />
        </button>
        <button on:click={() => dispatch('clearNodes')} class="p-1.5 text-zinc-400 hover:text-zinc-100 hover:bg-zinc-800 rounded" title="Clear Nodes">
          <RemoveFormatting size={18} />
        </button>
      </div>

      <!-- Lists Group -->
      <div class="flex items-center gap-1 p-1 bg-zinc-950/50 rounded-lg border border-zinc-800/50">
        <button on:click={() => dispatch('toggleBulletList')} class="p-1.5 text-zinc-400 hover:text-zinc-100 hover:bg-zinc-800 rounded" title="Bullet List">
          <List size={18} />
        </button>
        <button on:click={() => dispatch('toggleOrderedList')} class="p-1.5 text-zinc-400 hover:text-zinc-100 hover:bg-zinc-800 rounded" title="Ordered List">
          <ListOrdered size={18} />
        </button>
      </div>

      <!-- Alignment Group -->
      <div class="flex items-center gap-1 p-1 bg-zinc-950/50 rounded-lg border border-zinc-800/50">
        <button on:click={() => dispatch('setTextAlign', 'left')} class="p-1.5 text-zinc-400 hover:text-zinc-100 hover:bg-zinc-800 rounded" title="Align Left">
          <AlignLeft size={18} />
        </button>
        <button on:click={() => dispatch('setTextAlign', 'center')} class="p-1.5 text-zinc-400 hover:text-zinc-100 hover:bg-zinc-800 rounded" title="Align Center">
          <AlignCenter size={18} />
        </button>
        <button on:click={() => dispatch('setTextAlign', 'right')} class="p-1.5 text-zinc-400 hover:text-zinc-100 hover:bg-zinc-800 rounded" title="Align Right">
          <AlignRight size={18} />
        </button>
      </div>

      <div class="w-px h-6 bg-zinc-800 mx-1"></div>

      <!-- Insert Group -->
      <div class="flex items-center gap-1">
        <button on:click={() => dispatch('setParagraph')} class="flex items-center gap-1 px-2 py-1.5 text-zinc-400 hover:text-zinc-100 hover:bg-zinc-800 rounded text-sm" title="Paragraph">
          <Type size={18} />
          <span class="hidden xl:inline">Para</span>
        </button>
        <div class="relative">
          <button 
            on:click={() => showHeadings = !showHeadings} 
            class="flex items-center gap-1 px-2 py-1.5 text-zinc-400 hover:text-zinc-100 hover:bg-zinc-800 rounded text-sm {showHeadings ? 'bg-zinc-800 text-zinc-100' : ''}" 
            title="Heading"
          >
            <Type size={18} class="font-bold" />
            <span class="hidden xl:inline">Heading</span>
            <ChevronDown size={14} />
          </button>

          {#if showHeadings}
            <div class="fixed inset-0 z-40" on:click={() => showHeadings = false} role="presentation"></div>
            <div class="absolute top-full left-0 mt-1 w-48 bg-zinc-900 border border-zinc-700 rounded-lg shadow-xl z-50 flex flex-col p-1">
              {#each [1, 2, 3, 4, 5, 6] as level}
                <button 
                  on:click={() => { dispatch('toggleHeading', level); showHeadings = false; }}
                  class="flex items-center gap-2 px-3 py-2 text-left hover:bg-zinc-800 rounded text-zinc-300 hover:text-zinc-100"
                >
                  <span class={
                    level === 1 ? "text-2xl font-bold" :
                    level === 2 ? "text-xl font-bold" :
                    level === 3 ? "text-lg font-bold" :
                    level === 4 ? "text-base font-bold" :
                    level === 5 ? "text-sm font-bold" :
                    "text-xs font-bold"
                  }>H{level}</span>
                  <span class="text-sm">Heading {level}</span>
                </button>
              {/each}
            </div>
          {/if}
        </div>
        <button on:click={() => dispatch('addImage')} class="flex items-center gap-1 px-2 py-1.5 text-zinc-400 hover:text-zinc-100 hover:bg-zinc-800 rounded text-sm" title="Image">
          <ImageIcon size={18} />
          <span class="hidden xl:inline">Image</span>
        </button>
        <button on:click={() => dispatch('insertTable')} class="flex items-center gap-1 px-2 py-1.5 text-zinc-400 hover:text-zinc-100 hover:bg-zinc-800 rounded text-sm" title="Table">
          <TableIcon size={18} />
          <span class="hidden xl:inline">Table</span>
        </button>
        <button on:click={() => dispatch('toggleCodeBlock')} class="flex items-center gap-1 px-2 py-1.5 text-zinc-400 hover:text-zinc-100 hover:bg-zinc-800 rounded text-sm" title="Code Block">
          <SquareCode size={18} />
          <span class="hidden xl:inline">Code</span>
        </button>
        <button on:click={() => dispatch('toggleBlockquote')} class="flex items-center gap-1 px-2 py-1.5 text-zinc-400 hover:text-zinc-100 hover:bg-zinc-800 rounded text-sm" title="Quote">
          <Quote size={18} />
          <span class="hidden xl:inline">Quote</span>
        </button>
        <button on:click={() => dispatch('setHorizontalRule')} class="flex items-center gap-1 px-2 py-1.5 text-zinc-400 hover:text-zinc-100 hover:bg-zinc-800 rounded text-sm" title="Horizontal Rule">
          <Minus size={18} />
          <span class="hidden xl:inline">HR</span>
        </button>
        <button on:click={() => dispatch('setHardBreak')} class="flex items-center gap-1 px-2 py-1.5 text-zinc-400 hover:text-zinc-100 hover:bg-zinc-800 rounded text-sm" title="Hard Break">
          <WrapText size={18} />
          <span class="hidden xl:inline">Break</span>
        </button>
      </div>

      <div class="w-px h-6 bg-zinc-800 mx-1"></div>

      <!-- History Group -->
      <div class="flex items-center gap-1">
        <button on:click={() => dispatch('undo')} class="p-1.5 text-zinc-400 hover:text-zinc-100 hover:bg-zinc-800 rounded" title="Undo">
          <Undo size={18} />
        </button>
        <button on:click={() => dispatch('redo')} class="p-1.5 text-zinc-400 hover:text-zinc-100 hover:bg-zinc-800 rounded" title="Redo">
          <Redo size={18} />
        </button>
      </div>

      {#if $activeTab?.type === 'slides'}
        <div class="w-px h-6 bg-zinc-800 mx-1"></div>
        <!-- Slide Specific -->
        <div class="flex items-center gap-1">
           <button on:click={() => dispatch('insertShape', 'rect')} class="flex items-center gap-1 px-2 py-1.5 text-zinc-400 hover:text-zinc-100 hover:bg-zinc-800 rounded text-sm" title="Rectangle">
            <Square size={18} />
            <span class="hidden xl:inline">Rect</span>
          </button>
          <button on:click={() => dispatch('insertShape', 'circle')} class="flex items-center gap-1 px-2 py-1.5 text-zinc-400 hover:text-zinc-100 hover:bg-zinc-800 rounded text-sm" title="Circle">
            <Circle size={18} />
            <span class="hidden xl:inline">Circle</span>
          </button>
        </div>
      {/if}

    {:else}
      <span class="text-sm text-zinc-500 italic">No document open</span>
    {/if}
  </div>

  <!-- Right: Actions -->
  <div class="flex items-center gap-2">
     {#if $activeTab}
      <a 
        href="/preview?filename={encodeURIComponent($activeTab.title)}" 
        target="_blank"
        class="flex items-center gap-2 px-3 py-1.5 bg-zinc-800 hover:bg-zinc-700 text-zinc-200 rounded-lg transition-colors text-sm font-medium"
      >
        <Play size={16} />
        Preview
      </a>
    {/if}
  </div>
</div>
