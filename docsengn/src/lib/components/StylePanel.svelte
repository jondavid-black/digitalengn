<script>
  import { 
    AlignCenter, 
    AlignLeft, 
    AlignRight, 
    Bold, 
    Italic, 
    Underline
  } from 'lucide-svelte';

  let fontSize = 16;
  let color = '#ffffff';
  let strokeWidth = 1;
</script>

<div class="space-y-6">
  <!-- Typography Section -->
  <div class="space-y-4">
    <h3 class="text-xs font-semibold text-zinc-500 uppercase tracking-wider px-2">Typography</h3>
    
    <div class="space-y-3 px-2">
      <div class="flex flex-col gap-1.5">
        <label for="font-size" class="text-xs text-zinc-500">Font Size: {fontSize}px</label>
        <input 
          id="font-size"
          type="range" 
          min="8" 
          max="72" 
          bind:value={fontSize}
          class="w-full h-1.5 bg-zinc-800 rounded-lg appearance-none cursor-pointer accent-blue-500"
        />
      </div>

      <div class="flex items-center gap-1">
        <button class="flex-1 p-2 bg-zinc-800 border border-zinc-700 rounded hover:bg-zinc-700 transition-colors">
          <Bold size={16} class="mx-auto" />
        </button>
        <button class="flex-1 p-2 bg-zinc-800 border border-zinc-700 rounded hover:bg-zinc-700 transition-colors">
          <Italic size={16} class="mx-auto" />
        </button>
        <button class="flex-1 p-2 bg-zinc-800 border border-zinc-700 rounded hover:bg-zinc-700 transition-colors">
          <Underline size={16} class="mx-auto" />
        </button>
      </div>

      <div class="flex items-center gap-1">
        <button class="flex-1 p-2 bg-zinc-800 border border-zinc-700 rounded hover:bg-zinc-700 transition-colors">
          <AlignLeft size={16} class="mx-auto" />
        </button>
        <button class="flex-1 p-2 bg-zinc-800 border border-zinc-700 rounded hover:bg-zinc-700 transition-colors">
          <AlignCenter size={16} class="mx-auto" />
        </button>
        <button class="flex-1 p-2 bg-zinc-800 border border-zinc-700 rounded hover:bg-zinc-700 transition-colors">
          <AlignRight size={16} class="mx-auto" />
        </button>
      </div>
    </div>
  </div>

  <!-- Appearance Section -->
  <div class="space-y-4 pt-4 border-t border-zinc-800">
    <h3 class="text-xs font-semibold text-zinc-500 uppercase tracking-wider px-2">Appearance</h3>
    
    <div class="space-y-3 px-2">
      <div class="flex items-center justify-between">
        <span class="text-xs text-zinc-500">Fill Color</span>
        <div class="flex items-center gap-2">
          <span class="text-[10px] text-zinc-500 font-mono uppercase">{color}</span>
          <input type="color" bind:value={color} class="w-6 h-6 rounded-md bg-transparent border-none cursor-pointer" />
        </div>
      </div>

      <div class="flex flex-col gap-1.5">
        <label for="stroke-width" class="text-xs text-zinc-500">Stroke Weight: {strokeWidth}px</label>
        <input 
          id="stroke-width"
          type="range" 
          min="0" 
          max="20" 
          bind:value={strokeWidth}
          class="w-full h-1.5 bg-zinc-800 rounded-lg appearance-none cursor-pointer accent-blue-500"
        />
      </div>
    </div>
  </div>
</div>
