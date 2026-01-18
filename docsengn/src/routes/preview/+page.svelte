<script>
  import { page } from '$app/stores';
  import { onMount } from 'svelte';
  import MarkdownEditor from '$lib/components/MarkdownEditor.svelte';

  let content = '';
  let loading = true;
  let error = null;

  onMount(async () => {
    const filename = $page.url.searchParams.get('filename');
    if (!filename) {
      error = 'No filename provided';
      loading = false;
      return;
    }

    try {
      const res = await fetch(`/api/content?filename=${encodeURIComponent(filename)}`);
      if (!res.ok) throw new Error('Failed to load content');
      const data = await res.json();
      content = data.content;
    } catch (e) {
      error = e.message;
    } finally {
      loading = false;
    }
  });
</script>

<div class="min-h-screen bg-white text-zinc-900 p-8">
  <div class="max-w-4xl mx-auto">
    {#if loading}
      <p>Loading...</p>
    {:else if error}
      <p class="text-red-500">Error: {error}</p>
    {:else}
      <h1 class="text-3xl font-bold mb-8 pb-4 border-b">Preview: {$page.url.searchParams.get('filename')}</h1>
      <MarkdownEditor {content} editable={false} />
    {/if}
  </div>
</div>
