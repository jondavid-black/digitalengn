<script>
  import { onMount, onDestroy } from 'svelte';
  import { Editor } from '@tiptap/core';
  import StarterKit from '@tiptap/starter-kit';
  import CharacterCount from '@tiptap/extension-character-count';
  import Typography from '@tiptap/extension-typography';
  import { Markdown } from 'tiptap-markdown';
  import { MonitorPlay } from 'lucide-svelte';

  export let content = '';
  export let onChange = (markdown) => {};

  let element;
  let editor;

  onMount(() => {
    editor = new Editor({
      element: element,
      extensions: [
        StarterKit,
        CharacterCount,
        Typography,
        Markdown
      ],
      content: content,
      onUpdate: ({ editor }) => {
        onChange(editor.storage.markdown.getMarkdown());
      },
      editorProps: {
        attributes: {
          class: 'prose prose-invert max-w-none focus:outline-none min-h-[500px] p-8',
        },
      },
    });
  });

  onDestroy(() => {
    if (editor) {
      editor.destroy();
    }
  });

  $: if (editor && content !== editor.storage.markdown.getMarkdown()) {
    editor.commands.setContent(content, false);
  }
</script>

<div class="flex flex-col h-full bg-zinc-950">
  <div class="flex items-center gap-2 px-4 py-2 bg-zinc-900/50 border-b border-zinc-800 text-zinc-400 text-sm">
    <MonitorPlay size={16} />
    <span>Slide Editor Mode</span>
  </div>
  <div class="flex-1 overflow-y-auto custom-scrollbar">
    <div bind:this={element} />
  </div>
</div>

<style>
  :global(.tiptap p.is-editor-empty:first-child::before) {
    content: attr(data-placeholder);
    float: left;
    color: #52525b;
    pointer-events: none;
    height: 0;
  }

  :global(.tiptap) {
    outline: none !important;
  }
</style>
