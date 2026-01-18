<script>
  import { onMount, onDestroy } from 'svelte';
  import { Editor } from '@tiptap/core';
  import StarterKit from '@tiptap/starter-kit';
  import CharacterCount from '@tiptap/extension-character-count';
  import Typography from '@tiptap/extension-typography';

  export let content = '';
  export let onChange = () => {};

  let element;
  let editor;

  onMount(() => {
    editor = new Editor({
      element: element,
      extensions: [
        StarterKit,
        CharacterCount,
        Typography
      ],
      content: content,
      onUpdate: ({ editor }) => {
        onChange(editor.getHTML());
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

  $: if (editor && content !== editor.getHTML()) {
    editor.commands.setContent(content, false);
  }
</script>

<div class="w-full h-full overflow-y-auto bg-zinc-950 custom-scrollbar">
  <div bind:this={element} />
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
