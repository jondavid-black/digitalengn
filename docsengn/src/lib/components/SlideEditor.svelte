<script>
  import { onMount, onDestroy } from 'svelte';
  import { Editor } from '@tiptap/core';
  import { getEditorExtensions } from '$lib/editorConfig';
  import { editorAction } from '$lib/stores';
  import { MonitorPlay } from 'lucide-svelte';

  export let content = '';
  export let onChange = (markdown) => {};

  let element;
  let editor;
  let unsubscribe;

  onMount(() => {
    editor = new Editor({
      element: element,
      extensions: getEditorExtensions(),
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

    unsubscribe = editorAction.subscribe(action => {
      if (!action || !editor) return;
      
      switch (action.type) {
        case 'insertText':
          editor.chain().focus().insertContent('New Text Block').run();
          break;
        case 'toggleHeading':
          const level = action.payload || 2;
          editor.chain().focus().toggleHeading({ level }).run();
          break;
        case 'toggleBlockquote':
          editor.chain().focus().toggleBlockquote().run();
          break;
        case 'addImage':
          editor.chain().focus().insertContent('![Image](https://placehold.co/600x400)').run();
          break;
        case 'insertTable':
          // Table extension not loaded yet, inserting markdown table representation
          editor.chain().focus().insertContent('\n| Header 1 | Header 2 |\n| --- | --- |\n| Cell 1 | Cell 2 |\n').run();
          break;
        case 'insertShape':
          editor.chain().focus().insertContent(`\n> Shape: ${action.payload}\n`).run();
          break;
        case 'toggleBold':
          editor.chain().focus().toggleBold().run();
          break;
        case 'toggleItalic':
          editor.chain().focus().toggleItalic().run();
          break;
        case 'toggleUnderline':
          editor.chain().focus().toggleUnderline().run();
          break;
        case 'setTextAlign':
          // Requires extension-text-align
          // editor.chain().focus().setTextAlign(action.payload).run();
          break;
      }
      
      // Reset action to null
      editorAction.set(null);
    });
  });

  onDestroy(() => {
    if (unsubscribe) unsubscribe();
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
