import StarterKit from "@tiptap/starter-kit";
import CharacterCount from "@tiptap/extension-character-count";
import Typography from "@tiptap/extension-typography";
import Underline from "@tiptap/extension-underline";
import { Markdown } from "tiptap-markdown";

export function getEditorExtensions() {
  return [StarterKit, CharacterCount, Typography, Underline, Markdown];
}
