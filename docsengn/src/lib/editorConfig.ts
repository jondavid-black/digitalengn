import StarterKit from "@tiptap/starter-kit";
import CharacterCount from "@tiptap/extension-character-count";
import Typography from "@tiptap/extension-typography";
import Underline from "@tiptap/extension-underline";
import { Color } from "@tiptap/extension-color";
import { TextStyle } from "@tiptap/extension-text-style";
import { ListItem } from "@tiptap/extension-list-item";
import { Markdown } from "tiptap-markdown";

export function getEditorExtensions() {
  return [
    StarterKit,
    CharacterCount,
    Typography,
    Underline,
    TextStyle,
    Color,
    ListItem,
    Markdown,
  ];
}
