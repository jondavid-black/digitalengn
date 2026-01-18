<script>
  import { activeTab, updateTabContent } from '$lib/stores';
  import MarkdownEditor from '$lib/components/MarkdownEditor.svelte';
  import SlideEditor from '$lib/components/SlideEditor.svelte';

  function handleContentChange(newContent) {
    if ($activeTab) {
      updateTabContent($activeTab.id, newContent);
    }
  }
</script>

{#if $activeTab}
  {#if $activeTab.type === 'markdown'}
    <MarkdownEditor 
      content={$activeTab.content} 
      onChange={handleContentChange} 
    />
  {:else if $activeTab.type === 'slides'}
    <SlideEditor 
      content={$activeTab.content} 
      onChange={handleContentChange} 
    />
  {/if}
{:else}
  <div class="flex items-center justify-center h-full text-zinc-500">
    <p>No document open</p>
  </div>
{/if}
