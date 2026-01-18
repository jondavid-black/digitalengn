import { describe, it, expect } from "vitest";
import { getEditorExtensions } from "./editorConfig";

describe("editorConfig", () => {
  it("should include all required extensions", () => {
    const extensions = getEditorExtensions();

    const extensionNames = extensions.map((e) => e.name);

    // StarterKit includes bold and italic
    // We check for the explicit extensions we added
    expect(extensionNames).toContain("characterCount");
    expect(extensionNames).toContain("typography");
    expect(extensionNames).toContain("underline");
    expect(extensionNames).toContain("markdown");

    // Check StarterKit presence (it's a wrapper, name might be 'starterKit' or similar)
    // Tiptap extensions usually have a name property.
    // StarterKit is an extension itself.
    expect(extensionNames).toContain("starterKit");
  });
});
