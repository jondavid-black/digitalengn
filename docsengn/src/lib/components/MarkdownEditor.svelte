<script>
  import { onMount, onDestroy } from 'svelte';
  import { Editor } from '@tiptap/core';
  import { getEditorExtensions } from '$lib/editorConfig';
  import { editorAction } from '$lib/stores';

  export let content = '';
  export let editable = true;
  export let onChange = (markdown) => {};

  let element;
  let editor;
  let unsubscribe;

  onMount(() => {
    editor = new Editor({
      element: element,
      editable: editable,
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
        case 'toggleStrike':
          editor.chain().focus().toggleStrike().run();
          break;
        case 'toggleCode':
          editor.chain().focus().toggleCode().run();
          break;
        case 'unsetAllMarks':
          editor.chain().focus().unsetAllMarks().run();
          break;
        case 'clearNodes':
          editor.chain().focus().clearNodes().run();
          break;
        case 'setParagraph':
          editor.chain().focus().setParagraph().run();
          break;
        case 'toggleBulletList':
          editor.chain().focus().toggleBulletList().run();
          break;
        case 'toggleOrderedList':
          editor.chain().focus().toggleOrderedList().run();
          break;
        case 'toggleCodeBlock':
          editor.chain().focus().toggleCodeBlock().run();
          break;
        case 'setHorizontalRule':
          editor.chain().focus().setHorizontalRule().run();
          break;
        case 'setHardBreak':
          editor.chain().focus().setHardBreak().run();
          break;
        case 'undo':
          editor.chain().focus().undo().run();
          break;
        case 'redo':
          editor.chain().focus().redo().run();
          break;
        case 'setColor':
          editor.chain().focus().setColor(action.payload).run();
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

  // Watch for external content changes
  $: if (editor && content !== editor.storage.markdown.getMarkdown()) {
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

  :global(.tiptap ul) {
    list-style-type: disc;
    padding: 0 1rem;
    margin: 1.25rem 1rem 1.25rem 0.4rem;
  }

  :global(.tiptap ol) {
    list-style-type: decimal;
    padding: 0 1rem;
    margin: 1.25rem 1rem 1.25rem 0.4rem;
  }

  :global(.tiptap blockquote) {
    border-left: 3px solid #52525b;
    margin: 1.5rem 0;
    padding-left: 1rem;
  }

  :global(.tiptap pre) {
    background: #09090b;
    border-radius: 0.5rem;
    color: #f4f4f5;
    font-family: "JetBrainsMono", monospace;
    margin: 1.5rem 0;
    padding: 0.75rem 1rem;
  }

  :global(.tiptap code) {
    background-color: #27272a;
    border-radius: 0.4rem;
    color: #f4f4f5;
    font-size: 0.85rem;
    padding: 0.25em 0.3em;
  }

  :global(.tiptap pre code) {
    background: none;
    color: inherit;
    font-size: 0.8rem;
    padding: 0;
  }

  :global(.tiptap hr) {
    border: none;
    border-top: 1px solid #27272a;
    margin: 2rem 0;
  }
</style>
